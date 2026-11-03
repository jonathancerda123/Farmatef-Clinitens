from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from UsuarioApp.models import Profile
from core.permissions import es_administrador, es_docente


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


class FarmaTEFView(LoginRequiredMixin, TemplateView):
    template_name = "pages/farmatef/farmatef.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["puede_gestionar"] = es_docente(self.request.user)
        return context
