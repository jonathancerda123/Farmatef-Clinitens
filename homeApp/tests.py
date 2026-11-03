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
