import json
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from core.test_helpers import usuario
from CliniTensFichaApp.models import FichaClinica
from .models import CasoClinico, CodigoActividad
from .forms import CasoClinicoForm
from .evaluation import guardar_evaluacion
from .rubrica import RUBRICA
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.contrib.auth.models import User
from UsuarioApp.models import Profile
from .models import Curso, Paciente, ResultadoDiagnostico, CasoMultimedia
from .students import importar, leer_filas, excel_credenciales
from .views import normalizar_encabezado
from io import BytesIO
from openpyxl import Workbook, load_workbook


class SeguridadDocenteTests(TestCase):
    def setUp(self):
        self.docente = usuario("docente", "MANAGER")
        self.otro = usuario("otro", "MANAGER")
        self.alumno = usuario("alumno")
        self.caso = CasoClinico.objects.create(titulo="Simulación", contenido="<p>Ficticio</p>", creado_por=self.docente)
        self.codigo = CodigoActividad.objects.create(codigo="DEMO", caso_clinico=self.caso, creado_por=self.docente, activo=True)
        self.ficha = FichaClinica.objects.create(codigo_actividad=self.codigo, estudiante=self.alumno,
                    docente=self.docente, estado="ENVIADA")

    def test_otro_docente_no_revisa_rubrica_ajena(self):
        self.client.force_login(self.otro)
        self.assertEqual(self.client.get(reverse("clinitensdocente:ficha_rubrica", args=[self.ficha.pk])).status_code, 404)

    def test_otro_docente_no_edita_caso(self):
        self.client.force_login(self.otro)
        self.assertEqual(self.client.get(reverse("clinitensdocente:caso_editar", args=[self.caso.pk])).status_code, 404)

    def test_publicacion_parcial_no_guarda_rubrica(self):
        self.client.force_login(self.docente)
        self.client.post(reverse("clinitensdocente:ficha_rubrica", args=[self.ficha.pk]),
            {"puntajes_json": json.dumps({"3.1.1.I.1": 5}), "accion": "publicar", "version": 0})
        self.ficha.refresh_from_db()
        self.assertEqual(self.ficha.evaluacion_rubrica, {})

    def test_extension_adjunto_se_valida_en_servidor(self):
        form = CasoClinicoForm({"titulo": "Demo", "contenido": "<p>Demo</p>"},
              {"archivos": SimpleUploadedFile("archivo.exe", b"ejecutable")})
        self.assertFalse(form.is_valid())
        self.assertIn("archivos", form.errors)

    def test_matriz_pdf_por_url_directa(self):
        url = reverse("clinitensdocente:ficha_pdf", args=[self.ficha.pk])
        self.assertEqual(self.client.get(url).status_code, 302)
        for user, status in [(self.alumno, 403), (self.otro, 404), (self.docente, 200),
                             (usuario("admin", "ADMIN"), 200), (usuario("root", None, is_superuser=True), 200),
                             (usuario("sin_perfil", None), 403)]:
            with self.subTest(user=user.username):
                self.client.force_login(user)
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)
                if status == 200:
                    self.assertTrue(response.content.startswith(b"%PDF"))

    def test_catalogo_toggles_y_cursos_ajenos_denegados(self):
        self.client.force_login(self.otro)
        self.assertEqual(self.client.post(reverse("clinitensdocente:codigo_cambiar_estado", args=[self.codigo.pk])).status_code, 404)
        curso = Curso.objects.create(nombre="Propio docente", creado_por=self.docente)
        self.assertEqual(self.client.get(reverse("clinitensdocente:curso_detalle", args=[curso.pk])).status_code, 404)
        self.assertNotIn(self.caso, self.client.get(reverse("clinitensdocente:casos")).context["casos"])

    def test_publica_completa_y_borrador_preserva_nota(self):
        full = {key: maximum for key, _, maximum in RUBRICA}
        self.assertEqual(guardar_evaluacion(self.ficha, self.docente, full, "Publicado", "publicar", 0), 1)
        self.ficha.refresh_from_db()
        self.assertEqual(str(self.ficha.calificacion), "7.0")
        self.assertEqual(self.ficha.porcentaje, 100)
        original = self.ficha.evaluacion_rubrica.copy()
        self.assertEqual(guardar_evaluacion(self.ficha, self.docente, {}, "Borrador", "guardar", 1), 1)
        self.ficha.refresh_from_db()
        self.assertEqual(self.ficha.evaluacion_rubrica, original)
        self.assertEqual(self.ficha.retroalimentacion, "Publicado")
        self.assertEqual(self.ficha.borrador_evaluacion["retroalimentacion"], "Borrador")

    def test_rubrica_rechaza_puntajes_invalidos_y_version_obsoleta(self):
        key = RUBRICA[0][0]
        for scores in [{key: "5"}, {key: True}, {key: -1}, {"inventado": 0}]:
            with self.subTest(scores=scores), self.assertRaises(ValidationError):
                guardar_evaluacion(self.ficha, self.docente, scores, "", "guardar", 0)
        self.assertEqual(guardar_evaluacion(self.ficha, self.docente, {}, "Uno", "guardar", 0), 1)
        self.assertEqual(guardar_evaluacion(self.ficha, self.docente, {}, "Obsoleto", "guardar", 0), 0)
        self.ficha.refresh_from_db()
        self.assertEqual(self.ficha.borrador_evaluacion["retroalimentacion"], "Uno")

    def test_metricas_y_en_vivo_no_exponen_alumno_ajeno(self):
        self.alumno.profile.update_last_activity()
        self.client.force_login(self.docente)
        response = self.client.get(reverse("clinitensdocente:codigos"))
        code = list(response.context["codigos"])[0]
        self.assertEqual(code.total_estudiantes, 1)
        self.assertEqual(code.en_linea, 1)
        usuario("ajeno")
        response = self.client.get(reverse("clinitensdocente:en_vivo"), {"codigo": self.codigo.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([r["estudiante"].pk for r in response.context["registros"]], [self.alumno.pk])

    def test_archivos_imagen_validos_y_falsificados(self):
        from PIL import Image
        from .upload_validation import validar_archivo
        content = BytesIO()
        Image.new("RGB", (10, 10), color="blue").save(content, "PNG")
        image = SimpleUploadedFile("valida.png", content.getvalue())
        self.assertIs(validar_archivo(image), image)
        self.assertEqual(image.tell(), 0)
        for name, data in [("falsa.jpg", content.getvalue()), ("falso.pdf", b"HTML"), ("falso.mp4", b"video"), ("archivo.svg", b"<svg/>")]:
            with self.subTest(name=name), self.assertRaises(ValidationError):
                validar_archivo(SimpleUploadedFile(name, data))

    def test_resultados_ocultos_y_habilitados_por_url(self):
        paciente = Paciente.objects.create(rut="11.111.111-1", nombre_completo="Simulado", edad=20,
            sexo="F", fecha_nacimiento="2006-01-01", creado_por=self.docente)
        result = ResultadoDiagnostico.objects.create(paciente=paciente, caso_clinico=self.caso, categoria="LAB",
            nombre_examen="Ficticio", fecha="2026-10-08", hora="10:00", creado_por=self.docente, publicacion="HABILITACION",
            archivo=SimpleUploadedFile("resultado.pdf", b"%PDF-1.4\nficticio"))
        url = result.archivo.url
        self.client.force_login(self.alumno)
        self.assertEqual(self.client.get(url).status_code, 404)
        self.client.force_login(self.otro)
        habilitar = reverse("clinitensdocente:resultado_habilitar", args=[result.pk])
        self.assertEqual(self.client.post(habilitar).status_code, 404)
        self.client.force_login(self.docente)
        self.assertEqual(self.client.post(habilitar).status_code, 302)
        self.client.force_login(self.alumno)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response.close()
        visible = self.client.get(reverse("clinitensficha:caso", args=[self.ficha.pk])).context["resultados"]
        self.assertIn(result, visible)
        result.publicacion = "OCULTO"
        result.save()
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_multimedia_privada_y_contenido_sanitizado(self):
        from core.html import sanitizar_html
        self.assertEqual(sanitizar_html('<p onclick="x()">Texto<script>alert(1)</script></p>'), "<p>Texto</p>")
        self.assertNotIn("javascript", sanitizar_html('<a href="javascript:alert(1)">Link</a>'))
        media = CasoMultimedia.objects.create(caso=self.caso, archivo=SimpleUploadedFile("caso.pdf", b"%PDF-1.4\nFicticio"))
        self.assertEqual(self.client.get(media.archivo.url).status_code, 302)
        self.client.force_login(self.otro)
        self.assertEqual(self.client.get(media.archivo.url).status_code, 404)
        self.client.force_login(self.alumno)
        response = self.client.get(media.archivo.url)
        self.assertEqual(response.status_code, 200)
        response.close()
        self.assertEqual(self.client.get("/media/archivo-sin-vinculo.pdf").status_code, 404)

    def test_avatar_generico_compartido_sin_exponer_archivos_ajenos(self):
        from django.conf import settings
        from PIL import Image
        settings.MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (10, 10), "blue").save(settings.MEDIA_ROOT / "profile.webp")
        self.client.force_login(self.alumno)
        response = self.client.get("/media/profile.webp")
        self.assertEqual(response.status_code, 200)
        response.close()


class ImportacionSeguraTests(TestCase):
    def setUp(self):
        cache.clear()
        self.docente = usuario("docente", "MANAGER")
        self.curso = Curso.objects.create(nombre="Curso ficticio", creado_por=self.docente)
        self.headers = ["username", "email", "first_name", "last_name"]

    def importar(self, rows):
        return importar([self.headers] + rows, self.curso, normalizar_encabezado, lambda: "Temporal-ficticia-123")

    def excel(self, rows):
        book = Workbook()
        for row in [self.headers] + rows:
            book.active.append(row)
        content = BytesIO()
        book.save(content)
        return SimpleUploadedFile("estudiantes.xlsx", content.getvalue())

    def test_nueva_cuenta_atomica_y_cambio_password_obligatorio(self):
        result, credentials = self.importar([["nuevo", "nuevo@example.test", "Ficticio", "Alumno"]])
        self.assertEqual(result["creados"], 1)
        user = User.objects.get(username="nuevo")
        self.assertTrue(user.profile.requiere_cambio_password)
        self.assertIsNotNone(user.profile.password_temporal_expira)
        self.assertTrue(self.curso.estudiantes.filter(pk=user.pk).exists())
        self.assertTrue(user.check_password(credentials[0]["password"]))

    def test_identidad_discordante_no_modifica_cuentas(self):
        uno, dos = usuario("uno"), usuario("dos")
        before = Profile.objects.count()
        result, credentials = self.importar([[uno.username, dos.email, "Ficticio", "Uno"]])
        self.assertEqual(len(result["errores"]), 1)
        self.assertEqual(Profile.objects.count(), before)
        self.assertFalse(self.curso.estudiantes.exists())
        self.assertEqual(credentials, [])

    def test_rechazo_sin_perfil_no_crea_perfil_ni_altera_cargo(self):
        user = usuario("sin_perfil", None)
        before = Profile.objects.count()
        result, _ = self.importar([[user.username, user.email, "Ficticio", "Uno"]])
        self.assertEqual(len(result["errores"]), 1)
        self.assertEqual(Profile.objects.count(), before)
        self.assertEqual(self.docente.profile.position_FK.permission_code, "MANAGER")

    def test_fallo_de_perfil_revierte_usuario_y_matricula(self):
        from unittest.mock import patch
        from django.db import IntegrityError
        with patch("CliniTensDocenteApp.students.Profile.objects.create", side_effect=IntegrityError("ficticio")):
            result, credentials = self.importar([["nuevo", "nuevo@example.test", "Ficticio", "Alumno"]])
        self.assertEqual(len(result["errores"]), 1)
        self.assertEqual(credentials, [])
        self.assertFalse(User.objects.filter(username="nuevo").exists())
        self.assertFalse(self.curso.estudiantes.exists())

    def test_excel_corrupto_y_filas_invalidas(self):
        with self.assertRaises(ValidationError):
            leer_filas(SimpleUploadedFile("corrupto.xlsx", b"Esto no es Excel"))
        result, _ = self.importar([["no valido espacio", "invalido", "Ficticio", "Uno"]])
        self.assertEqual(result["creados"], 0)
        self.assertFalse(User.objects.filter(username="no valido espacio").exists())

    def test_excel_formulas_se_exportan_como_texto(self):
        content = excel_credenciales([{"username": "=1+1", "email": "+formula", "nombre": "@formula", "password": "-formula"}])
        book = load_workbook(BytesIO(content), data_only=False)
        self.assertTrue(all(cell.data_type == "s" for cell in book.active[2]))
        self.assertEqual(book.active["A2"].value, "=1+1")
        book.close()

    def test_exportacion_token_servidor_una_vez_y_sin_password_html(self):
        self.client.force_login(self.docente)
        response = self.client.post(reverse("clinitensdocente:curso_importar_excel", args=[self.curso.pk]),
            {"archivo": self.excel([["nuevo", "nuevo@example.test", "Ficticio", "Alumno"]])})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Temporal-ficticia-123")
        token = response.context["token_credenciales"]
        self.assertTrue(token)
        url = reverse("clinitensdocente:curso_credenciales_excel", args=[self.curso.pk])
        self.assertEqual(self.client.post(url, {"token": "inventado", "credenciales_json": "[]"}).status_code, 400)
        exported = self.client.post(url, {"token": token})
        self.assertEqual(exported.status_code, 200)
        self.assertEqual(self.client.post(url, {"token": token}).status_code, 400)
        book = load_workbook(BytesIO(exported.content))
        user = User.objects.get(username="nuevo")
        self.assertTrue(user.check_password(book.active["D2"].value))
        self.assertNotContains(response, book.active["D2"].value)
        book.close()

    def test_token_caducado_y_sesion_ajena(self):
        self.client.force_login(self.docente)
        response = self.client.post(reverse("clinitensdocente:curso_importar_excel", args=[self.curso.pk]),
            {"archivo": self.excel([["nuevo", "nuevo@example.test", "Ficticio", "Alumno"]])})
        token = response.context["token_credenciales"]
        url = reverse("clinitensdocente:curso_credenciales_excel", args=[self.curso.pk])
        from django.test import Client
        other = Client()
        other.force_login(self.docente)
        self.assertEqual(other.post(url, {"token": token}).status_code, 400)
        cache.delete("credenciales:" + token)
        self.assertEqual(self.client.post(url, {"token": token}).status_code, 400)
