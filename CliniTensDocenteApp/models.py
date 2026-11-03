from django.conf import settings
from django.core.validators import (
    FileExtensionValidator,
    MaxLengthValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import MinValueValidator, MaxValueValidator
from .validators import normalizar_rut, validar_rut
from .upload_validation import validar_archivo_nuevo
from core.html import sanitizar_html


ARCHIVOS_CLINICOS = FileExtensionValidator(
    allowed_extensions=["jpg", "jpeg", "png", "webp", "mp4", "mov", "webm", "pdf"]
)


class CasoClinico(models.Model):
    titulo = models.CharField(max_length=150)

    contenido = CKEditor5Field("Contenido del caso clínico", config_name="default")

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="casos_clinicos",
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    @property
    def imagen_principal(self):
        extensiones_imagen = (".jpg", ".jpeg", ".png", ".webp")

        for multimedia in self.archivos.all():
            if multimedia.archivo.name.lower().endswith(extensiones_imagen):
                return multimedia

        return None

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        self.contenido = sanitizar_html(self.contenido)
        super().save(*args, **kwargs)


class CasoMultimedia(models.Model):
    caso = models.ForeignKey(
        CasoClinico, on_delete=models.CASCADE, related_name="archivos"
    )
    archivo = models.FileField(
        upload_to="clinitens/casos/%Y/%m/", validators=[ARCHIVOS_CLINICOS, validar_archivo_nuevo]
    )
    subido_en = models.DateTimeField(auto_now_add=True)


class CodigoActividad(models.Model):
    codigo = models.CharField(
        max_length=30, unique=True, validators=[MaxLengthValidator(30)]
    )
    caso_clinico = models.ForeignKey(
        CasoClinico, on_delete=models.PROTECT, related_name="codigos"
    )
    activo = models.BooleanField(default=False)
    curso = models.ForeignKey("Curso", on_delete=models.PROTECT,
                              null=True, blank=True, related_name="actividades")
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="codigos_actividad",
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]

    def __str__(self):
        return self.codigo


class Paciente(models.Model):
    class Sexo(models.TextChoices):
        FEMENINO = "F", "Mujer"
        MASCULINO = "M", "Hombre"
        OTRO = "O", "Otro / no especificado"

    rut = models.CharField(max_length=12, unique=True, validators=[validar_rut])
    nombre_completo = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=Sexo.choices)
    edad = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(120),
        ]
    )
    ciudad_comuna = models.CharField(max_length=100, blank=True)
    centro_atencion = models.CharField(max_length=150, blank=True)
    diagnostico_1 = models.CharField(max_length=120, blank=True)
    diagnostico_2 = models.CharField(max_length=120, blank=True)
    observaciones = models.TextField(max_length=1500, blank=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="pacientes_clinitens",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre_completo"]

    def save(self, *args, **kwargs):
        self.rut = normalizar_rut(self.rut)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_completo} ({self.rut})"


class PacienteMultimedia(models.Model):
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="archivos"
    )
    archivo = models.FileField(
        upload_to="clinitens/pacientes/%Y/%m/", validators=[ARCHIVOS_CLINICOS, validar_archivo_nuevo]
    )
    subido_en = models.DateTimeField(auto_now_add=True)


class ResultadoDiagnostico(models.Model):
    class Categoria(models.TextChoices):
        LABORATORIO = "LAB", "Resultados de laboratorio"
        IMAGEN = "IMG", "Imágenes diagnósticas"
        ECG = "ECG", "ECG"
        INFORME = "INF", "Informe clínico"

    class Publicacion(models.TextChoices):
        INICIO = "INICIO", "Disponible al iniciar el caso"
        OCULTO = "OCULTO", "Oculto"
        HABILITACION_DOCENTE = (
            "HABILITACION",
            "Disponible cuando el docente lo habilite",
        )

    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="resultados"
    )
    caso_clinico = models.ForeignKey(
        CasoClinico,
        on_delete=models.SET_NULL,
        related_name="resultados",
        null=True,
        blank=True,
    )
    categoria = models.CharField(max_length=3, choices=Categoria.choices)
    nombre_examen = models.CharField(max_length=180)
    fecha = models.DateField()
    hora = models.TimeField()
    publicacion = models.CharField(
        max_length=20, choices=Publicacion.choices, default=Publicacion.INICIO
    )
    habilitado = models.BooleanField(default=False)
    archivo = models.FileField(
        upload_to="clinitens/resultados/%Y/%m/",
        validators=[ARCHIVOS_CLINICOS, validar_archivo_nuevo],
        blank=True,
    )
    observaciones = models.TextField(max_length=2000, blank=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="resultados_diagnosticos",
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha", "-hora"]

    def __str__(self):
        return self.nombre_examen


class Curso(models.Model):
    nombre = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nombre del curso",
    )

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cursos_clinitens_creados",
    )

    estudiantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="cursos_clinitens",
        blank=True,
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.nombre
