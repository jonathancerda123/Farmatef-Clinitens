from .forms import UserCreateForm, ProfileCreateForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q, Exists, OuterRef
from django.db import transaction
from django.core.exceptions import PermissionDenied
from allauth.account.models import EmailAddress
from django.contrib import messages
from core.mixins import AdministradorMixin
from .models import Profile


class UserListView(AdministradorMixin, ListView):
    model = User
    template_name = "pages/usuarios/usuarios_lista.html"
    context_object_name = "users"
    paginate_by = 9

    def get_queryset(self):
        show_inactive = self.request.GET.get("inactive") == "1"

        queryset = User.objects.filter(is_active=not show_inactive).select_related(
            "profile__position_FK").annotate(email_verificado=Exists(
                EmailAddress.objects.filter(user=OuterRef("pk"), email__iexact=OuterRef("email"), verified=True)
            )).order_by("-id")

        search_query = self.request.GET.get("search")

        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query)
                | Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        verification_users = [(user, user.email_verificado) for user in context["users"]]

        context["verification_users"] = verification_users
        context["placeholder"] = "Buscar por usuario, nombre o apellido"
        context["search_query"] = self.request.GET.get("search", "")
        context["show_inactive"] = self.request.GET.get("inactive") == "1"

        return context


class UserDeactivateView(AdministradorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)

        if user.is_superuser:
            raise PermissionDenied("Esta cuenta está protegida.")

        if user == request.user:
            messages.error(request, "No puedes desactivar tu propio usuario.")
            return redirect("User")

        user.is_active = False
        user.save()

        messages.success(request, "Usuario desactivado correctamente.")
        return redirect("User")


class UserActivateView(AdministradorMixin, View):
    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        if user.is_superuser:
            raise PermissionDenied("Esta cuenta está protegida.")
        user.is_active = True
        user.save()

        messages.success(request, "Usuario activado correctamente.")
        return redirect("User")


class UserCreateView(AdministradorMixin, View):
    template_name = "pages/usuarios/registro_usuario.html"

    def get(self, request, *args, **kwargs):
        user_form = UserCreateForm()
        profile_form = ProfileCreateForm(actor=request.user)

        context = {"user_form": user_form, "profile_form": profile_form}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = UserCreateForm(request.POST)
        profile_form = ProfileCreateForm(request.POST, request.FILES, actor=request.user)

        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = user_form.save()
                profile = profile_form.save(commit=False)
                profile.user_FK = user
                profile.save()
            messages.success(request, "Usuario creado con Éxito.")
            return redirect("Register")

        context = {"user_form": user_form, "profile_form": profile_form}

        return render(request, self.template_name, context)


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = "pages/perfil/perfil.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        profile, _ = Profile.objects.get_or_create(user_FK=user)
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

        context = {"user_form": user_form, "profile_form": profile_form}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        profile, _ = Profile.objects.get_or_create(user_FK=user)
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    user_form.save()
                    profile_form.save()
                messages.success(request, "Perfil actualizado con éxito.")
            except (OSError, ValueError):
                messages.error(request, "Error al guardar la imagen")

            return redirect("Profile")

        context = {"user_form": user_form, "profile_form": profile_form}

        return render(request, self.template_name, context)
