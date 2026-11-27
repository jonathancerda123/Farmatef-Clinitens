"""Persistencia y lectura de la sala. Nunca modifica lotes o dispensaciones."""
import json

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import F, Q, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

from core.permissions import es_administrador, es_docente_de_area
from UsuarioApp.models import AreaDocente
from .geometria_sala import compartimentos, nombre_compartimento, validar_mueble
from .models import Medicamento, MuebleFarmacia, SalaFarmacia, UbicacionMedicamento

CAMPOS_MUEBLE = ("nombre", "tipo", "ancho_cm", "alto_cm", "fondo_cm", "x_cm", "y_cm", "orientacion", "filas", "columnas")


def autorizar_gestion(actor, propietario):
    if not es_docente_de_area(actor, AreaDocente.FARMACIA) or (actor.pk != propietario.pk and not es_administrador(actor)):
        raise PermissionDenied("No puedes configurar esta sala de farmacia.")


def version_entera(valor):
    try:
        if type(valor) is bool or str(int(valor)) != str(valor):
            raise ValueError
        numero = int(valor)
        if not 0 <= numero < 2**31 - 1:
            raise ValueError
        return numero
    except (ValueError, TypeError, OverflowError):
        raise ValidationError("La versión de la sala no es válida. Recarga la página.")


def actualizar_version(sala, version, *, geometria=False):
    consulta = SalaFarmacia.objects.filter(pk=sala.pk, version=version_entera(version))
    if geometria:
        consulta = consulta.filter(plano_bloqueado=False)
    if not consulta.update(version=F("version") + 1, actualizado_en=timezone.now()):
        raise ValidationError("El plano está bloqueado o la sala cambió en otra pestaña. Recarga antes de guardar.")


@transaction.atomic
def guardar_sala(actor, propietario, texto, version):
    autorizar_gestion(actor, propietario)
    if not isinstance(texto, str) or len(texto) > 100000:
        raise ValidationError("La configuración supera el tamaño permitido.")
    try:
        datos = json.loads(texto)
    except (ValueError, TypeError, RecursionError):
        raise ValidationError("No se pudo leer la configuración de sala.")
    if not isinstance(datos, dict) or not isinstance(datos.get("muebles"), list) or len(datos["muebles"]) > 30:
        raise ValidationError("La sala admite como máximo 30 muebles.")
    for campo in ("ancho_cm", "largo_cm"):
        if type(datos.get(campo)) is not int or not 200 <= datos[campo] <= 3000:
            raise ValidationError("Las medidas de la sala deben estar entre 2 y 30 metros.")
    sala, _ = SalaFarmacia.objects.get_or_create(propietario=propietario)
    actualizar_version(sala, version, geometria=True)
    sala.ancho_cm, sala.largo_cm = datos["ancho_cm"], datos["largo_cm"]
    anteriores = {m.pk: m for m in sala.muebles.all()}
    ubicaciones = list(UbicacionMedicamento.objects.filter(mueble__sala=sala))
    vistos, nuevos = set(), []
    for item in datos["muebles"]:
        if not isinstance(item, dict) or type(item.get("id")) is not int or item["id"] == 0 or item["id"] in vistos:
            raise ValidationError("Cada mueble debe tener un identificador distinto.")
        ident = item["id"]
        vistos.add(ident)
        if ident > 0 and ident not in anteriores:
            raise ValidationError("Un mueble no pertenece a esta sala.")
        if not isinstance(item.get("nombre"), str) or not 1 <= len(item["nombre"].strip()) <= 80 or not isinstance(item.get("tipo"), str):
            raise ValidationError("Indica un nombre válido de hasta 80 caracteres para cada mueble.")
        mueble = MuebleFarmacia(sala=sala, **{k: item.get(k) for k in CAMPOS_MUEBLE})
        mueble.nombre = mueble.nombre.strip()
        if ident > 0:
            mueble.pk = ident
        validar_mueble(mueble, sala)
        if any(u.mueble_id == ident and u.compartimento not in compartimentos(mueble) for u in ubicaciones):
            raise ValidationError("Reubica los medicamentos antes de reducir o cambiar los compartimentos de un mueble.")
        nuevos.append(mueble)
    eliminados = set(anteriores) - vistos
    if sum(m.tipo == "entrance" for m in nuevos) > 1:
        raise ValidationError("La sala puede tener una sola zona de entrada.")
    if any(u.mueble_id in eliminados for u in ubicaciones):
        raise ValidationError("Reubica los medicamentos antes de retirar su mueble.")
    sala.save(update_fields=["ancho_cm", "largo_cm"])
    for mueble in nuevos:
        mueble.save()
    sala.muebles.filter(pk__in=eliminados).delete()
    sala.refresh_from_db()
    return sala


@transaction.atomic
def asignar_ubicacion(actor, propietario, medicamento_id, mueble_id, clave, version):
    autorizar_gestion(actor, propietario)
    sala = SalaFarmacia.objects.filter(propietario=propietario).first()
    if not sala:
        raise ValidationError("Guarda primero la sala y sus muebles.")
    actualizar_version(sala, version)
    medicamento = Medicamento.objects.filter(pk=medicamento_id, creado_por=propietario).first()
    if not medicamento:
        raise ValidationError("El medicamento no pertenece a este inventario.")
    if not mueble_id:
        UbicacionMedicamento.objects.filter(medicamento=medicamento).delete()
        return
    mueble = sala.muebles.filter(pk=mueble_id).first()
    if not mueble or clave not in compartimentos(mueble):
        raise ValidationError("Selecciona un mueble y un compartimento de esta sala.")
    if not medicamento.activo:
        raise ValidationError("Activa el medicamento antes de asignar una nueva ubicación.")
    ubicacion = UbicacionMedicamento(medicamento=medicamento, mueble=mueble, compartimento=clave)
    ubicacion.clean()
    UbicacionMedicamento.objects.update_or_create(medicamento=medicamento, defaults={"mueble": mueble, "compartimento": clave})


def datos_sala(propietario, *, docente=False, productos_ids=None):
    sala = SalaFarmacia.objects.filter(propietario=propietario).first() if propietario else None
    muebles = list(sala.muebles.all()) if sala else []
    productos = []
    if propietario:
        medicamentos = Medicamento.objects.filter(creado_por=propietario)
        if not docente:
            medicamentos = medicamentos.filter(activo=True)
        medicamentos = medicamentos.annotate(disponible=Coalesce(Sum("lotes__unidades", filter=Q(lotes__vence_el__gte=timezone.localdate())), 0)).select_related("ubicacion_farmacia__mueble")
        # Selección contextual nunca amplía el inventario autorizado.
        if productos_ids is not None:
            medicamentos = medicamentos.filter(pk__in=productos_ids)
        for m in medicamentos:
            u = getattr(m, "ubicacion_farmacia", None)
            correcta = u and u.mueble.sala_id == getattr(sala, "pk", None) and u.compartimento in compartimentos(u.mueble)
            productos.append({"id": m.pk, "nombre": m.nombre, "concentracion": m.concentracion,
                              "forma": m.forma_farmaceutica, "activo": m.activo, "stock": m.disponible,
                              "mueble_id": u.mueble_id if correcta else None,
                              "compartimento": u.compartimento if correcta else "",
                              "ubicacion": f"{u.mueble.nombre} · {nombre_compartimento(u.compartimento)}" if correcta else "Ubicación pendiente"})
    return {"plano_bloqueado": sala.plano_bloqueado if sala else False, "version": sala.version if sala else 0, "ancho_cm": sala.ancho_cm if sala else 1000,
            "largo_cm": sala.largo_cm if sala else 900, "configurada": sala is not None,
            "muebles": [{"id": m.pk, **{k: getattr(m, k) for k in CAMPOS_MUEBLE},
                         "compartimentos": [{"clave": c, "nombre": nombre_compartimento(c)} for c in compartimentos(m)]} for m in muebles],
            "productos": productos, "docente": docente}


@transaction.atomic
def alternar_candado(actor, propietario, version):
    autorizar_gestion(actor, propietario)
    sala, _ = SalaFarmacia.objects.get_or_create(propietario=propietario)
    actualizar_version(sala, version)
    sala.refresh_from_db()
    sala.plano_bloqueado = not sala.plano_bloqueado
    sala.save(update_fields=["plano_bloqueado"])
