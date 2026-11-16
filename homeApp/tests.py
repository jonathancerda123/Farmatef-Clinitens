from django.test import TestCase

from django.urls import reverse
from django.utils import timezone
from core.test_helpers import usuario


class PrivacidadInicioTests(TestCase):
    def test_estudiante_solo_ve_su_conexion(self):
        student = usuario("alumno")
        other = usuario("ajeno")
        for user in [student, other]:
            user.last_login = timezone.now()
            user.save()
        self.client.force_login(student)
        response = self.client.get(reverse("Home"))
        self.assertNotContains(response, "ajeno@example.test")
        self.assertEqual(list(response.context["object_list"]), [student])

    def test_acceso_principal_clinico_abre_los_casos_del_perfil(self):
        portada = reverse("clinitens")
        casos_estudiante = reverse("clinitens_simulacion:estudiante_casos")
        casos_docente = reverse("clinitens_simulacion:docente_casos")
        for rol in ("RESTRICTED", "MANAGER", "ADMIN"):
            with self.subTest(rol=rol):
                self.client.force_login(usuario(f"casos-{rol.lower()}", rol))
                vista = self.client.get(portada)
                if rol == "RESTRICTED":
                    self.assertContains(vista, f'href="{casos_estudiante}"')
                    self.assertContains(vista, "Mis casos de práctica")
                    self.assertEqual(self.client.get(casos_estudiante).status_code, 200)
                    self.assertEqual(self.client.get(casos_docente).status_code, 403)
                else:
                    self.assertContains(vista, f'href="{casos_docente}#casos-titulo"')
                    self.assertEqual(self.client.get(casos_docente).status_code, 200)
                    self.assertEqual(self.client.get(casos_estudiante).status_code, 403)
        self.client.force_login(usuario("casos-sin-perfil", None))
        vista = self.client.get(portada)
        self.assertNotContains(vista, "Mis casos de práctica")
        self.assertNotContains(vista, "Gestionar casos de simulación")
