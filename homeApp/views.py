from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse
from UsuarioApp.models import Profile
from core.permissions import cargo, es_administrador, es_docente


class HomeView(LoginRequiredMixin, ListView):
    model = User
    template_name = "pages/index.html"

    def get_queryset(self):
        users = User.objects.filter(last_login__isnull=False).select_related("profile__position_FK")
        if not es_administrador(self.request.user):
            scope = Q(pk=self.request.user.pk)
            if es_docente(self.request.user):
                scope |= Q(cursos_clinitens__creado_por=self.request.user) | Q(fichas_clinicas__docente=self.request.user)
            users = users.filter(scope).distinct()
        return users.order_by("-last_login")[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        recent_activity_cutoff = timezone.now() - timezone.timedelta(minutes=2)

        context["active_users"] = Profile.objects.filter(
            last_activity__gte=recent_activity_cutoff
        ).values_list("user_FK_id", flat=True)

        return context


class CliniTENSView(LoginRequiredMixin, TemplateView):
    template_name = "pages/clinitens/clinitens.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        docente = es_docente(user)
        estudiante = cargo(user) == "RESTRICTED"
        administrador = es_administrador(user)
        modules = [
            {
                "titulo": "Ficha Clínica Electrónica", "icono": "clipboard",
                "publico": "Estudiante",
                "descripcion": "Revisa el caso asignado, completa tu ficha y consulta la evaluación de tu actividad.",
                "url": reverse("clinitensficha:ingreso") if estudiante or docente else None,
                "accion": "Abrir ficha clínica", "restriccion": "Acceso con cuenta de estudiante",
            },
            {
                "titulo": "Registro de Atención de Urgencia", "icono": "urgencia",
                "publico": "DAU",
                "descripcion": "Registra signos vitales, procedimientos y cierre de la atención del paciente simulado.",
                "url": reverse("clinitens_simulacion:docente_dau") if docente else reverse("clinitens_simulacion:dau_inicio") if estudiante else None,
                "accion": "Preparar casos DAU" if docente else "Abrir registro de urgencia",
                "restriccion": "Requiere perfil de estudiante o docente",
            },
            {
                "titulo": "Registro de Atención de Enfermería", "icono": "enfermeria",
                "publico": "RAE",
                "descripcion": "Consulta al paciente simulado y registra cuidados y observaciones en una atención de enfermería.",
                "url": reverse("clinitens_simulacion:docente_enfermeria") if docente else reverse("clinitens_simulacion:enfermeria_inicio") if estudiante else None,
                "accion": "Preparar pacientes de enfermería" if docente else "Abrir registro de enfermería",
                "restriccion": "Requiere perfil de estudiante o docente",
            },
            {
                "titulo": "Laboratorio Clínico", "icono": "laboratorio",
                "publico": "Laboratorio",
                "descripcion": "Prepara solicitudes de exámenes, emite órdenes y obtén etiquetas educativas por tubo.",
                "url": reverse("clinitens_simulacion:docente_laboratorio") if docente else reverse("clinitens_simulacion:modulo", args=["laboratorio"]) if estudiante else None,
                "accion": "Preparar laboratorio" if docente else "Abrir laboratorio clínico",
                "restriccion": "Requiere perfil de estudiante o docente",
            },
            {
                "titulo": "Centro de Apoyo Diagnóstico", "icono": "diagnostico",
                "publico": "Diagnóstico",
                "descripcion": "Consulta resultados ficticios de laboratorio, imágenes diagnósticas, ECG e informes.",
                "url": reverse("clinitens_simulacion:docente_diagnostico") if docente else reverse("clinitens_simulacion:modulo", args=["diagnostico"]) if estudiante else None,
                "accion": "Preparar resultados diagnósticos" if docente else "Abrir apoyo diagnóstico",
                "restriccion": "Requiere perfil de estudiante o docente",
            },
            {
                "titulo": "Perfil Docente", "icono": "course", "publico": "Gestión docente",
                "descripcion": "Organiza cursos, pacientes, casos y códigos de actividad; revisa y evalúa fichas clínicas.",
                "url": reverse("clinitensdocente:dashboard") if docente else None,
                "accion": "Abrir panel docente", "restriccion": "Acceso con perfil docente",
            },
            {
                "titulo": "Perfil Administrador", "icono": "users", "publico": "Administración",
                "descripcion": "Gestiona las cuentas y los accesos de estudiantes y docentes de la plataforma.",
                "url": reverse("User") if administrador else None,
                "accion": "Administrar usuarios", "restriccion": "Acceso con perfil administrador",
            },
        ]
        context.update({"modulos_clinicos": modules, "puede_gestionar": docente})
        return context


class FarmaTEFView(LoginRequiredMixin, TemplateView):
    template_name = "pages/farmatef/farmatef.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["puede_gestionar"] = es_docente(self.request.user)
        return context
