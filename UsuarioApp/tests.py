from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from core.test_helpers import usuario
from .forms import ProfileCreateForm


class ProteccionCuentasTests(TestCase):
    def setUp(self):
        self.admin = usuario("admin", "ADMIN")
        self.docente = usuario("docente", "MANAGER")
        self.estudiante = usuario("estudiante")
        self.root = usuario("root", None, is_superuser=True, is_staff=True)

    def test_estudiante_no_lista_cuentas(self):
        self.client.force_login(self.estudiante)
        self.assertEqual(self.client.get(reverse("User")).status_code, 403)

    def test_admin_no_activa_superusuario(self):
        self.root.is_active = False
        self.root.save(update_fields=["is_active"])
        self.client.force_login(self.admin)
        self.assertEqual(self.client.post(reverse("UserActivate", args=[self.root.pk])).status_code, 403)
        self.root.refresh_from_db()
        self.assertFalse(self.root.is_active)

    def test_cargo_no_depende_de_pk(self):
        form = ProfileCreateForm(actor=self.admin)
        self.assertIn(self.estudiante.profile.position_FK,
                      form.fields["position_FK"].queryset)
        self.assertNotIn(self.admin.profile.position_FK,
                         form.fields["position_FK"].queryset)

    def test_actividad_no_procesa_imagen(self):
        with patch("UsuarioApp.models.resize_image") as resize, patch("UsuarioApp.models.os.path.exists", return_value=True):
            self.estudiante.profile.update_last_activity()
        resize.assert_not_called()

    def test_manager_no_administra_cuentas(self):
        self.client.force_login(self.docente)
        for route in ["User", "Register"]:
            self.assertEqual(self.client.get(reverse(route)).status_code, 403)
        self.assertEqual(self.client.post(reverse("UserDeactivate", args=[self.estudiante.pk])).status_code, 403)

    def test_admin_no_desactiva_super(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.post(reverse("UserDeactivate", args=[self.root.pk])).status_code, 403)
        self.root.refresh_from_db()
        self.assertTrue(self.root.is_active)

    def test_admin_django_protege_otro_super(self):
        from django.test import RequestFactory
        from django.contrib import admin
        from django.contrib.auth.models import User
        request = RequestFactory().get("/admin/")
        request.user = usuario("otro_root", None, is_superuser=True, is_staff=True)
        model_admin = admin.site._registry[User]
        self.assertFalse(model_admin.has_change_permission(request, self.root))
        self.assertFalse(model_admin.has_delete_permission(request, self.root))
        request.user = self.admin
        self.assertFalse(model_admin.has_change_permission(request, self.root))

    def test_anonimo_e_inactivo_no_listan(self):
        self.assertEqual(self.client.get(reverse("User")).status_code, 302)
        self.admin.is_active = False
        self.admin.save()
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse("User")).status_code, 302)

    def test_lista_no_hace_consultas_por_usuario(self):
        from django.test import RequestFactory
        from .views import UserListView
        request = RequestFactory().get("/usuarios/")
        request.user = self.admin
        view = UserListView()
        view.setup(request)
        with self.assertNumQueries(1):
            users = list(view.get_queryset())
            for user in users:
                getattr(user, "profile", None)
                user.email_verificado

    def test_password_temporal_obliga_cambio(self):
        profile = self.estudiante.profile
        profile.requiere_cambio_password = True
        profile.save()
        self.client.force_login(self.estudiante)
        self.assertRedirects(self.client.get(reverse("Home")), reverse("account_change_password"), fetch_redirect_response=False)

    def test_password_temporal_caducada_cierra_sesion(self):
        from django.utils import timezone
        profile = self.estudiante.profile
        profile.requiere_cambio_password = True
        profile.password_temporal_expira = timezone.now() - timezone.timedelta(seconds=1)
        profile.save()
        self.client.force_login(self.estudiante)
        self.assertRedirects(self.client.get(reverse("Home")), reverse("account_reset_password"), fetch_redirect_response=False)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_cambiar_password_real_libera_restriccion(self):
        profile = self.estudiante.profile
        profile.requiere_cambio_password = True
        profile.save()
        self.client.force_login(self.estudiante)
        self.client.post(reverse("account_change_password"), {"oldpassword": "Clave-ficticia-789", "password1": "NuevaFicticia456!", "password2": "NuevaFicticia456!"})
        profile.refresh_from_db()
        self.assertFalse(profile.requiere_cambio_password)
        self.estudiante.refresh_from_db()
        self.assertTrue(self.estudiante.check_password("NuevaFicticia456!"))

    def test_logout_get_no_cierra_sesion_post_si(self):
        self.client.force_login(self.estudiante)
        self.client.get(reverse("account_logout"))
        self.assertIn("_auth_user_id", self.client.session)
        self.client.post(reverse("account_logout"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_verificacion_corresponde_al_correo_actual(self):
        from allauth.account.models import EmailAddress
        from django.test import RequestFactory
        from .views import UserListView
        EmailAddress.objects.create(user=self.estudiante, email="anterior@example.test", verified=True)
        view = UserListView()
        request = RequestFactory().get("/usuarios/")
        request.user = self.admin
        view.setup(request)
        self.assertFalse(view.get_queryset().get(pk=self.estudiante.pk).email_verificado)
