from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from datetime import timedelta

from django.utils import timezone


class Medicamento(models.Model):
    nombre = models.CharField(max_length=160)
    principio_activo = models.CharField(max_length=160, blank=True)
    concentracion = models.CharField(max_length=80, blank=True)
    forma_farmaceutica = models.CharField(max_length=100, blank=True)
    clasificacion = models.CharField(max_length=120, blank=True)
    observaciones = models.CharField(max_length=300, blank=True)
    fuente_documental = models.CharField(max_length=120, blank=True)
    codigo_barras = models.CharField(max_length=64, blank=True)
    stock_minimo = models.PositiveIntegerField(default=0)
    dias_alerta_vencimiento = models.PositiveSmallIntegerField(
        default=90,
        validators=[MinValueValidator(1), MaxValueValidator(365)],
    )
    activo = models.BooleanField(default=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="medicamentos_farmatef",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["creado_por", "nombre"],
                name="ft_med_autor_nombre_uq",
            ),
            models.UniqueConstraint(
                fields=["creado_por", "codigo_barras"],
                condition=~Q(codigo_barras=""),
                name="ft_med_autor_barcode_uq",
            ),
        ]
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"

    @property
    def stock_total(self):
        return sum(lote.unidades for lote in self.lotes.all())

    @property
    def stock_bajo(self):
        return self.stock_total < self.stock_minimo

    @property
    def proximo_a_vencer(self):
        hoy = timezone.localdate()
        limite = hoy + timedelta(days=self.dias_alerta_vencimiento)
        return self.lotes.filter(vence_el__gte=hoy, vence_el__lte=limite).exists()

    @property
    def tiene_vencidos(self):
        return self.lotes.filter(vence_el__lt=timezone.localdate()).exists()

    def __str__(self):
        return self.nombre


class LoteInventario(models.Model):
    medicamento = models.ForeignKey(
        Medicamento,
        on_delete=models.PROTECT,
        related_name="lotes",
    )
    numero_lote = models.CharField(max_length=80)
    vence_el = models.DateField()
    unidades = models.PositiveIntegerField(default=0)
    es_simulado = models.BooleanField(default=False)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="lotes_farmatef_registrados",
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["vence_el", "numero_lote"]
        constraints = [
            models.UniqueConstraint(
                fields=["medicamento", "numero_lote"],
                name="ft_lote_med_numero_uq",
            ),
            models.CheckConstraint(
                condition=Q(unidades__gte=0),
                name="ft_lote_unidades_gte0",
            ),
        ]
        verbose_name = "Lote de inventario"
        verbose_name_plural = "Lotes de inventario"

    @property
    def vencido(self):
        return self.vence_el < timezone.localdate()

    @property
    def vence_pronto(self):
        hoy = timezone.localdate()
        limite = hoy + timedelta(days=self.medicamento.dias_alerta_vencimiento)
        return hoy <= self.vence_el <= limite

    def __str__(self):
        return f"{self.medicamento}: {self.numero_lote}"


class Receta(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        PARCIAL = "PARCIAL", "Parcialmente entregada"
        ENTREGADA = "ENTREGADA", "Entregada"

    numero = models.CharField(max_length=32, unique=True)
    persona_ficticia = models.CharField(max_length=100)
    vence_el = models.DateField()
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.PENDIENTE)
    es_ficticia = models.BooleanField(default=True)
    sospecha_falsificacion = models.BooleanField(default=False)
    motivo_rechazo_esperado = models.CharField(
        max_length=28,
        choices=[
            ("", "Válida: dispensar"),
            ("VENCIDA", "Receta vencida"),
            ("FALSIFICACION", "Sospecha de falsificación"),
            ("DATOS_INCONSISTENTES", "Datos inconsistentes"),
            ("INFORMACION_INCOMPLETA", "Información incompleta"),
        ],
        blank=True,
        default="",
    )
    pista_estudiante = models.CharField(max_length=500, blank=True)
    retroalimentacion_docente = models.TextField(max_length=1200, blank=True)
    curso = models.ForeignKey(
        "CliniTensDocenteApp.Curso",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="recetas_farmatef",
    )
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="recetas_farmatef")
    creado_en = models.DateTimeField(auto_now_add=True)
    entregado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="recetas_farmatef_entregadas")
    entregado_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-creado_en"]
        verbose_name = "Receta simulada"
        verbose_name_plural = "Recetas simuladas"

    def __str__(self):
        return self.numero


class RecetaLinea(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.PROTECT, related_name="lineas")
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT, related_name="lineas_receta")
    unidades = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unidades_entregadas = models.PositiveIntegerField(default=0)

    @property
    def unidades_pendientes(self):
        return self.unidades - self.unidades_entregadas

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["receta", "medicamento"], name="ft_receta_med_uq"),
            models.CheckConstraint(condition=Q(unidades_entregadas__lte=models.F("unidades")), name="ft_receta_entregadas_lte"),
        ]


class Dispensacion(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.PROTECT, related_name="dispensaciones")
    respuesta = models.OneToOneField(
        "RespuestaReceta",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="dispensacion",
    )
    entregado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="dispensaciones_farmatef")
    entregado_en = models.DateTimeField(auto_now_add=True)
    es_simulada = models.BooleanField(default=True)


class RespuestaReceta(models.Model):
    class Decision(models.TextChoices):
        DISPENSAR = "DISPENSAR", "Dispensar receta"
        RECHAZAR = "RECHAZAR", "Rechazar receta"

    class Motivo(models.TextChoices):
        VENCIDA = "VENCIDA", "Receta vencida"
        FALSIFICACION = "FALSIFICACION", "Posible falsificación"
        DATOS_INCONSISTENTES = "DATOS_INCONSISTENTES", "Datos inconsistentes"
        INFORMACION_INCOMPLETA = "INFORMACION_INCOMPLETA", "Información incompleta"
        OTRO = "OTRO", "Otro motivo"

    receta = models.ForeignKey(Receta, on_delete=models.PROTECT, related_name="respuestas_estudiantiles")
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="respuestas_recetas_farmatef")
    decision = models.CharField(max_length=10, choices=Decision.choices)
    motivo_rechazo = models.CharField(max_length=32, choices=Motivo.choices, blank=True)
    correcta = models.BooleanField(default=False)
    explicacion = models.TextField(max_length=1600, blank=True)
    respondida_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["receta", "estudiante"],
                name="ft_respuesta_receta_estudiante_uq",
            ),
        ]


class DispensacionLote(models.Model):
    dispensacion = models.ForeignKey(Dispensacion, on_delete=models.PROTECT, related_name="lotes_usados")
    linea = models.ForeignKey(RecetaLinea, on_delete=models.PROTECT, related_name="lotes_dispensados")
    lote = models.ForeignKey(LoteInventario, on_delete=models.PROTECT, related_name="dispensaciones")
    unidades = models.PositiveIntegerField(validators=[MinValueValidator(1)])
