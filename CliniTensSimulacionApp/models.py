from django.conf import settings
from django.db import models
from django.utils import timezone
from uuid import uuid4


class CasoSimulacion(models.Model):
    """Contenido ficticio preparado por un docente para un curso."""

    curso = models.ForeignKey(
        "CliniTensDocenteApp.Curso", on_delete=models.PROTECT,
        related_name="casos_simulacion",
    )
    titulo = models.CharField(max_length=150)
    resumen = models.CharField(max_length=500)
    escenario_dau = models.TextField(max_length=5000)
    paciente_codigo = models.CharField(max_length=24, blank=True, db_index=True)
    paciente_nombre = models.CharField(max_length=150, blank=True)
    paciente_sexo = models.CharField(
        max_length=1,
        choices=[("F", "Femenino"), ("M", "Masculino"), ("O", "Otro / no especificado")],
        blank=True,
    )
    paciente_edad = models.PositiveSmallIntegerField(null=True, blank=True)
    paciente_fecha_nacimiento = models.DateField(null=True, blank=True)
    paciente_comuna = models.CharField(max_length=100, blank=True)
    paciente_antecedentes = models.TextField(max_length=1000, blank=True)
    escenario_laboratorio = models.TextField(max_length=5000)
    indicaciones_kardex = models.JSONField(default=list)
    ordenes_laboratorio = models.JSONField(default=list, blank=True)
    documentos_diagnosticos = models.JSONField(default=list, blank=True)
    publicado = models.BooleanField(default=False)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name="casos_simulacion_creados",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado_en"]
        constraints = [models.UniqueConstraint(
            fields=["paciente_codigo"], condition=~models.Q(paciente_codigo=""),
            name="sim_codigo_paciente_no_vacio_unico",
        )]

    def __str__(self):
        return self.titulo


class IntentoSimulacion(models.Model):
    caso = models.ForeignKey(
        CasoSimulacion, on_delete=models.PROTECT, related_name="intentos"
    )
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name="intentos_simulacion",
    )
    datos_dau = models.JSONField(default=dict)
    resultados_laboratorio = models.JSONField(default=dict)
    tubos_laboratorio = models.JSONField(default=dict, blank=True)
    documentos_diagnosticos_revisados = models.JSONField(default=list, blank=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["caso", "estudiante"], name="sim_intento_unico_por_alumno"
        )]
        ordering = ["-actualizado_en"]


class SolicitudLaboratorioSimulada(models.Model):
    """Orden educativa emitida por un estudiante, con catálogo congelado al emitir."""
    caso = models.ForeignKey(CasoSimulacion, on_delete=models.PROTECT, related_name="solicitudes_laboratorio")
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="solicitudes_laboratorio_simuladas")
    codigo = models.CharField(max_length=40, unique=True, editable=False)
    examenes = models.JSONField(default=list)
    prioridad = models.CharField(max_length=12, choices=[("RUTINA", "Rutina"), ("URGENTE", "Urgente"), ("STAT", "Prioritaria (STAT)")], default="RUTINA")
    observaciones = models.CharField(max_length=1000, blank=True)
    emitida_en = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-emitida_en", "-pk"]

    def save(self, *args, **kwargs):
        if not self.codigo:
            from django.utils import timezone as dj_timezone
            self.codigo = f"LAB-SIM-{dj_timezone.localdate():%Y%m%d}-{uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class AtencionDAU(models.Model):
    """Atención individual, exclusivamente ficticia y asociada al alumno autenticado."""

    caso = models.ForeignKey(
        CasoSimulacion, on_delete=models.PROTECT, related_name="atenciones_dau"
    )
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name="atenciones_dau_simuladas",
    )
    signos_vitales = models.JSONField(default=dict, blank=True)
    cierre = models.JSONField(default=dict, blank=True)
    finalizada = models.BooleanField(default=False)
    finalizada_en = models.DateTimeField(null=True, blank=True)
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-actualizada_en", "-pk"]


class AtencionEnfermeria(models.Model):
    """Registro RAE educativo propio, independiente de DAU y Kardex."""

    caso = models.ForeignKey(
        CasoSimulacion, on_delete=models.PROTECT, related_name="atenciones_enfermeria"
    )
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name="atenciones_enfermeria_simuladas",
    )
    cuidados = models.TextField(max_length=5000, blank=True)
    observaciones = models.TextField(max_length=2000, blank=True)
    version = models.PositiveIntegerField(default=1)
    finalizada = models.BooleanField(default=False)
    finalizada_en = models.DateTimeField(null=True, blank=True)
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-actualizada_en", "-pk"]
        constraints = [models.UniqueConstraint(
            fields=["caso", "estudiante"], condition=models.Q(finalizada=False),
            name="sim_rae_un_borrador_por_alumno",
        )]


class ProcedimientoDAU(models.Model):
    class Responsable(models.TextChoices):
        ESTUDIANTE = "ESTUDIANTE", "Estudiante en simulación"
        ENFERMERIA = "ENFERMERIA", "Enfermería (rol simulado)"
        OTRO = "OTRO", "Otro rol simulado"

    atencion = models.ForeignKey(
        AtencionDAU, on_delete=models.PROTECT, related_name="procedimientos"
    )
    procedimiento = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=1000, blank=True)
    responsable = models.CharField(max_length=12, choices=Responsable.choices)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name="procedimientos_dau_simulados",
    )
    registrado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["registrado_en", "pk"]


class EventoKardex(models.Model):
    class Estado(models.TextChoices):
        ADMINISTRADO = "ADMINISTRADO", "Registrado en simulación"
        OMITIDO = "OMITIDO", "Omitido en simulación"

    intento = models.ForeignKey(
        IntentoSimulacion, on_delete=models.PROTECT, related_name="eventos_kardex"
    )
    indice_indicacion = models.PositiveSmallIntegerField()
    estado = models.CharField(max_length=12, choices=Estado.choices)
    observacion = models.CharField(max_length=500, blank=True)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name="eventos_kardex_simulados",
    )
    registrado_en = models.DateTimeField(default=timezone.now)
    corrige_a = models.ForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True,
        related_name="correcciones",
    )

    class Meta:
        ordering = ["registrado_en", "pk"]
        constraints = [models.UniqueConstraint(
            fields=["intento", "indice_indicacion"], condition=models.Q(corrige_a__isnull=True),
            name="sim_kardex_primera_accion_unica",
        ), models.UniqueConstraint(
            fields=["corrige_a"], condition=models.Q(corrige_a__isnull=False),
            name="sim_kardex_una_correccion_por_evento",
        )]

    def __str__(self):
        return f"{self.get_estado_display()} · {self.registrado_en:%Y-%m-%d %H:%M}"
