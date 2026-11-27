from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .geometria_sala import TIPOS_MUEBLE, compartimentos, validar_mueble


class SalaFarmacia(models.Model):
    propietario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="sala_farmacia")
    ancho_cm = models.PositiveSmallIntegerField(default=1000, validators=[MinValueValidator(200), MaxValueValidator(3000)])
    largo_cm = models.PositiveSmallIntegerField(default=900, validators=[MinValueValidator(200), MaxValueValidator(3000)])
    plano_bloqueado = models.BooleanField(default=False)
    version = models.PositiveIntegerField(default=0)
    actualizado_en = models.DateTimeField(auto_now=True)


class MuebleFarmacia(models.Model):
    sala = models.ForeignKey(SalaFarmacia, on_delete=models.CASCADE, related_name="muebles")
    nombre = models.CharField(max_length=80)
    tipo = models.CharField(max_length=20, choices=TIPOS_MUEBLE)
    ancho_cm = models.PositiveSmallIntegerField()
    alto_cm = models.PositiveSmallIntegerField()
    fondo_cm = models.PositiveSmallIntegerField()
    x_cm = models.PositiveSmallIntegerField(default=0)
    y_cm = models.PositiveSmallIntegerField(default=0)
    orientacion = models.PositiveSmallIntegerField(default=0)
    filas = models.PositiveSmallIntegerField(default=1)
    columnas = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["pk"]

    def clean(self):
        super().clean()
        if self.sala_id:
            validar_mueble(self, self.sala)


class UbicacionMedicamento(models.Model):
    medicamento = models.OneToOneField("FarmaTEFApp.Medicamento", on_delete=models.PROTECT, related_name="ubicacion_farmacia")
    mueble = models.ForeignKey(MuebleFarmacia, on_delete=models.PROTECT, related_name="ubicaciones")
    compartimento = models.CharField(max_length=12)

    def clean(self):
        super().clean()
        if self.mueble_id and self.medicamento_id:
            if self.mueble.sala.propietario_id != self.medicamento.creado_por_id:
                raise ValidationError("El medicamento y el mueble deben pertenecer al mismo inventario.")
            if self.compartimento not in compartimentos(self.mueble):
                raise ValidationError("El compartimento no existe en este mueble.")
