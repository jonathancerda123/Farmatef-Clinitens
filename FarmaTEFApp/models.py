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
    unidades = models.PositiveIntegerField(validators=[MinValueValidator(1)])
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
                condition=Q(unidades__gt=0),
                name="ft_lote_unidades_gt0",
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
