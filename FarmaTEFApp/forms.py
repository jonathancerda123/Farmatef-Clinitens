from django import forms
from django.forms import formset_factory
from django.core.exceptions import ValidationError
from django.utils import timezone

from core.permissions import cursos_visibles_para_docente, objetos_del_docente
from .codigos_barras import ancho_code128, codigo_para_etiqueta, patron_code128
from .models import LoteInventario, Medicamento, Receta, RespuestaReceta
from CliniTensDocenteApp.models import Curso


INPUT = (
    "mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3 py-2 "
    "text-sm text-slate-900 outline-hidden transition focus:border-brand-600 "
    "focus:ring-2 focus:ring-brand-200"
)


class MedicamentoForm(forms.ModelForm):
    precio = forms.IntegerField(label="Precio unitario (CLP)", min_value=0, max_value=999999999)
    class Meta:
        model = Medicamento
        fields = [
            "nombre",
            "precio",
            "principio_activo",
            "concentracion",
            "forma_farmaceutica",
            "clasificacion",
            "observaciones",
            "codigo_barras",
            "stock_minimo",
            "dias_alerta_vencimiento",
        ]
        labels = {"codigo_barras": "Código de barras"}
        widgets = {
            "nombre": forms.TextInput(attrs={"maxlength": 160}),
            "principio_activo": forms.TextInput(attrs={"maxlength": 160}),
            "concentracion": forms.TextInput(attrs={"maxlength": 80}),
            "forma_farmaceutica": forms.TextInput(attrs={"maxlength": 100}),
            "clasificacion": forms.TextInput(attrs={"maxlength": 120}),
            "observaciones": forms.TextInput(attrs={"maxlength": 300}),
            "codigo_barras": forms.TextInput(attrs={
                "maxlength": 64, "autocomplete": "off", "spellcheck": "false",
                "aria-describedby": "codigo-registro-ayuda codigo-registro-estado",
            }),
            "stock_minimo": forms.NumberInput(attrs={"min": 0, "placeholder": "0"}),
            "dias_alerta_vencimiento": forms.NumberInput(
                attrs={"min": 1, "max": 365}
            ),
        }

    def __init__(self, *args, actor=None, **kwargs):
        self.actor = actor
        super().__init__(*args, **kwargs)
        if self.instance.pk is None:
            self.initial.setdefault("stock_minimo", None)
        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT

    def clean(self):
        cleaned = super().clean()
        nombre = cleaned.get("nombre")
        codigo = cleaned.get("codigo_barras")
        if self.actor and nombre and Medicamento.objects.filter(
            creado_por=self.actor, nombre=nombre
        ).exists():
            self.add_error("nombre", "Ya registraste un medicamento con ese nombre.")
        if self.actor and codigo and Medicamento.objects.filter(
            creado_por=self.actor, codigo_barras=codigo
        ).exists():
            self.add_error("codigo_barras", "Ese código de barras ya está registrado.")
        return cleaned


class LoteInventarioBaseForm(forms.ModelForm):
    def clean(self):
        cleaned = super().clean()
        if self.instance.pk and {"medicamento", "numero_lote"}.isdisjoint(self.changed_data):
            return cleaned

        numero_lote = cleaned.get("numero_lote")
        if not numero_lote:
            return cleaned

        numero_lote = numero_lote.upper()
        cleaned["numero_lote"] = numero_lote
        medicamento = cleaned.get("medicamento")
        if medicamento:
            lotes = medicamento.lotes.exclude(pk=self.instance.pk)
            numeros = lotes.order_by().values_list("numero_lote", flat=True).iterator()
            if any(numero.strip().upper() == numero_lote for numero in numeros):
                self.add_error("numero_lote", "Ese lote ya existe para el medicamento.")
        return cleaned


class LoteInventarioForm(LoteInventarioBaseForm):
    class Meta:
        model = LoteInventario
        fields = ["medicamento", "numero_lote", "vence_el", "unidades"]
        widgets = {
            "numero_lote": forms.TextInput(attrs={"maxlength": 80, "data-numero-lote": ""}),
            "vence_el": forms.DateInput(attrs={"type": "date"}),
            "unidades": forms.NumberInput(attrs={"min": 1, "placeholder": "0"}),
        }

    def __init__(self, *args, actor=None, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk is None:
            self.initial.setdefault("unidades", None)
        self.fields["medicamento"].queryset = objetos_del_docente(
            Medicamento.objects.filter(activo=True), actor, campo="creado_por"
        )
        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT
        self.fields["medicamento"].widget = MedicamentoEtiquetaSelect(
            attrs={"class": INPUT, "data-medicine-accepts-barcode": ""},
            choices=self.fields["medicamento"].choices,
        )


class MedicamentoEtiquetaSelect(forms.Select):
    def __init__(self, attrs=None, choices=()):
        super().__init__({**(attrs or {}), "data-medicamento-search": ""}, choices)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        medicamento = getattr(value, "instance", None)
        if medicamento:
            option["attrs"].update(
                {
                    "data-principio": medicamento.principio_activo,
                    "data-search": " ".join([medicamento.nombre, medicamento.principio_activo, medicamento.concentracion, medicamento.forma_farmaceutica]),
                    "data-concentracion": medicamento.concentracion,
                    "data-forma": medicamento.forma_farmaceutica,
                }
            )
            if "data-medicine-accepts-barcode" in self.attrs:
                option["attrs"]["data-medicine-barcode"] = medicamento.codigo_barras
                option["attrs"]["data-medicine-label-code"] = codigo_para_etiqueta(medicamento)
        return option


class LoteEtiquetaSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        lote = getattr(value, "instance", None)
        if lote:
            option["attrs"].update(
                {
                    "data-medicamento-id": str(lote.medicamento_id),
                    "data-vence": lote.vence_el.strftime("%d/%m/%Y"),
                    "data-stock": str(lote.unidades),
                }
            )
        return option


class EtiquetaLoteForm(forms.Form):
    medicamento = forms.ModelChoiceField(
        queryset=Medicamento.objects.none(), label="Medicamento"
    )
    lote = forms.ModelChoiceField(queryset=LoteInventario.objects.none(), label="Lote")
    ancho_mm = forms.IntegerField(
        min_value=40,
        max_value=150,
        initial=55,
        label="Ancho (mm)",
        widget=forms.NumberInput(attrs={"min": 40, "max": 150, "step": 1, "class": INPUT}),
    )
    alto_mm = forms.IntegerField(
        min_value=30,
        max_value=150,
        initial=44,
        label="Alto (mm)",
        widget=forms.NumberInput(attrs={"min": 30, "max": 150, "step": 1, "class": INPUT}),
    )
    copias = forms.IntegerField(
        min_value=1,
        max_value=100,
        initial=1,
        label="Número de copias",
        widget=forms.NumberInput(attrs={"min": 1, "max": 100, "step": 1, "class": INPUT}),
    )

    def __init__(self, *args, actor=None, lote_dispensado=None, **kwargs):
        super().__init__(*args, **kwargs)
        if lote_dispensado is None:
            medicamentos = objetos_del_docente(
                Medicamento.objects.filter(activo=True), actor, campo="creado_por"
            )
            lotes = LoteInventario.objects.filter(medicamento__in=medicamentos)
        else:
            medicamentos = Medicamento.objects.filter(pk=lote_dispensado.medicamento_id)
            lotes = LoteInventario.objects.filter(pk=lote_dispensado.pk)
            self.initial.update(medicamento=lote_dispensado.medicamento_id, lote=lote_dispensado.pk)
            self.fields["medicamento"].disabled = True
            self.fields["lote"].disabled = True
        self.fields["medicamento"].queryset = medicamentos
        self.fields["medicamento"].widget = MedicamentoEtiquetaSelect(
            attrs={"class": INPUT}
        )
        self.fields["medicamento"].widget.choices = self.fields["medicamento"].choices
        self.fields["lote"].queryset = lotes.select_related("medicamento")
        self.fields["lote"].label_from_instance = lambda lote: (
            f"{lote.numero_lote} · Vence {lote.vence_el:%d/%m/%Y} · "
            f"Stock: {lote.unidades}"
        )
        self.fields["lote"].widget = LoteEtiquetaSelect(attrs={"class": INPUT})
        self.fields["lote"].widget.choices = self.fields["lote"].choices

    def clean(self):
        cleaned = super().clean()
        medicamento = cleaned.get("medicamento")
        lote = cleaned.get("lote")
        if medicamento and lote and lote.medicamento_id != medicamento.pk:
            self.add_error("lote", "Selecciona un lote del medicamento elegido.")
        ancho = cleaned.get("ancho_mm")
        if medicamento and ancho is not None:
            codigo = codigo_para_etiqueta(medicamento)
            patron = patron_code128(codigo)
            ancho_codigo = ancho_code128(patron)
            minimo = ancho_codigo + 5
            if ancho < minimo:
                self.add_error("ancho_mm", f"Usa al menos {minimo} mm de ancho para imprimir este código de barras.")
            else:
                cleaned.update(codigo=codigo, patron_codigo=patron, ancho_codigo=ancho_codigo)
        return cleaned


class RecetaForm(forms.Form):
    numero = forms.CharField(max_length=32, label="Número único de receta", widget=forms.TextInput(attrs={"class": INPUT}))
    persona_ficticia = forms.CharField(max_length=100, label="Alias ficticio de la persona", widget=forms.TextInput(attrs={"class": INPUT}))
    vence_el = forms.DateField(label="Válida hasta", widget=forms.DateInput(attrs={"type": "date", "class": INPUT}))
    curso = forms.ModelChoiceField(queryset=Curso.objects.none(), label="Curso asignado")
    motivo_rechazo_esperado = forms.ChoiceField(
        required=False,
        label="Clave docente (no visible al alumno)",
        choices=Receta._meta.get_field("motivo_rechazo_esperado").choices,
    )
    pista_estudiante = forms.CharField(
        required=False, max_length=500, label="Pista que verá el alumno",
        widget=forms.Textarea(attrs={"class": INPUT, "rows": 3}),
    )
    retroalimentacion_docente = forms.CharField(
        required=False, max_length=1200, label="Explicación después de responder",
        widget=forms.Textarea(attrs={"class": INPUT, "rows": 3}),
    )

    def __init__(self, *args, actor=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["curso"].queryset = cursos_visibles_para_docente(
            Curso.objects.all(), actor
        )
        if not self.fields["curso"].queryset.exists():
            self.fields["curso"].help_text = (
                "Primero crea un curso e inscribe estudiantes para asignar casos de práctica."
            )
        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT

    def clean_numero(self):
        value = self.cleaned_data["numero"].strip().upper()
        if Receta.objects.filter(numero=value).exists():
            raise forms.ValidationError("Ese número de receta ya existe.")
        return value

    def clean(self):
        cleaned = super().clean()
        expiry = cleaned.get("vence_el")
        expected = cleaned.get("motivo_rechazo_esperado") or ""
        hint = cleaned.get("pista_estudiante", "").strip()
        feedback = cleaned.get("retroalimentacion_docente", "").strip()
        expired = expiry is not None and expiry < timezone.localdate()

        if expired and expected != "VENCIDA":
            self.add_error("motivo_rechazo_esperado", "Una receta vencida debe evaluarse con el motivo “Receta vencida”.")
        elif not expired and expected == "VENCIDA":
            self.add_error("vence_el", "Para practicar el rechazo por vencimiento, la fecha debe estar vencida.")
        if expected and (not hint or not feedback):
            self.add_error("pista_estudiante", "Añade una pista visible y una explicación para el alumno.")
            self.add_error("retroalimentacion_docente", "Añade la explicación que se mostrará después de responder.")
        return cleaned


class RecetaLineaForm(forms.Form):
    medicamento = forms.ModelChoiceField(queryset=Medicamento.objects.none(), required=False, label="Medicamento")
    unidades = forms.IntegerField(required=False, min_value=1, label="Unidades")
    dosis = forms.CharField(required=False, max_length=60, label="Dosis ficticia")
    indicaciones = forms.CharField(required=False, max_length=160, label="Indicaciones ficticias")

    def __init__(self, *args, actor=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["medicamento"].queryset = objetos_del_docente(
            Medicamento.objects.filter(activo=True), actor, campo="creado_por"
        )
        self.fields["medicamento"].widget = MedicamentoEtiquetaSelect(attrs={"class": INPUT}, choices=self.fields["medicamento"].choices)
        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT

    def clean(self):
        cleaned = super().clean()
        medicine, units = cleaned.get("medicamento"), cleaned.get("unidades")
        if bool(medicine) != bool(units):
            raise forms.ValidationError("Selecciona medicamento y unidades en cada línea utilizada.")
        if not medicine and (cleaned.get("dosis") or cleaned.get("indicaciones")):
            self.add_error("medicamento", "Selecciona el medicamento al que corresponden las indicaciones.")
        return cleaned


class BaseRecetaLineaFormSet(forms.BaseFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        used = [form.cleaned_data["medicamento"] for form in self.forms if form.cleaned_data.get("medicamento")]
        if not used:
            raise forms.ValidationError("Añade al menos un medicamento.")
        if len(used) != len(set(m.pk for m in used)):
            raise forms.ValidationError("Cada medicamento debe aparecer una sola vez en la receta.")


RecetaLineaFormSet = formset_factory(
    RecetaLineaForm, formset=BaseRecetaLineaFormSet, extra=3, max_num=10, validate_max=True
)


class EntregaLineaForm(forms.Form):
    linea_id = forms.IntegerField(widget=forms.HiddenInput)
    entregar = forms.BooleanField(required=False, label="Entregar este medicamento")
    unidades = forms.IntegerField(min_value=0, label="Unidades en esta ocasión")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["entregar"].widget.attrs["class"] = "h-4 w-4 rounded border-slate-300 text-brand-700 focus:ring-brand-600"
        self.fields["unidades"].widget.attrs.update({"min": 0, "class": INPUT})

    def clean(self):
        cleaned = super().clean()
        if not cleaned:
            return cleaned
        if not cleaned.get("entregar"):
            cleaned["unidades"] = 0
        elif not cleaned.get("unidades"):
            self.add_error("unidades", "Indica cuántas unidades de este medicamento se entregarán.")
        return cleaned


class BaseEntregaLineaFormSet(forms.BaseFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        ids = [form.cleaned_data["linea_id"] for form in self.forms]
        if len(ids) != len(set(ids)):
            raise forms.ValidationError("Hay líneas de receta repetidas en la solicitud.")
        if not any(form.cleaned_data["unidades"] for form in self.forms):
            raise forms.ValidationError("Indica al menos una unidad para entregar.")


EntregaLineaFormSet = formset_factory(
    EntregaLineaForm, formset=BaseEntregaLineaFormSet, extra=0, max_num=10, validate_max=True
)


class LotePracticaSelect(forms.Select):
    @staticmethod
    def titulo(lote):
        medicamento = lote.medicamento
        return " · ".join(filter(None, (
            medicamento.nombre, medicamento.concentracion, medicamento.forma_farmaceutica,
        )))

    @staticmethod
    def detalle(lote):
        medicamento = lote.medicamento
        datos = [
            f"Lote {lote.numero_lote}",
            f"Vence {lote.vence_el:%d/%m/%Y}",
            f"{lote.unidades} unidades disponibles",
        ]
        if medicamento.principio_activo and medicamento.principio_activo.casefold() != medicamento.nombre.casefold():
            datos.insert(0, medicamento.principio_activo)
        return " · ".join(datos)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        lote = getattr(value, "instance", None)
        if lote is not None:
            option["attrs"]["data-medicine-title"] = self.titulo(lote)
            option["attrs"]["data-medicine-detail"] = self.detalle(lote)
            option["attrs"]["data-medicine-barcode"] = lote.medicamento.codigo_barras
            option["attrs"]["data-medicine-label-code"] = codigo_para_etiqueta(lote.medicamento)
        return option


class RespuestaRecetaForm(forms.Form):
    intento = forms.IntegerField(min_value=1, max_value=2, initial=1, required=False, widget=forms.HiddenInput)
    decision = forms.ChoiceField(
        choices=RespuestaReceta.Decision.choices,
        widget=forms.RadioSelect,
        label="¿Qué harías con esta receta?",
    )
    motivo_rechazo = forms.ChoiceField(
        choices=[("", "Selecciona un motivo"), *RespuestaReceta.Motivo.choices],
        required=False,
        label="Motivo del rechazo",
    )
    explicacion_otro_motivo = forms.CharField(
        required=False,
        label="Explica brevemente el motivo",
        widget=forms.Textarea(attrs={
            "class": INPUT, "rows": 3, "maxlength": RespuestaReceta.LIMITE_EXPLICACION_OTRO,
        }),
    )

    def __init__(self, *args, receta, lotes, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["motivo_rechazo"].widget.attrs["class"] = INPUT
        self.campos_lotes = {}
        self.lineas = list(receta.lineas.all())
        for numero, linea in enumerate(self.lineas, 1):
            nombre = f"lote_{linea.pk}"
            self.fields[nombre] = forms.ModelChoiceField(
                queryset=lotes,
                required=False,
                label=f"Producto y lote para la línea {numero}",
                widget=LotePracticaSelect(attrs={
                    "class": INPUT, "data-medicamento-search": "", "data-medicine-accepts-barcode": "",
                    "aria-describedby": f"indicacion-{linea.pk}",
                }),
            )
            self.fields[nombre].label_from_instance = self.descripcion_lote
            self.campos_lotes[linea.pk] = nombre

    @staticmethod
    def descripcion_lote(lote):
        return f"{LotePracticaSelect.titulo(lote)} · {LotePracticaSelect.detalle(lote)}"

    @property
    def seleccion_lotes(self):
        return [(linea, self[self.campos_lotes[linea.pk]]) for linea in self.lineas]

    def clean(self):
        cleaned = super().clean()
        if (
            cleaned.get("decision") == RespuestaReceta.Decision.RECHAZAR
            and not cleaned.get("motivo_rechazo")
        ):
            self.add_error("motivo_rechazo", "Selecciona el motivo por el que rechazas la receta.")
        if "explicacion_otro_motivo" in cleaned:
            try:
                cleaned["explicacion_otro_motivo"] = RespuestaReceta.limpiar_explicacion_otro(
                    cleaned.get("decision"), cleaned.get("motivo_rechazo"), cleaned["explicacion_otro_motivo"],
                )
            except ValidationError as exc:
                self.add_error("explicacion_otro_motivo", exc)
        if cleaned.get("decision") == RespuestaReceta.Decision.DISPENSAR:
            cleaned["motivo_rechazo"] = ""
            for nombre in self.campos_lotes.values():
                if not cleaned.get(nombre) and nombre not in self.errors:
                    self.add_error(nombre, "Selecciona el producto y lote de esta línea.")
        return cleaned
