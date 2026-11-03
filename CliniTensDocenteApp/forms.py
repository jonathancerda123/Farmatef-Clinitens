from django import forms
from django.core.exceptions import ValidationError
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import CasoClinico, CodigoActividad, Paciente, ResultadoDiagnostico, Curso
from .validators import normalizar_rut
from pathlib import Path
from core.permissions import objetos_del_docente
from core.html import sanitizar_html
from .upload_validation import validar_archivo


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        if not data:
            return []

        if not isinstance(data, (list, tuple)):
            data = [data]

        return [
            super(MultipleFileField, self).clean(archivo, initial) for archivo in data
        ]


INPUT = "mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-none outline-hidden transition focus:border-brand-600 focus:ring-2 focus:ring-brand-200"


class BaseTailwindForm(forms.ModelForm):
    def __init__(self, *args, actor=None, **kwargs):
        super().__init__(*args, **kwargs)
        for nombre, modelo in [("paciente", Paciente), ("caso_clinico", CasoClinico), ("curso", Curso)]:
            if nombre in self.fields:
                self.fields[nombre].queryset = objetos_del_docente(modelo.objects.all(), actor) if actor else modelo.objects.none()

        for field in self.fields.values():

            # No reemplazar la clase que CKEditor necesita para inicializarse.
            if isinstance(field.widget, CKEditor5Widget):
                clases_actuales = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = (
                    f"{clases_actuales} django_ckeditor_5".strip()
                )
                continue

            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = (
                    "h-4 w-4 rounded border-slate-300 "
                    "text-brand-600 focus:ring-brand-500"
                )
            else:
                field.widget.attrs["class"] = INPUT
                field.widget.attrs.setdefault("placeholder", field.label)


class CasoClinicoForm(BaseTailwindForm):
    archivos = MultipleFileField(
        required=False,
        widget=MultipleFileInput(
            attrs={
                "multiple": True,
                "accept": ".jpg,.jpeg,.png,.webp,.mp4,.mov,.webm,.pdf",
            }
        ),
    )

    class Meta:
        model = CasoClinico
        fields = ["titulo", "contenido"]

        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "maxlength": 150,
                    "placeholder": "Ej.: Crisis asmática en paciente adulto",
                }
            ),
            "contenido": CKEditor5Widget(
                attrs={
                    "class": "django_ckeditor_5",
                },
                config_name="extends",
            ),
        }

    def clean_archivos(self):
        archivos = self.cleaned_data.get("archivos", [])
        for archivo in archivos:
            validar_archivo(archivo)
        return archivos

    def clean_contenido(self):
        return sanitizar_html(self.cleaned_data["contenido"])


class CodigoActividadForm(BaseTailwindForm):
    class Meta:
        model = CodigoActividad
        fields = ["codigo", "caso_clinico", "curso"]
        widgets = {
            "codigo": forms.TextInput(
                attrs={
                    "maxlength": 30,
                    "placeholder": "Ej.: MQ2026-01",
                    "style": "text-transform:uppercase",
                }
            )
        }

    def clean_codigo(self):
        return self.cleaned_data["codigo"].upper().strip()

    def clean(self):
        cleaned = super().clean()
        caso, curso = cleaned.get("caso_clinico"), cleaned.get("curso")
        if caso and curso and caso.creado_por_id != curso.creado_por_id:
            raise ValidationError("El caso y el curso deben pertenecer al mismo docente.")
        return cleaned


class PacienteForm(BaseTailwindForm):
    archivos = MultipleFileField(
        required=False,
        widget=MultipleFileInput(
            attrs={
                "multiple": True,
                "accept": ".jpg,.jpeg,.png,.webp,.mp4,.mov,.webm,.pdf",
            }
        ),
    )

    class Meta:
        model = Paciente
        fields = [
            "rut",
            "nombre_completo",
            "fecha_nacimiento",
            "sexo",
            "edad",
            "ciudad_comuna",
            "centro_atencion",
            "diagnostico_1",
            "diagnostico_2",
            "observaciones",
        ]
        widgets = {
            "rut": forms.TextInput(
                attrs={
                    "placeholder": "Ej.: 12.345.678-9",
                    "data-rut": "true",
                    "maxlength": 12,
                }
            ),
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 4, "maxlength": 1500}),
        }

    def clean_rut(self):
        return normalizar_rut(self.cleaned_data["rut"])

    def clean_archivos(self):
        archivos = self.cleaned_data.get("archivos", [])
        for archivo in archivos:
            validar_archivo(archivo)
        return archivos


class ResultadoDiagnosticoForm(BaseTailwindForm):
    def clean_archivo(self):
        return validar_archivo(self.cleaned_data.get("archivo"))

    def clean(self):
        cleaned = super().clean()
        paciente, caso = cleaned.get("paciente"), cleaned.get("caso_clinico")
        if paciente and caso and paciente.creado_por_id != caso.creado_por_id:
            raise ValidationError("El paciente y el caso deben pertenecer al mismo docente.")
        return cleaned

    class Meta:
        model = ResultadoDiagnostico
        fields = [
            "paciente",
            "caso_clinico",
            "categoria",
            "nombre_examen",
            "fecha",
            "hora",
            "publicacion",
            "archivo",
            "observaciones",
        ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "hora": forms.TimeInput(attrs={"type": "time"}),
            "observaciones": forms.Textarea(attrs={"rows": 4, "maxlength": 2000}),
            "archivo": forms.ClearableFileInput(
                attrs={"accept": ".jpg,.jpeg,.png,.webp,.pdf"}
            ),
        }


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": INPUT,
                    "placeholder": "Ej.: TENS Jornada Diurna 2026",
                    "maxlength": 150,
                }
            )
        }


class ImportarEstudiantesExcelForm(forms.Form):
    archivo = forms.FileField(
        label="Archivo Excel",
        widget=forms.ClearableFileInput(
            attrs={
                "class": INPUT,
                "accept": ".xlsx",
            }
        ),
    )

    def clean_archivo(self):
        archivo = self.cleaned_data["archivo"]

        if Path(archivo.name).suffix.lower() != ".xlsx":
            raise ValidationError(
                "Debes seleccionar un archivo Excel con extensión .xlsx."
            )

        if archivo.size > 5 * 1024 * 1024:
            raise ValidationError("El archivo no puede superar los 5 MB.")

        return archivo
