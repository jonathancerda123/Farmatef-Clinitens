from uuid import uuid4

from django import forms
from django.core import signing
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from core.mixins import PermitsPositionMixin
from core.permissions import objetos_del_docente
from .forms import INPUT
from .inventario import inventario_visible
from .models import LoteInventario, Medicamento, MovimientoInventario
from .movimientos import mover_stock


class MovimientoForm(forms.Form):
    lote = forms.ModelChoiceField(queryset=LoteInventario.objects.none())
    sentido = forms.ChoiceField(choices=[("entrada", "Entrada"), ("salida", "Salida")])
    cantidad = forms.IntegerField(min_value=1, max_value=2147483647)
    motivo = forms.ChoiceField(choices=MovimientoInventario.MOTIVOS)
    observacion = forms.CharField(label="Observación", max_length=300, required=False)
    token = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, actor, **kwargs):
        super().__init__(*args, **kwargs)
        self.actor = actor
        self.fields["lote"].queryset = objetos_del_docente(
            LoteInventario.objects.select_related("medicamento"), actor, campo="medicamento__creado_por"
        )
        self.initial["token"] = signing.dumps({"actor": actor.pk, "operacion": str(uuid4())}, salt="movimientos037")
        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT

    def clean_token(self):
        try:
            data = signing.loads(self.cleaned_data["token"], salt="movimientos037", max_age=7200)
            if data["actor"] != self.actor.pk:
                raise ValueError
            return data["operacion"]
        except (signing.BadSignature, ValueError, KeyError):
            raise forms.ValidationError("El formulario caducó. Recarga para registrar el movimiento.")


class FiltroForm(forms.Form):
    medicamento = forms.ModelChoiceField(queryset=Medicamento.objects.none(), required=False)
    lote = forms.CharField(max_length=80, required=False)
    motivo = forms.ChoiceField(choices=[("", "Todos los motivos")] + MovimientoInventario.MOTIVOS, required=False)
    desde = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    hasta = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))


class MovimientosView(PermitsPositionMixin, View):
    def pagina(self, request, form):
        filtro = FiltroForm(request.GET)
        filtro.fields["medicamento"].queryset = inventario_visible(request.user)
        movimientos = objetos_del_docente(
            MovimientoInventario.objects.select_related("lote__medicamento", "actor", "uso__dispensacion"),
            request.user, campo="lote__medicamento__creado_por",
        )
        if filtro.is_valid():
            valores = filtro.cleaned_data
            for campo, consulta in [("medicamento", "lote__medicamento"), ("lote", "lote__numero_lote__icontains"),
                                    ("motivo", "motivo"), ("desde", "creado_en__date__gte"), ("hasta", "creado_en__date__lte")]:
                if valores.get(campo):
                    movimientos = movimientos.filter(**{consulta: valores[campo]})
        else:
            movimientos = movimientos.none()
        params = request.GET.copy()
        params.pop("page", None)
        return render(request, "pages/farmatef/movimientos.html", {
            "form": form, "filtro": filtro, "pagina": Paginator(movimientos, 30).get_page(request.GET.get("page")),
            "parametros": params.urlencode(),
        })

    def get(self, request):
        return self.pagina(request, MovimientoForm(actor=request.user))

    def post(self, request):
        form = MovimientoForm(request.POST, actor=request.user)
        if form.is_valid():
            d = form.cleaned_data
            try:
                mover_stock(request.user, d["lote"].pk, d["sentido"], d["cantidad"], d["motivo"], d["observacion"], d["token"])
            except ValidationError as exc:
                form.add_error(None, exc)
            except IntegrityError:
                form.add_error(None, "La operación ya fue registrada. Recarga el historial antes de reintentar.")
            else:
                messages.success(request, "Movimiento registrado.")
                return redirect("farmatef:movimientos")
        return self.pagina(request, form)


class PrecioForm(forms.ModelForm):
    precio = forms.IntegerField(label="Precio unitario (CLP)", min_value=0, max_value=999999999)

    class Meta:
        model = Medicamento
        fields = ["precio"]


class PrecioView(PermitsPositionMixin, View):
    def pagina(self, request, medicamento_id):
        medicamento = get_object_or_404(inventario_visible(request.user), pk=medicamento_id)
        form = PrecioForm(request.POST if request.method == "POST" else None, instance=medicamento)
        if request.method == "POST" and form.is_valid():
            # Only update the price: never overwrite concurrent product changes.
            Medicamento.objects.filter(pk=medicamento.pk).update(precio=form.cleaned_data["precio"])
            messages.success(request, "Precio actualizado.")
            return redirect("farmatef:inventario")
        return render(request, "pages/farmatef/precio.html", {"form": form, "medicamento": medicamento})

    get = pagina
    post = pagina
