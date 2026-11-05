from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from uuid import uuid4
import re
from CliniTensDocenteApp.models import Curso
from core.permissions import cursos_visibles_para_docente
from .models import CasoSimulacion


class SolicitudLaboratorioForm(forms.Form):
    examenes = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple)
    prioridad = forms.ChoiceField(choices=[("RUTINA", "Rutina"), ("URGENTE", "Urgente"), ("STAT", "Prioritaria (STAT)")])
    observaciones = forms.CharField(required=False, max_length=1000, widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Indicaciones educativas u observaciones ficticias"}))

    def __init__(self, *args, catalogo, **kwargs):
        self.catalogo = catalogo
        choices = [(str(row.get("id", "")), f"{row.get('examen', '')} · {row.get('muestra', '')} · {row.get('tubo', '')}") for row in catalogo if row.get("id")]
        super().__init__(*args, **kwargs)
        self.fields["examenes"].choices = choices

    def clean_examenes(self):
        values = self.cleaned_data["examenes"]
        if len(values) > 30:
            raise ValidationError("Selecciona hasta 30 exámenes por solicitud.")
        available = {str(row.get("id")) for row in self.catalogo}
        if not set(values).issubset(available):
            raise ValidationError("La selección contiene exámenes que no están en el catálogo de este caso.")
        return values


class CasoSimulacionForm(forms.ModelForm):
    class Meta:
        model = CasoSimulacion
        fields = ["curso", "titulo", "resumen"]
        widgets = {
            "resumen": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, actor, **kwargs):
        super().__init__(*args, **kwargs)
        self.actor = actor
        self.fields["curso"].queryset = cursos_visibles_para_docente(
            Curso.objects.all(), actor
        )
    def save(self, commit=True):
        caso = super().save(commit=False)
        caso.creado_por = self.actor
        if commit:
            caso.save()
        return caso


class ContenidoDAUDocenteForm(forms.ModelForm):
    class Meta:
        model = CasoSimulacion
        fields = [
            "paciente_codigo", "paciente_nombre", "paciente_sexo", "paciente_edad",
            "paciente_fecha_nacimiento", "paciente_comuna", "paciente_antecedentes",
            "escenario_dau",
        ]
        widgets = {
            "paciente_fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "paciente_antecedentes": forms.Textarea(attrs={"rows": 3}),
            "escenario_dau": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in (
            "paciente_codigo", "paciente_nombre", "paciente_sexo", "paciente_edad",
            "paciente_fecha_nacimiento", "paciente_comuna",
        ):
            self.fields[name].required = True
        self.fields["paciente_codigo"].help_text = "Código inventado, por ejemplo SIM-PAC-001. No uses RUT."
        self.fields["paciente_antecedentes"].help_text = "Escribe solo antecedentes ficticios para este ejercicio."
        self.fields["escenario_dau"].label = "Proceso de atención de urgencia"
        self.fields["escenario_dau"].help_text = "Describe el escenario educativo que verá el estudiante."

    def clean_paciente_codigo(self):
        codigo = self.cleaned_data["paciente_codigo"].strip().upper()
        if not re.fullmatch(r"SIM-[A-Z0-9-]{3,20}", codigo):
            raise ValidationError("Usa un código ficticio que comience con SIM-, por ejemplo SIM-PAC-001.")
        duplicado = CasoSimulacion.objects.filter(paciente_codigo__iexact=codigo).exclude(pk=self.instance.pk)
        if duplicado.exists():
            raise ValidationError("Ese código SIM ya está asignado a otro caso.")
        return codigo

    def clean_paciente_edad(self):
        edad = self.cleaned_data["paciente_edad"]
        if edad is not None and edad > 120:
            raise ValidationError("Ingresa una edad de hasta 120 años para el escenario ficticio.")
        return edad


class ContenidoLaboratorioDocenteForm(forms.ModelForm):
    ordenes = forms.CharField(
        label="Órdenes de exámenes",
        max_length=12000,
        widget=forms.Textarea(attrs={"rows": 7, "placeholder": "Hemograma ficticio | Sangre total | Tubo morado\nPerfil de demostración | Suero | Tubo amarillo"}),
        help_text="Una orden por línea: examen | muestra | tubo. Órdenes del mismo tubo se agrupan en una etiqueta.",
    )

    class Meta:
        model = CasoSimulacion
        fields = ["escenario_laboratorio"]
        widgets = {"escenario_laboratorio": forms.Textarea(attrs={"rows": 6})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["escenario_laboratorio"].label = "Solicitud y contexto de laboratorio"
        self.fields["escenario_laboratorio"].help_text = "Contexto ficticio de la solicitud. No agregues interpretación diagnóstica ni rangos reales."
        self.fields["ordenes"].initial = "\n".join(
            f"{row.get('examen', '')} | {row.get('muestra', '')} | {row.get('tubo', '')}"
            for row in (self.instance.ordenes_laboratorio or [])
        )

    def clean_ordenes(self):
        lines = [line.strip() for line in self.cleaned_data["ordenes"].splitlines() if line.strip()]
        if not 1 <= len(lines) <= 30:
            raise ValidationError("Ingresa entre 1 y 30 órdenes ficticias.")
        previous = list(self.instance.ordenes_laboratorio or [])
        parsed = []
        for index, line in enumerate(lines):
            parts = [part.strip() for part in line.split("|", 2)]
            if len(parts) != 3 or any(not part for part in parts):
                raise ValidationError(f"La línea {index + 1} debe tener examen | muestra | tubo.")
            examen, muestra, tubo = parts
            if any(len(part) > 120 for part in parts):
                raise ValidationError(f"Los campos de la línea {index + 1} no pueden superar 120 caracteres.")
            match = next((
                row for row in previous
                if (row.get("examen", "").casefold(), row.get("muestra", "").casefold(), row.get("tubo", "").casefold())
                == (examen.casefold(), muestra.casefold(), tubo.casefold())
            ), None)
            if match:
                previous.remove(match)
            old_id = match.get("id") if match else None
            parsed.append({"id": old_id or uuid4().hex, "examen": examen, "muestra": muestra, "tubo": tubo})
        return parsed

    def save(self):
        self.instance.escenario_laboratorio = self.cleaned_data["escenario_laboratorio"]
        self.instance.ordenes_laboratorio = self.cleaned_data["ordenes"]
        self.instance.save(update_fields=["escenario_laboratorio", "ordenes_laboratorio", "actualizado_en"])
        return self.instance


class ContenidoDiagnosticoDocenteForm(forms.Form):
    documentos = forms.CharField(
        label="Resultados e informes del Centro de Apoyo Diagnóstico",
        help_text="Una entrada por línea: categoría | título | contenido. Categorías: laboratorio, imagen, ECG, informe.",
        max_length=18000,
        widget=forms.Textarea(attrs={"rows": 9, "placeholder": "laboratorio | Panel de demostración | Resultado ficticio sin interpretación\nimagen | Radiografía simulada | Representación educativa: descripción ficticia\nECG | Trazado de práctica | Registro simulado para revisión\ninforme | Informe de apoyo | Contenido ficticio"}),
    )

    def __init__(self, *args, instance, **kwargs):
        self.instance = instance
        initial = kwargs.pop("initial", {})
        initial.setdefault("documentos", "\n".join(
            f"{row.get('tipo', '')} | {row.get('titulo', '')} | {row.get('contenido', '')}"
            for row in (instance.documentos_diagnosticos or [])
        ))
        super().__init__(*args, initial=initial, **kwargs)

    def clean_documentos(self):
        lines = [line.strip() for line in self.cleaned_data["documentos"].splitlines() if line.strip()]
        if not 1 <= len(lines) <= 30:
            raise ValidationError("Ingresa entre 1 y 30 resultados o informes ficticios.")
        previous = list(self.instance.documentos_diagnosticos or [])
        parsed = []
        allowed = {"laboratorio", "imagen", "ecg", "informe"}
        for index, line in enumerate(lines):
            parts = [part.strip() for part in line.split("|", 2)]
            if len(parts) != 3 or any(not part for part in parts):
                raise ValidationError(f"La línea {index + 1} debe tener categoría | título | contenido.")
            tipo, titulo, contenido = parts
            tipo = tipo.casefold()
            if tipo not in allowed:
                raise ValidationError(f"La categoría de la línea {index + 1} debe ser laboratorio, imagen, ECG o informe.")
            if len(titulo) > 150 or len(contenido) > 1500:
                raise ValidationError(f"El título o contenido de la línea {index + 1} supera el límite permitido.")
            match = next((
                row for row in previous
                if (row.get("tipo", "").casefold(), row.get("titulo", "").casefold(), row.get("contenido", "").casefold())
                == (tipo, titulo.casefold(), contenido.casefold())
            ), None)
            if match:
                previous.remove(match)
            old_id = match.get("id") if match else None
            parsed.append({"id": old_id or uuid4().hex, "tipo": tipo, "titulo": titulo, "contenido": contenido})
        return parsed

    def save(self):
        self.instance.documentos_diagnosticos = self.cleaned_data["documentos"]
        self.instance.save(update_fields=["documentos_diagnosticos", "actualizado_en"])
        return self.instance


class DatosDAUForm(forms.Form):
    pa_sistolica = forms.DecimalField(label="PA Sistólica (mmHg)", required=False, max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("400"))])
    pa_diastolica = forms.DecimalField(label="PA Diastólica (mmHg)", required=False, max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("300"))])
    frecuencia_cardiaca = forms.DecimalField(label="FC (lpm)", required=False, max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("500"))])
    frecuencia_respiratoria = forms.DecimalField(label="FR (rpm)", required=False, max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("200"))])
    temperatura = forms.DecimalField(label="Temperatura (°C)", required=False, max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("60"))])
    saturacion_oxigeno = forms.DecimalField(label="Saturación O₂ (%)", required=False, max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("100"))])
    hgt = forms.DecimalField(label="HGT (mg/dL)", required=False, max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("2000"))])
    peso = forms.DecimalField(label="Peso (kg)", required=False, max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal("0.01")), MaxValueValidator(Decimal("700"))])
    talla = forms.DecimalField(label="Talla (cm)", required=False, max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal("1")), MaxValueValidator(Decimal("300"))])


class BuscarPacienteDAUForm(forms.Form):
    codigo = forms.CharField(
        label="Código ficticio del paciente",
        max_length=24,
        widget=forms.TextInput(attrs={"placeholder": "Ej.: SIM-PAC-001", "autocomplete": "off"}),
    )

    def clean_codigo(self):
        return self.cleaned_data["codigo"].strip().upper()


class ProcedimientoDAUForm(forms.Form):
    procedimiento = forms.CharField(label="Procedimiento realizado", max_length=200, widget=forms.TextInput(attrs={"placeholder": "Ej.: Registro educativo de la atención"}))
    observaciones = forms.CharField(label="Observaciones", required=False, max_length=1000, widget=forms.TextInput(attrs={"placeholder": "Detalles ficticios del procedimiento"}))
    responsable = forms.ChoiceField(label="Profesional responsable", choices=[("ESTUDIANTE", "Estudiante en simulación"), ("ENFERMERIA", "Enfermería (rol simulado)"), ("OTRO", "Otro rol simulado")])


class CierreDAUForm(forms.Form):
    motivo_consulta = forms.CharField(label="Motivo de consulta", max_length=1000, widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Describe el motivo dentro del escenario ficticio"}))
    antecedentes_relevantes = forms.CharField(label="Antecedentes relevantes", required=False, max_length=1500, widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Antecedentes ficticios del escenario"}))
    evaluacion_realizada = forms.CharField(label="Evaluación realizada", max_length=3000, widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Registra lo observado en la simulación"}))
    observaciones = forms.CharField(label="Observaciones", required=False, max_length=1500, widget=forms.Textarea(attrs={"rows": 3}))
    indicaciones_alta = forms.CharField(label="Indicaciones educativas de cierre", required=False, max_length=1500, widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Solo contenido ficticio preparado para esta práctica"}))


class ResultadosLaboratorioForm(forms.Form):
    solicitud = forms.CharField(label="Solicitud ficticia de exámenes", max_length=1000, widget=forms.Textarea(attrs={"rows": 3}))
    resultados = forms.CharField(label="Resultados ficticios y unidades", max_length=3000, required=False, help_text="Un resultado por línea, por ejemplo: Examen de demostración: 12 u. No interpretes clínicamente el valor.", widget=forms.Textarea(attrs={"rows": 5}))

    def clean_resultados(self):
        lines = [line.strip() for line in self.cleaned_data["resultados"].splitlines() if line.strip()]
        if len(lines) > 30 or any(len(line) > 300 for line in lines):
            raise ValidationError("Ingresa hasta 30 resultados ficticios, de máximo 300 caracteres cada uno.")
        return lines


class EventoKardexForm(forms.Form):
    estado = forms.ChoiceField(label="Acción educativa", choices=[("ADMINISTRADO", "Marcar como registrado en la simulación"), ("OMITIDO", "Marcar como omitido en la simulación")])
    observacion = forms.CharField(label="Observación", max_length=500, required=False, widget=forms.Textarea(attrs={"rows": 2}))

    def __init__(self, *args, correccion=False, **kwargs):
        super().__init__(*args, **kwargs)
        if correccion:
            self.fields["observacion"].required = True
            self.fields["observacion"].help_text = "Explica el motivo de esta corrección; el registro anterior se conservará."
