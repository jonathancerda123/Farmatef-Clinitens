from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.views.generic import TemplateView

from core.mixins import PermitsPositionMixin
from core.permissions import objetos_del_docente
from .forms import LoteInventarioForm, MedicamentoForm
from .models import LoteInventario, Medicamento


class InventarioView(PermitsPositionMixin, TemplateView):
    template_name = "pages/farmatef/inventario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        medicamentos = objetos_del_docente(
            Medicamento.objects.all(), self.request.user, campo="creado_por"
        ).prefetch_related(
            Prefetch("lotes", queryset=LoteInventario.objects.select_related("medicamento"))
        )
        context.update(
            {
                "medicamentos": medicamentos,
                "form_medicamento": MedicamentoForm(
                    prefix="medicamento", actor=self.request.user
                ),
                "form_lote": LoteInventarioForm(
                    prefix="lote", actor=self.request.user
                ),
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        if "crear_medicamento" in request.POST:
            form = MedicamentoForm(
                request.POST, prefix="medicamento", actor=request.user
            )
            if form.is_valid():
                medicamento = form.save(commit=False)
                medicamento.creado_por = request.user
                medicamento.save()
                messages.success(request, "Medicamento registrado.")
                return redirect("farmatef:inventario")
            return self.render_to_response(
                self.get_context_data(form_medicamento=form)
            )

        if "crear_lote" in request.POST:
            form = LoteInventarioForm(
                request.POST, prefix="lote", actor=request.user
            )
            if form.is_valid():
                lote = form.save(commit=False)
                lote.registrado_por = request.user
                lote.save()
                messages.success(request, "Lote de inventario registrado.")
                return redirect("farmatef:inventario")
            return self.render_to_response(self.get_context_data(form_lote=form))

        messages.error(request, "No se reconoció la operación solicitada.")
        return redirect("farmatef:inventario")
