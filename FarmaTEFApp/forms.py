from django import forms
from django.core.exceptions import ValidationError

from core.permissions import objetos_del_docente
from .models import LoteInventario, Medicamento


INPUT = (
    "mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3 py-2 "
    "text-sm text-slate-900 outline-hidden transition focus:border-brand-600 "
    "focus:ring-2 focus:ring-brand-200"
)


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = [
            "nombre",
            "principio_activo",
            "concentracion",
            "forma_farmaceutica",
            "codigo_barras",
            "stock_minimo",
            "dias_alerta_vencimiento",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"maxlength": 160}),
            "principio_activo": forms.TextInput(attrs={"maxlength": 160}),
            "concentracion": forms.TextInput(attrs={"maxlength": 80}),
            "forma_farmaceutica": forms.TextInput(attrs={"maxlength": 100}),
            "codigo_barras": forms.TextInput(attrs={"maxlength": 64}),
            "stock_minimo": forms.NumberInput(attrs={"min": 0}),
            "dias_alerta_vencimiento": forms.NumberInput(
                attrs={"min": 1, "max": 365}
            ),
        }

    def __init__(self, *args, actor=None, **kwargs):
        self.actor = actor
        super().__init__(*args, **kwargs)
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


class LoteInventarioForm(forms.ModelForm):
    class Meta:
        model = LoteInventario
        fields = ["medicamento", "numero_lote", "vence_el", "unidades"]
        widgets = {
            "numero_lote": forms.TextInput(attrs={"maxlength": 80}),
            "vence_el": forms.DateInput(attrs={"type": "date"}),
            "unidades": forms.NumberInput(attrs={"min": 1}),
        }

    def __init__(self, *args, actor=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["medicamento"].queryset = objetos_del_docente(
            Medicamento.objects.filter(activo=True), actor, campo="creado_por"
        )
        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT

    def clean(self):
        cleaned = super().clean()
        medicamento = cleaned.get("medicamento")
        numero_lote = cleaned.get("numero_lote")
        if medicamento and numero_lote and LoteInventario.objects.filter(
            medicamento=medicamento, numero_lote=numero_lote
        ).exists():
            self.add_error(
                "numero_lote", ValidationError("Ese lote ya existe para el medicamento.")
            )
        return cleaned
