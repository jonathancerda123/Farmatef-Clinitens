from django import forms

from CliniTensDocenteApp.models import CodigoActividad
from django.contrib.auth.models import User
from django.db.models import Q
from core.permissions import es_administrador, cargo


INPUT = "mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-none outline-hidden transition focus:border-brand-600 focus:ring-2 focus:ring-brand-100"


class IngresoFichaForm(forms.Form):
    codigo_actividad = forms.ModelChoiceField(
        queryset=CodigoActividad.objects.none(),
        empty_label="Seleccionar código de actividad",
        label="Código de actividad",
    )
    docente = forms.ModelChoiceField(
        queryset=User.objects.none(),
        empty_label="Seleccionar docente",
        label="Docente",
    )

    def __init__(self, *args, actor=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["codigo_actividad"].queryset = CodigoActividad.objects.filter(
            activo=True
        ).select_related("caso_clinico", "creado_por", "curso")
        if actor is None:
            self.fields["codigo_actividad"].queryset = CodigoActividad.objects.none()
        elif not es_administrador(actor):
            codes = self.fields["codigo_actividad"].queryset
            if cargo(actor) == "MANAGER":
                codes = codes.filter(creado_por=actor)
            else:
                codes = codes.filter(Q(curso__isnull=True) | Q(curso__estudiantes=actor))
            self.fields["codigo_actividad"].queryset = codes.distinct()
        self.fields["docente"].queryset = User.objects.filter(is_active=True, pk__in=self.fields["codigo_actividad"].queryset.values_list("creado_por_id", flat=True)).filter(
            Q(is_superuser=True) | Q(profile__position_FK__permission_code__in=["MANAGER", "ADMIN"])
        ).distinct()
        self.fields["codigo_actividad"].label_from_instance = (
            lambda codigo: f"{codigo.codigo} — {codigo.caso_clinico.titulo}"
        )
        self.fields["docente"].label_from_instance = (
            lambda docente: docente.get_full_name() or docente.username
        )
        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT

    def clean(self):
        cleaned = super().clean()
        codigo, docente = cleaned.get("codigo_actividad"), cleaned.get("docente")
        if codigo and docente and codigo.creado_por_id != docente.pk:
            raise forms.ValidationError("Selecciona al docente responsable del código.")
        if codigo and not codigo.creado_por.is_active:
            raise forms.ValidationError("El docente responsable está desactivado.")
        return cleaned
