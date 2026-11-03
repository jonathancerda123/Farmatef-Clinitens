from django.conf import settings
from django.db import models

from CliniTensDocenteApp.models import CodigoActividad


class FichaClinica(models.Model):
    class Estado(models.TextChoices):
        BORRADOR = "BORRADOR", "Borrador"
        ENVIADA = "ENVIADA", "Pendiente de calificación"
        CALIFICADA = "CALIFICADA", "Calificada"

    codigo_actividad = models.ForeignKey(
        CodigoActividad, on_delete=models.PROTECT, related_name="fichas_estudiantes"
    )
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="fichas_clinicas",
    )
    docente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="fichas_a_calificar",
    )
    datos = models.JSONField(default=dict, blank=True)
    version = models.PositiveIntegerField(default=0)
    borrador_evaluacion = models.JSONField(default=dict, blank=True)
    estado = models.CharField(
        max_length=12, choices=Estado.choices, default=Estado.BORRADOR
    )
    enviada_en = models.DateTimeField(null=True, blank=True)
    calificacion = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True
    )
    retroalimentacion = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    evaluacion_rubrica = models.JSONField(default=dict, blank=True)
    puntaje = models.PositiveIntegerField(default=0)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    evaluada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fichas_evaluadas",
    )
    evaluada_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["codigo_actividad", "estudiante"],
                name="ficha_unica_por_estudiante_y_codigo",
            )
        ]
        ordering = ["-actualizado_en"]

    @property
    def bloqueada(self):
        return self.estado in {self.Estado.ENVIADA, self.Estado.CALIFICADA}

    def __str__(self):
        return f"{self.codigo_actividad.codigo} - {self.estudiante.username}"
