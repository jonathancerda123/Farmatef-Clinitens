"""Importación acotada y entrega temporal de credenciales desde servidor."""
from datetime import timedelta
from io import BytesIO
import secrets
from zipfile import ZipFile, BadZipFile
from xml.etree.ElementTree import ParseError
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.utils import timezone
from openpyxl import load_workbook, Workbook
from openpyxl.utils.exceptions import InvalidFileException
from openpyxl.styles import Font, PatternFill, Alignment
from UsuarioApp.models import Profile, Position


def leer_filas(archivo):
    try:
        archivo.seek(0)
        with ZipFile(archivo) as archive:
            files = archive.infolist()
            if len(files) > 500 or sum(x.file_size for x in files) > 40 * 1024 * 1024:
                raise ValidationError("El Excel excede los límites de lectura.")
        archivo.seek(0)
        libro = load_workbook(archivo, read_only=True, data_only=True, keep_links=False)
        try:
            if libro.active is None:
                raise ValidationError("El Excel no contiene una hoja activa.")
            rows = []
            for row in libro.active.iter_rows(values_only=True):
                if len(rows) >= 2001 or len(row) > 30:
                    raise ValidationError("Máximo 2000 estudiantes y 30 columnas.")
                rows.append(row)
            return rows
        finally:
            libro.close()
    except (BadZipFile, InvalidFileException, OSError, ValueError, KeyError, ParseError, EOFError):
        raise ValidationError("El archivo Excel está dañado o no es compatible.")


def importar(rows, curso, normalizar, generar_password):
    if not rows:
        raise ValidationError("El archivo Excel está vacío.")
    headers = [normalizar(v) for v in rows[0]]
    required = ["username", "email", "first_name", "last_name"]
    if any(headers.count(k) != 1 for k in required):
        raise ValidationError("Debe haber una columna de usuario, correo, nombre y apellido, sin duplicados.")
    indices = {k: headers.index(k) for k in required}
    result = {"creados": 0, "agregados": 0, "ya_inscritos": 0, "errores": []}
    credentials, seen_users, seen_emails = [], set(), set()
    for numero, row in enumerate(rows[1:], start=2):
        data = {k: str(row[i] if i < len(row) and row[i] is not None else "").strip()
                for k, i in indices.items()}
        if not any(data.values()):
            continue
        data["email"] = data["email"].lower()
        try:
            if not all(data.values()) or any("\x00" in v for v in data.values()):
                raise ValidationError("Faltan datos obligatorios o contienen caracteres no válidos.")
            key_user, key_email = data["username"].casefold(), data["email"].casefold()
            if key_user in seen_users or key_email in seen_emails:
                raise ValidationError("Usuario o correo repetido en el archivo.")
            seen_users.add(key_user)
            seen_emails.add(key_email)
            candidate = User(**data)
            # Valida campos incluso si la cuenta ya existe; unicidad se trata debajo.
            candidate.clean_fields(exclude=["password"])
            matches = User.objects.filter(email__iexact=data["email"])
            email_user = matches.first()
            name_user = User.objects.filter(username__iexact=data["username"]).first()
            if email_user or name_user:
                if matches.count() != 1 or not email_user or not name_user or email_user.pk != name_user.pk:
                    raise ValidationError("Correo y usuario deben identificar la misma cuenta existente.")
                user = email_user
                profile = getattr(user, "profile", None)
                if user.is_superuser or not user.is_active or not profile or not profile.position_FK or profile.position_FK.permission_code != "RESTRICTED":
                    raise ValidationError("La cuenta existente no es un estudiante activo con perfil.")
                with transaction.atomic():
                    if curso.estudiantes.filter(pk=user.pk).exists():
                        result["ya_inscritos"] += 1
                    else:
                        curso.estudiantes.add(user)
                        result["agregados"] += 1
                continue
            password = generar_password()
            with transaction.atomic():
                position = Position.objects.filter(permission_code="RESTRICTED").first()
                if position is None:
                    position = Position.objects.create(user_position="Estudiante importado", permission_code="RESTRICTED")
                candidate.set_password(password)
                candidate.save()
                Profile.objects.create(user_FK=candidate, position_FK=position,
                    requiere_cambio_password=True, password_temporal_expira=timezone.now() + timedelta(hours=24))
                curso.estudiantes.add(candidate)
            credentials.append({"user_id": candidate.pk, "username": candidate.username,
                "email": candidate.email, "nombre": candidate.get_full_name(), "password": password})
            result["creados"] += 1
        except (ValidationError, IntegrityError) as error:
            detail = "; ".join(error.messages) if isinstance(error, ValidationError) else "Conflicto de datos; no se creó la cuenta."
            result["errores"].append({"fila": numero, "motivo": detail})
    return result, credentials


def guardar_credenciales(request, curso, credenciales):
    if not credenciales:
        return None
    session_token = request.session.setdefault("entrega_credenciales", secrets.token_urlsafe(32))
    token = secrets.token_urlsafe(32)
    cache.set("credenciales:" + token, {"usuario": request.user.pk, "curso": curso.pk,
              "sesion": session_token, "filas": credenciales}, timeout=600)
    return token


def consumir_credenciales(request, curso, token):
    if not isinstance(token, str) or len(token) != 43:
        raise ValidationError("Descarga no válida o caducada.")
    key = "credenciales:" + token
    record = cache.get(key)
    if not record or record["usuario"] != request.user.pk or record["curso"] != curso.pk or record["sesion"] != request.session.get("entrega_credenciales"):
        raise ValidationError("Descarga no válida o caducada.")
    if not cache.add(key + ":usado", True, timeout=600):
        raise ValidationError("Las credenciales ya fueron descargadas.")
    cache.delete(key)
    rows = record["filas"]
    if set(x["user_id"] for x in rows) - set(curso.estudiantes.values_list("id", flat=True)):
        raise ValidationError("La matrícula cambió; la descarga ya no es válida.")
    return rows


def excel_credenciales(rows):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Credenciales"
    sheet.append(["Usuario", "Correo", "Nombre completo", "Contraseña temporal"])
    for record in rows:
        sheet.append([record[k] for k in ["username", "email", "nombre", "password"]])
        # Excel trata literalmente todo el contenido, incluso = + - @.
        for cell in sheet[sheet.max_row]:
            cell.data_type = "s"
    for col, width in [("A", 25), ("B", 35), ("C", 40), ("D", 25)]:
        sheet.column_dimensions[col].width = width
    for row in sheet:
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="center")
        sheet.row_dimensions[row[0].row].height = 32
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1D65B7")
    sheet.freeze_panes = "A2"
    output = BytesIO()
    workbook.save(output)
    return output.getvalue()
