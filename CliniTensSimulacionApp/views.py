from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views import View
from django.views.generic import FormView, TemplateView
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
from io import BytesIO
import hashlib
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from CliniTensDocenteApp.models import Curso
from core.permissions import cargo, cursos_visibles_para_docente, es_docente
from .forms import (
    BuscarPacienteDAUForm, CasoSimulacionForm, CierreDAUForm, ContenidoDAUDocenteForm,
    ContenidoDiagnosticoDocenteForm, ContenidoLaboratorioDocenteForm, DatosDAUForm,
    ProcedimientoDAUForm, SolicitudLaboratorioForm,
    PacienteEnfermeriaDocenteForm, RegistroEnfermeriaForm,
)
from .models import (
    AtencionDAU, AtencionEnfermeria, CasoSimulacion, EventoKardex, IntentoSimulacion, ProcedimientoDAU,
    SolicitudLaboratorioSimulada,
)
from .preparacion import preparacion_caso, paso_url


def curso_estudiante(request, caso):
    user = request.user
    if not user.is_active or cargo(user) != "RESTRICTED":
        raise PermissionDenied("Esta práctica está disponible para estudiantes inscritos.")
    if not caso.publicado or not caso.curso.estudiantes.filter(pk=user.pk).exists():
        raise Http404("La simulación no está disponible para esta cuenta.")
    return caso


class DocenteMixin(LoginRequiredMixin):
    login_url = "account_login"

    def dispatch(self, request, *args, **kwargs):
        if not es_docente(request.user):
            raise PermissionDenied("Esta sección requiere un perfil docente autorizado.")
        return super().dispatch(request, *args, **kwargs)


class EstudianteMixin(LoginRequiredMixin):
    login_url = "account_login"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_active or cargo(request.user) != "RESTRICTED":
            raise PermissionDenied("Esta práctica está disponible para estudiantes inscritos.")
        return super().dispatch(request, *args, **kwargs)


class DocenteModuloView(DocenteMixin, TemplateView):
    template_name = "pages/clinitens/simulacion/docente_modulo.html"
    modulo = None
    configuracion = {
        "enfermeria": {
            "titulo": "Preparar pacientes de enfermería",
            "descripcion": "Completa el paciente ficticio del caso. Comparte su identidad con DAU, laboratorio y apoyo diagnóstico; los registros de cuidados son independientes.",
            "form_class": PacienteEnfermeriaDocenteForm,
            "seccion": "Paciente simulado para enfermería",
            "clase": "enfermeria",
        },
        "dau": {
            "titulo": "Preparar Atención de urgencia (DAU)",
            "descripcion": "Configura el paciente ficticio SIM y el proceso que completará el estudiante.",
            "form_class": ContenidoDAUDocenteForm,
            "seccion": "Paciente SIM y escenario de atención",
            "clase": "dau",
        },
        "laboratorio": {
            "titulo": "Preparar laboratorio clínico",
            "descripcion": "Prepara órdenes de exámenes, tipo de muestra y tubo para generar etiquetas educativas tubo a tubo.",
            "form_class": ContenidoLaboratorioDocenteForm,
            "seccion": "Órdenes de laboratorio",
            "clase": "laboratorio",
        },
        "diagnostico": {
            "titulo": "Preparar Centro de Apoyo Diagnóstico",
            "descripcion": "Organiza resultados ficticios de laboratorio, imágenes diagnósticas, ECG e informes.",
            "form_class": ContenidoDiagnosticoDocenteForm,
            "seccion": "Resultados del Centro de Apoyo Diagnóstico",
            "clase": "diagnostico",
        },
    }

    def get_modulo(self):
        try:
            return self.configuracion[self.modulo]
        except KeyError as exc:
            raise Http404("Módulo de simulación no encontrado.") from exc

    def get_queryset(self):
        cursos = cursos_visibles_para_docente(Curso.objects.all(), self.request.user)
        queryset = CasoSimulacion.objects.filter(curso__in=cursos).select_related("curso")
        selected = self.request.GET.get("caso")
        if selected is not None:
            if not selected.isdecimal():
                raise Http404("Caso no encontrado.")
            caso = get_object_or_404(queryset, pk=selected)
            return queryset.filter(pk=caso.pk)
        return queryset

    def crear_form(self, caso, data=None):
        form_class = self.get_modulo()["form_class"]
        if self.modulo == "enfermeria":
            return form_class(data, instance=caso, prefix=f"rae-{caso.pk}")
        if self.modulo == "diagnostico":
            return form_class(data, instance=caso)
        return form_class(data, instance=caso)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        modulo = self.get_modulo()
        error_case_id = context.pop("error_case_id", None)
        error_form = context.pop("error_form", None)
        filas = []
        for caso in self.get_queryset():
            filas.append({
                "caso": caso,
                "form": error_form if caso.pk == error_case_id else self.crear_form(caso),
            })
        context.update({
            "modulo": self.modulo,
            "config": modulo,
            "filas": filas,
            "crear_caso_url": reverse("clinitens_simulacion:docente_casos") + "#nuevo-caso",
            "resultados_url": reverse("clinitens_simulacion:docente_resultados"),
        })
        if self.request.GET.get("caso") is not None:
            context["preparacion"] = preparacion_caso(filas[0]["caso"])
        return context

    def post(self, request):
        caso = get_object_or_404(self.get_queryset(), pk=request.POST.get("caso_id"))
        if caso.publicado:
            messages.error(request, "Este caso ya está publicado. Para proteger las prácticas activas, sus contenidos quedan en solo lectura.")
            return redirect(paso_url(caso, self.modulo) if "caso" in request.GET else reverse(f"clinitens_simulacion:docente_{self.modulo}"))
        form = self.crear_form(caso, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Se guardó el contenido de {self.get_modulo()['seccion']} para {caso.titulo}.")
            if "caso" in request.GET:
                progreso = preparacion_caso(caso)
                index = [p["modulo"] for p in progreso["pasos"]].index(self.modulo)
                return redirect(progreso["pasos"][index+1]["url"] if index < 3 else progreso["revision_url"])
            return redirect(f"clinitens_simulacion:docente_{self.modulo}")
        return self.render_to_response(self.get_context_data(
            error_case_id=caso.pk, error_form=form
        ))


class DocenteCasosView(DocenteMixin, FormView):
    template_name = "pages/clinitens/simulacion/docente.html"
    form_class = CasoSimulacionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["actor"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cursos = cursos_visibles_para_docente(Curso.objects.all(), self.request.user)
        context["casos"] = CasoSimulacion.objects.filter(curso__in=cursos).select_related("curso")
        context["preparaciones"] = [preparacion_caso(caso) for caso in context["casos"]]
        return context

    def form_valid(self, form):
        caso = form.save()
        messages.success(self.request, "Caso de simulación guardado como borrador.")
        return redirect(paso_url(caso, "enfermeria"))


class PrepararCasoView(DocenteMixin, TemplateView):
    template_name = "pages/clinitens/simulacion/preparar_caso.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cursos = cursos_visibles_para_docente(Curso.objects.all(), self.request.user)
        caso = get_object_or_404(CasoSimulacion.objects.select_related("curso"), pk=self.kwargs["pk"], curso__in=cursos)
        context["preparacion"] = preparacion_caso(caso)
        return context


class PublicarCasoView(DocenteMixin, View):
    def post(self, request, pk):
        cursos = cursos_visibles_para_docente(Curso.objects.all(), request.user)
        caso = get_object_or_404(CasoSimulacion, pk=pk, curso__in=cursos)
        if not preparacion_caso(caso)["listo"]:
            messages.error(request, "Completa el proceso DAU, al menos una orden de laboratorio y un resultado del Centro de Apoyo Diagnóstico antes de publicar.")
        else:
            caso.publicado = True
            caso.save(update_fields=["publicado", "actualizado_en"])
            messages.success(request, "Caso ficticio publicado para estudiantes inscritos.")
        if request.POST.get("volver_preparacion") == "1":
            return redirect("clinitens_simulacion:preparar_caso", pk=caso.pk)
        return redirect("clinitens_simulacion:docente_casos")


class EstudianteCasosView(EstudianteMixin, TemplateView):
    template_name = "pages/clinitens/simulacion/estudiante.html"

    def get(self, request, *args, **kwargs):
        if kwargs.get("etapa") == "kardex":
            return redirect("clinitens_simulacion:modulo", etapa="diagnostico")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context.get("etapa") and context["etapa"] not in EtapaView.etapas:
            raise Http404("Módulo no encontrado.")
        cursos = Curso.objects.filter(estudiantes=self.request.user)
        casos = CasoSimulacion.objects.filter(curso__in=cursos, publicado=True).select_related("curso")
        context["casos"] = casos
        context["intentos"] = {
            intento.caso_id: intento for intento in IntentoSimulacion.objects.filter(
                estudiante=self.request.user, caso__in=casos
            )
        }
        context["etapa"] = self.kwargs.get("etapa")
        context["titulo_etapa"] = EtapaView.etapas.get(context["etapa"], "Práctica clínica simulada")
        return context


class EtapaView(EstudianteMixin, TemplateView):
    template_name = "pages/clinitens/simulacion/etapa.html"
    etapas = {"dau": "Atención de urgencia (DAU)", "laboratorio": "Laboratorio clínico", "diagnostico": "Centro de Apoyo Diagnóstico"}

    def obtener_caso(self):
        caso = get_object_or_404(CasoSimulacion.objects.select_related("curso"), pk=self.kwargs["pk"])
        return curso_estudiante(self.request, caso)

    def get(self, request, *args, **kwargs):
        if kwargs.get("etapa") == "dau":
            return redirect("clinitens_simulacion:dau_inicio")
        if kwargs.get("etapa") == "kardex":
            return redirect("clinitens_simulacion:etapa", pk=kwargs["pk"], etapa="diagnostico")
        if kwargs.get("etapa") == "laboratorio":
            return redirect("clinitens_simulacion:solicitud_laboratorio", pk=kwargs["pk"])
        return super().get(request, *args, **kwargs)

    def intento(self, caso):
        intento, _ = IntentoSimulacion.objects.get_or_create(caso=caso, estudiante=self.request.user)
        return intento

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        caso = self.obtener_caso()
        etapa = self.kwargs["etapa"]
        if etapa not in self.etapas:
            raise Http404("Etapa no encontrada.")
        intento = self.intento(caso)
        context.update({"caso": caso, "etapa": etapa, "titulo_etapa": self.etapas[etapa], "intento": intento})
        if etapa == "dau":
            context["form"] = DatosDAUForm(initial=intento.datos_dau)
        elif etapa == "laboratorio":
            context["tubos_recolectados"] = intento.tubos_laboratorio or {}
            context["tubos"] = [
                {**tubo, "recolectado": bool(context["tubos_recolectados"].get(tubo["id"], {}).get("recolectado"))}
                for tubo in grupos_tubos(caso)
            ]
            context["etiquetas_url"] = reverse("clinitens_simulacion:etiquetas_laboratorio", kwargs={"pk": caso.pk})
        else:
            revisados = set(intento.documentos_diagnosticos_revisados or [])
            grupos_documentos = [
                (tipo, etiqueta, [
                    {**documento, "revisado": documento.get("id") in revisados}
                    for documento in (caso.documentos_diagnosticos or [])
                    if documento.get("tipo") == tipo
                ])
                for tipo, etiqueta in (
                    ("laboratorio", "Resultados de laboratorio"),
                    ("imagen", "Imágenes diagnósticas"),
                    ("ecg", "Electrocardiogramas (ECG)"),
                    ("informe", "Informes del paciente"),
                )
            ]
            context["documentos_por_tipo"] = [grupo for grupo in grupos_documentos if grupo[2]]
        return context

    def post(self, request, pk, etapa):
        if etapa == "dau":
            return redirect("clinitens_simulacion:dau_inicio")
        caso = self.obtener_caso()
        if etapa not in self.etapas:
            raise Http404("Etapa no encontrada.")
        intento = self.intento(caso)
        if etapa == "dau":
            form = DatosDAUForm(request.POST)
            if form.is_valid():
                intento.datos_dau = form.cleaned_data
                intento.save(update_fields=["datos_dau", "actualizado_en"])
                messages.success(request, "Registro DAU educativo guardado.")
                return redirect("clinitens_simulacion:etapa", pk=pk, etapa=etapa)
        elif etapa == "laboratorio":
            tubos = {item["id"]: item for item in grupos_tubos(caso)}
            tubo_id = request.POST.get("tubo_id", "")
            if not tubo_id or tubo_id not in tubos:
                raise Http404("Tubo de laboratorio no encontrado.")
            avance = dict(intento.tubos_laboratorio or {})
            avance[tubo_id] = {"recolectado": True, "registrado_en": timezone.now().isoformat()}
            intento.tubos_laboratorio = avance
            intento.save(update_fields=["tubos_laboratorio", "actualizado_en"])
            messages.success(request, "Tubo registrado en la simulación. Ya puedes imprimir su etiqueta educativa.")
            return redirect("clinitens_simulacion:etapa", pk=pk, etapa=etapa)
        elif etapa == "diagnostico":
            documento_id = request.POST.get("documento_id", "")
            ids = {item.get("id") for item in (caso.documentos_diagnosticos or [])}
            if not documento_id or documento_id not in ids:
                raise Http404("Resultado diagnóstico no encontrado.")
            revisados = set(intento.documentos_diagnosticos_revisados or [])
            revisados.add(documento_id)
            intento.documentos_diagnosticos_revisados = sorted(revisados)
            intento.save(update_fields=["documentos_diagnosticos_revisados", "actualizado_en"])
            messages.success(request, "Revisión registrada en tu práctica educativa.")
            return redirect("clinitens_simulacion:etapa", pk=pk, etapa=etapa)
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


def grupos_tubos(caso):
    grupos = {}
    for orden in (caso.ordenes_laboratorio or []):
        tubo = str(orden.get("tubo", "")).strip()
        muestra = str(orden.get("muestra", "")).strip()
        examen = str(orden.get("examen", "")).strip()
        if not tubo or not muestra or not examen:
            continue
        clave = f"{muestra.casefold()}|{tubo.casefold()}"
        if clave not in grupos:
            identificador = hashlib.sha256(clave.encode("utf-8")).hexdigest()[:20]
            grupos[clave] = {"id": identificador, "tubo": tubo, "muestra": muestra, "examenes": []}
        grupos[clave]["examenes"].append(examen)
    return list(grupos.values())


class EtiquetasLaboratorioView(EstudianteMixin, TemplateView):
    template_name = "pages/clinitens/simulacion/etiquetas_laboratorio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        caso = get_object_or_404(CasoSimulacion.objects.select_related("curso"), pk=self.kwargs["pk"])
        curso_estudiante(self.request, caso)
        intento = get_object_or_404(IntentoSimulacion, caso=caso, estudiante=self.request.user)
        recolectados = intento.tubos_laboratorio or {}
        context.update({
            "caso": caso,
            "tubos": [tubo for tubo in grupos_tubos(caso) if recolectados.get(tubo["id"], {}).get("recolectado")],
        })
        return context


class LaboratorioSolicitudView(EstudianteMixin, TemplateView):
    template_name = "pages/clinitens/simulacion/laboratorio.html"

    def obtener_caso(self):
        caso = get_object_or_404(CasoSimulacion.objects.select_related("curso"), pk=self.kwargs["pk"])
        return curso_estudiante(self.request, caso)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        caso = self.obtener_caso()
        code = self.request.GET.get("orden")
        orden = None
        if code:
            orden = get_object_or_404(SolicitudLaboratorioSimulada.objects.select_related("caso", "estudiante"), pk=code, caso=caso, estudiante=self.request.user)
        catalogo = caso.ordenes_laboratorio or []
        draft_key = f"laboratorio_draft_{caso.pk}"
        draft = self.request.session.get(draft_key, {})
        paso = kwargs.get("paso") or self.request.GET.get("paso", "paciente")
        if paso not in {"paciente", "examenes", "resumen"}:
            paso = "paciente"
        selected = set(draft.get("examenes", []))
        snapshots = [row for row in catalogo if str(row.get("id")) in selected]
        context.update({
            "caso": caso, "orden": orden, "paso": paso, "draft": draft,
            "funcionario": self.request.user.get_full_name().strip() or self.request.user.get_username(),
            "form": kwargs.get("form") or SolicitudLaboratorioForm(catalogo=catalogo, initial={"examenes": list(selected), "prioridad": draft.get("prioridad", "RUTINA"), "observaciones": draft.get("observaciones", "")}),
            "examenes": snapshots,
            "tubos": grupos_tubos(caso) if not snapshots else grupos_tubos_snapshot(snapshots),
            "historial": SolicitudLaboratorioSimulada.objects.filter(caso=caso, estudiante=self.request.user)[:20],
            "catalogo_json": [{"id": str(row.get("id")), "texto": f"{row.get('examen','')} {row.get('muestra','')} {row.get('tubo','')}"} for row in catalogo],
        })
        return context

    def post(self, request, pk):
        caso = self.obtener_caso()
        paso = request.POST.get("paso", "paciente")
        draft_key = f"laboratorio_draft_{caso.pk}"
        if paso == "paciente":
            return redirect(f"{reverse('clinitens_simulacion:solicitud_laboratorio', kwargs={'pk': pk})}?paso=examenes")
        if paso == "examenes":
            form = SolicitudLaboratorioForm(request.POST, catalogo=caso.ordenes_laboratorio or [])
            if not form.is_valid():
                return self.render_to_response(self.get_context_data(paso="examenes", form=form))
            request.session[draft_key] = {"examenes": form.cleaned_data["examenes"], "prioridad": form.cleaned_data["prioridad"], "observaciones": form.cleaned_data["observaciones"]}
            request.session.modified = True
            return redirect(f"{reverse('clinitens_simulacion:solicitud_laboratorio', kwargs={'pk': pk})}?paso=resumen")
        if paso == "emitir":
            draft = request.session.get(draft_key, {})
            catalog = {str(row.get("id")): row for row in (caso.ordenes_laboratorio or [])}
            ids = draft.get("examenes", [])
            if not ids or len(ids) > 30 or not set(ids).issubset(catalog):
                request.session.pop(draft_key, None)
                messages.error(request, "La selección expiró o cambió. Vuelve a elegir los exámenes.")
                return redirect("clinitens_simulacion:solicitud_laboratorio", pk=pk)
            orden = SolicitudLaboratorioSimulada.objects.create(
                caso=caso, estudiante=request.user,
                examenes=[catalog[item] for item in ids],
                prioridad=draft.get("prioridad", "RUTINA"),
                observaciones=str(draft.get("observaciones", ""))[:1000],
            )
            request.session.pop(draft_key, None)
            messages.success(request, "Orden educativa emitida correctamente.")
            return redirect(f"{reverse('clinitens_simulacion:solicitud_laboratorio', kwargs={'pk': pk})}?orden={orden.pk}")
        return redirect("clinitens_simulacion:solicitud_laboratorio", pk=pk)


class HistorialLaboratorioView(EstudianteMixin, TemplateView):
    template_name = "pages/clinitens/simulacion/historial_laboratorio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        casos = CasoSimulacion.objects.filter(curso__estudiantes=self.request.user, publicado=True)
        context["ordenes"] = SolicitudLaboratorioSimulada.objects.filter(estudiante=self.request.user, caso__in=casos).select_related("caso")[:100]
        return context


def grupos_tubos_snapshot(examenes):
    class Snapshot:
        ordenes_laboratorio = examenes
    return grupos_tubos(Snapshot())


class OrdenLaboratorioPDFView(EstudianteMixin, View):
    def get(self, request, pk):
        orden = get_object_or_404(SolicitudLaboratorioSimulada.objects.select_related("caso"), pk=pk, estudiante=request.user, caso__curso__estudiantes=request.user, caso__publicado=True)
        output = BytesIO()
        doc = SimpleDocTemplate(output, pagesize=A4, title=f"Orden {orden.codigo}")
        styles = getSampleStyleSheet()
        story = [Paragraph("SIMULACIÓN EDUCATIVA · ORDEN DE LABORATORIO", styles["Title"]), Spacer(1, 8*mm),
                 Paragraph(f"Código: {escape(orden.codigo)}", styles["Heading2"]),
                 Paragraph(f"Paciente SIM: {escape(orden.caso.paciente_nombre or 'Paciente de simulación')} · {escape(orden.caso.paciente_codigo)}", styles["Normal"]),
                 Paragraph(f"Operador: {escape(request.user.get_full_name().strip() or request.user.get_username())}", styles["Normal"]),
                 Paragraph(f"Emitida: {timezone.localtime(orden.emitida_en).strftime('%d-%m-%Y %H:%M')} · Prioridad: {escape(orden.get_prioridad_display())}", styles["Normal"]), Spacer(1, 5*mm)]
        rows = [["Examen", "Muestra", "Tubo"]] + [[escape(x.get("examen", "")), escape(x.get("muestra", "")), escape(x.get("tubo", ""))] for x in orden.examenes]
        table = Table(rows, repeatRows=1, colWidths=[85*mm, 55*mm, 35*mm])
        table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#dcebf7")), ("GRID", (0,0), (-1,-1), .4, colors.HexColor("#b8c7d6")), ("VALIGN",(0,0),(-1,-1),"TOP"), ("PADDING",(0,0),(-1,-1),6)]))
        story.extend([table, Spacer(1, 5*mm), Paragraph("Observaciones educativas: " + escape(orden.observaciones or "Sin observaciones"), styles["Normal"])])
        doc.build(story)
        response = HttpResponse(output.getvalue(), content_type="application/pdf")
        disposition = "attachment" if request.GET.get("descargar") == "1" else "inline"
        response["Content-Disposition"] = f'{disposition}; filename="{orden.codigo}.pdf"'
        return response


class EtiquetasOrdenLaboratorioView(EstudianteMixin, TemplateView):
    template_name = "pages/clinitens/simulacion/etiquetas_orden_laboratorio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orden = get_object_or_404(SolicitudLaboratorioSimulada.objects.select_related("caso"), pk=self.kwargs["pk"], estudiante=self.request.user, caso__curso__estudiantes=self.request.user, caso__publicado=True)
        context.update({"orden": orden, "caso": orden.caso, "tubos": grupos_tubos_snapshot(orden.examenes)})
        return context


class DocenteResultadosView(DocenteMixin, TemplateView):
    template_name = "pages/clinitens/simulacion/resultados.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cursos = cursos_visibles_para_docente(Curso.objects.all(), self.request.user)
        casos = CasoSimulacion.objects.filter(curso__in=cursos).select_related("curso")
        context["casos"] = casos
        intentos = list(IntentoSimulacion.objects.filter(caso__in=casos).select_related("caso", "estudiante").prefetch_related("eventos_kardex"))
        for intento in intentos:
            tubos = intento.tubos_laboratorio or {}
            intento.tubos_resumen = [
                f"{tubo['tubo']} · {tubo['muestra']}"
                for tubo in grupos_tubos(intento.caso)
                if tubos.get(tubo["id"], {}).get("recolectado")
            ]
            revisados = set(intento.documentos_diagnosticos_revisados or [])
            intento.documentos_revisados_resumen = [
                doc.get("titulo") for doc in (intento.caso.documentos_diagnosticos or [])
                if doc.get("id") in revisados
            ]
        context["intentos"] = intentos
        return context


def casos_dau_del_alumno(user):
    return CasoSimulacion.objects.filter(
        curso__estudiantes=user, publicado=True
    ).exclude(paciente_codigo="").select_related("curso")


def atenciones_enfermeria_del_alumno(user):
    return AtencionEnfermeria.objects.filter(
        estudiante=user, caso__curso__estudiantes=user, caso__publicado=True,
    ).select_related("caso", "caso__curso")


class EnfermeriaInicioView(EstudianteMixin, FormView):
    template_name = "pages/clinitens/simulacion/enfermeria_inicio.html"
    form_class = BuscarPacienteDAUForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["codigo"].widget.attrs["class"] = "input"
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["casos"] = casos_dau_del_alumno(self.request.user)
        context["funcionario"] = self.request.user.get_full_name().strip() or self.request.user.get_username()
        return context

    def form_valid(self, form):
        caso = casos_dau_del_alumno(self.request.user).filter(
            paciente_codigo__iexact=form.cleaned_data["codigo"],
        ).first()
        if not caso:
            form.add_error("codigo", "No encontramos ese código SIM entre los casos publicados de tus cursos.")
            return self.form_invalid(form)
        atencion, _ = AtencionEnfermeria.objects.get_or_create(
            caso=caso, estudiante=self.request.user, finalizada=False,
        )
        return redirect("clinitens_simulacion:enfermeria_registro", pk=atencion.pk)


class EnfermeriaHistorialView(EstudianteMixin, TemplateView):
    template_name = "pages/clinitens/simulacion/enfermeria_historial.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_obj"] = Paginator(
            atenciones_enfermeria_del_alumno(self.request.user), 20,
        ).get_page(self.request.GET.get("page"))
        return context


class EnfermeriaRegistroView(EstudianteMixin, TemplateView):
    template_name = "pages/clinitens/simulacion/enfermeria_registro.html"

    def get_atencion(self):
        return get_object_or_404(
            atenciones_enfermeria_del_alumno(self.request.user), pk=self.kwargs["pk"],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        atencion = context.get("atencion") or self.get_atencion()
        context.update({
            "atencion": atencion, "caso": atencion.caso,
            "funcionario": self.request.user.get_full_name().strip() or self.request.user.get_username(),
        })
        context.setdefault("form", RegistroEnfermeriaForm(initial={
            "version": atencion.version, "cuidados": atencion.cuidados,
            "observaciones": atencion.observaciones,
        }))
        return context

    def post(self, request, pk):
        atencion = self.get_atencion()
        form = RegistroEnfermeriaForm(request.POST)
        if atencion.finalizada:
            form.add_error(None, "Esta atención ya está finalizada y se conserva en modo lectura. Tus cambios no se guardaron.")
            return self.render_to_response(self.get_context_data(atencion=atencion, form=form, conflicto=True), status=409)
        if not form.is_valid():
            return self.render_to_response(self.get_context_data(atencion=atencion, form=form), status=400)
        data = form.cleaned_data
        finalizada = data["accion"] == "finalizar"
        now = timezone.now()
        updated = atenciones_enfermeria_del_alumno(request.user).filter(
            pk=pk, finalizada=False, version=data["version"],
        ).update(
            cuidados=data["cuidados"], observaciones=data["observaciones"],
            finalizada=finalizada, finalizada_en=now if finalizada else None,
            actualizada_en=now, version=F("version") + 1,
        )
        if not updated:
            form.add_error(None, "El registro cambió en otra pestaña o se finalizó. Tus cambios no se guardaron; copia tu texto y recarga el registro para revisar la versión vigente.")
            return self.render_to_response(self.get_context_data(atencion=atencion, form=form, conflicto=True), status=409)
        messages.success(request, "Atención de enfermería finalizada." if finalizada else "Borrador de enfermería guardado.")
        return redirect("clinitens_simulacion:enfermeria_registro", pk=pk)


def atenciones_dau_del_alumno(user):
    return AtencionDAU.objects.filter(
        estudiante=user, caso__curso__estudiantes=user, caso__publicado=True
    ).select_related("caso", "caso__curso")


class DAUInicioView(EstudianteMixin, FormView):
    template_name = "pages/clinitens/simulacion/dau_inicio.html"
    form_class = BuscarPacienteDAUForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["casos"] = casos_dau_del_alumno(self.request.user)
        context["funcionario"] = self.request.user.get_full_name().strip() or self.request.user.get_username()
        context["historial_url"] = reverse("clinitens_simulacion:dau_historial")
        return context

    def form_valid(self, form):
        caso = casos_dau_del_alumno(self.request.user).filter(
            paciente_codigo__iexact=form.cleaned_data["codigo"]
        ).first()
        if not caso:
            form.add_error("codigo", "No encontramos ese código SIM entre los casos publicados de tus cursos.")
            return self.form_invalid(form)
        atencion = AtencionDAU.objects.filter(
            caso=caso, estudiante=self.request.user, finalizada=False
        ).order_by("-actualizada_en", "-pk").first()
        if not atencion:
            atencion = AtencionDAU.objects.create(caso=caso, estudiante=self.request.user)
        return redirect("clinitens_simulacion:dau_registro", pk=atencion.pk)


class DAUHistorialView(EstudianteMixin, TemplateView):
    template_name = "pages/clinitens/simulacion/dau_historial.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["atenciones"] = atenciones_dau_del_alumno(self.request.user)
        return context


class DAURegistroView(EstudianteMixin, TemplateView):
    template_name = "pages/clinitens/simulacion/dau_registro.html"

    def get_atencion(self):
        return get_object_or_404(
            atenciones_dau_del_alumno(self.request.user), pk=self.kwargs["pk"]
        )

    @staticmethod
    def calcular(signos):
        pas = signos.get("pa_sistolica")
        pad = signos.get("pa_diastolica")
        peso = signos.get("peso")
        talla = signos.get("talla")
        pam = ((Decimal(pas) + Decimal("2") * Decimal(pad)) / Decimal("3")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        ) if pas not in (None, "") and pad not in (None, "") else None
        imc = (Decimal(peso) / ((Decimal(talla) / Decimal("100")) ** 2)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        ) if peso not in (None, "") and talla not in (None, "") else None
        return pam, imc

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        atencion = self.get_atencion()
        signs_form = DatosDAUForm(initial=atencion.signos_vitales)
        cierre_form = CierreDAUForm(initial=atencion.cierre)
        if atencion.finalizada:
            for form in (signs_form, cierre_form):
                for field in form.fields.values():
                    field.disabled = True
        context.update({
            "atencion": atencion,
            "caso": atencion.caso,
            "signos_form": signs_form,
            "cierre_form": cierre_form,
            "procedimiento_form": ProcedimientoDAUForm(),
            "procedimientos": atencion.procedimientos.select_related("registrado_por"),
            "funcionario": self.request.user.get_full_name().strip() or self.request.user.get_username(),
        })
        context["pam"], context["imc"] = self.calcular(atencion.signos_vitales)
        return context

    def post(self, request, pk):
        atencion = self.get_atencion()
        if atencion.finalizada:
            messages.error(request, "Este DAU está cerrado y se conserva en modo lectura.")
            return redirect("clinitens_simulacion:dau_registro", pk=pk)
        action = request.POST.get("action")
        if action == "guardar_signos":
            form = DatosDAUForm(request.POST)
            if form.is_valid():
                signos = {
                    key: str(value) if value is not None else ""
                    for key, value in form.cleaned_data.items()
                }
                pam, imc = self.calcular(signos)
                signos["pam"] = str(pam) if pam is not None else ""
                signos["imc"] = str(imc) if imc is not None else ""
                atencion.signos_vitales = signos
                atencion.save(update_fields=["signos_vitales", "actualizada_en"])
                messages.success(request, "Signos del escenario guardados.")
                return redirect("clinitens_simulacion:dau_registro", pk=pk)
            context = self.get_context_data()
            context["signos_form"] = form
            return self.render_to_response(context)

        if action == "agregar_procedimiento":
            form = ProcedimientoDAUForm(request.POST)
            if form.is_valid():
                ProcedimientoDAU.objects.create(
                    atencion=atencion,
                    registrado_por=request.user,
                    **form.cleaned_data,
                )
                messages.success(request, "Procedimiento agregado al historial educativo.")
                return redirect("clinitens_simulacion:dau_registro", pk=pk)
            context = self.get_context_data()
            context["procedimiento_form"] = form
            return self.render_to_response(context)

        if action in {"guardar_cierre", "finalizar"}:
            form = CierreDAUForm(request.POST)
            if form.is_valid():
                atencion.cierre = form.cleaned_data
                if action == "finalizar":
                    atencion.finalizada = True
                    atencion.finalizada_en = timezone.now()
                atencion.save(update_fields=["cierre", "finalizada", "finalizada_en", "actualizada_en"])
                if atencion.finalizada:
                    messages.success(request, "DAU simulado finalizado y disponible en tu historial.")
                else:
                    messages.success(request, "Borrador de cierre guardado.")
                return redirect("clinitens_simulacion:dau_registro", pk=pk)
            context = self.get_context_data()
            context["cierre_form"] = form
            return self.render_to_response(context)

        raise Http404("Acción no encontrada.")


def descargar_dau_pdf(request, pk):
    if not request.user.is_authenticated:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.get_full_path())
    if not request.user.is_active or cargo(request.user) != "RESTRICTED":
        raise PermissionDenied("Este documento corresponde a la práctica del estudiante.")
    atencion = get_object_or_404(
        atenciones_dau_del_alumno(request.user).filter(finalizada=True), pk=pk
    )
    buffer = BytesIO()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="DAUTitle", parent=styles["Title"], alignment=TA_CENTER, textColor=colors.HexColor("#2367b1"), fontSize=17, leading=21))
    styles.add(ParagraphStyle(name="DAUSection", parent=styles["Heading2"], textColor=colors.HexColor("#2367b1"), fontSize=11, leading=14, spaceBefore=8, spaceAfter=5))
    styles.add(ParagraphStyle(name="DAUSmall", parent=styles["Normal"], fontSize=8, textColor=colors.HexColor("#566b71")))
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=22 * mm, bottomMargin=18 * mm)
    story = [
        Paragraph("DOCUMENTO DE ATENCIÓN DE URGENCIA (DAU)", styles["DAUTitle"]),
        Paragraph("SIMULACIÓN EDUCATIVA — DATOS FICTICIOS", styles["DAUSmall"]),
        Spacer(1, 8 * mm),
        Paragraph("Identificación del paciente", styles["DAUSection"]),
    ]
    case = atencion.caso
    patient_rows = [
        ["Nombre", case.paciente_nombre, "Código SIM", case.paciente_codigo],
        ["Sexo", case.get_paciente_sexo_display(), "Edad", f"{case.paciente_edad} años"],
        ["Nacimiento", case.paciente_fecha_nacimiento.strftime("%d-%m-%Y") if case.paciente_fecha_nacimiento else "—", "Comuna", case.paciente_comuna or "—"],
        ["Antecedentes ficticios", case.paciente_antecedentes or "—", "Funcionario", request.user.get_full_name().strip() or request.user.get_username()],
    ]
    patient_table = Table(patient_rows, colWidths=[27 * mm, 54 * mm, 27 * mm, 54 * mm])
    patient_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#d6e0e6")),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#edf4fa")),
        ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#edf4fa")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.extend([patient_table, Paragraph("Signos vitales", styles["DAUSection"])])
    signs = atencion.signos_vitales
    labels = [
        ("PA Sistólica", "pa_sistolica", "mmHg"), ("PA Diastólica", "pa_diastolica", "mmHg"),
        ("PAM (cálculo)", "pam", "mmHg"), ("FC", "frecuencia_cardiaca", "lpm"),
        ("FR", "frecuencia_respiratoria", "rpm"), ("Temperatura", "temperatura", "°C"),
        ("Saturación O₂", "saturacion_oxigeno", "%"), ("HGT", "hgt", "mg/dL"),
        ("Peso", "peso", "kg"), ("Talla", "talla", "cm"), ("IMC (cálculo)", "imc", "kg/m²"),
    ]
    rows = [["Dato", "Registro", "Dato", "Registro"]]
    pairs = list(zip(labels[::2], labels[1::2] + [("", "", "")]))
    for left, right in pairs:
        left_val = f"{signs.get(left[1], '—')} {left[2]}" if left[1] else "—"
        right_val = f"{signs.get(right[1], '—')} {right[2]}" if right[1] else "—"
        rows.append([left[0], left_val, right[0] or "—", right_val])
    vitals_table = Table(rows, colWidths=[42 * mm, 42 * mm, 42 * mm, 42 * mm])
    vitals_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5eff8")),
        ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#d6e0e6")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.extend([vitals_table, Paragraph("Registro de procedimientos", styles["DAUSection"])])
    procedures = atencion.procedimientos.all()
    procedure_rows = [["Fecha y hora", "Procedimiento", "Observaciones", "Rol simulado"]]
    procedure_rows.extend([
        [p.registrado_en.strftime("%d-%m-%Y %H:%M"), p.procedimiento, p.observaciones or "—", p.get_responsable_display()]
        for p in procedures
    ] or [["—", "Sin procedimientos registrados", "—", "—"]])
    proc_table = Table(procedure_rows, colWidths=[32 * mm, 50 * mm, 47 * mm, 39 * mm], repeatRows=1)
    proc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5eff8")),
        ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#d6e0e6")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.extend([proc_table])
    closure_labels = [
        ("Motivo de consulta", "motivo_consulta"), ("Antecedentes relevantes", "antecedentes_relevantes"),
        ("Evaluación realizada", "evaluacion_realizada"), ("Observaciones", "observaciones"),
        ("Indicaciones educativas de cierre", "indicaciones_alta"),
    ]
    for label, key in closure_labels:
        value = atencion.cierre.get(key) or "—"
        story.extend([Paragraph(label, styles["DAUSection"]), Paragraph(escape(str(value)).replace("\n", "<br/>"), styles["BodyText"])])
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph(
        f"SIMULACIÓN EDUCATIVA — Datos ficticios. Funcionario: {escape(request.user.get_full_name().strip() or request.user.get_username())}. Fecha de cierre: {timezone.localtime(atencion.finalizada_en).strftime('%d-%m-%Y %H:%M')}.",
        styles["DAUSmall"],
    ))

    def footer(canvas, document):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#d6e0e6"))
        canvas.line(18 * mm, 14 * mm, A4[0] - 18 * mm, 14 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#566b71"))
        canvas.drawString(18 * mm, 9 * mm, "DAU simulado · no válido para atención clínica")
        canvas.drawRightString(A4[0] - 18 * mm, 9 * mm, f"Página {document.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    disposition = "inline" if request.GET.get("inline") == "1" else "attachment"
    response["Content-Disposition"] = f'{disposition}; filename="DAU-{case.paciente_codigo}.pdf"'
    return response
