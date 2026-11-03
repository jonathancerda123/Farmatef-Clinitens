import json
from django.test import TestCase
from django.urls import reverse
from core.test_helpers import usuario
from CliniTensDocenteApp.models import CasoClinico, CodigoActividad
from .models import FichaClinica


class IntegridadFichaTests(TestCase):
    def setUp(self):
        self.docente = usuario("docente", "MANAGER")
        self.alumno = usuario("alumno")
        self.caso = CasoClinico.objects.create(titulo="Caso ficticio", contenido="<p>Simulación</p>", creado_por=self.docente)
        self.codigo = CodigoActividad.objects.create(codigo="PRUEBA", caso_clinico=self.caso, creado_por=self.docente, activo=True)
        self.ficha = FichaClinica.objects.create(codigo_actividad=self.codigo, estudiante=self.alumno, docente=self.docente)
        self.client.force_login(self.alumno)

    def post(self, datos, accion="guardar", seccion="identidad", version=0):
        return self.client.post(reverse("clinitensficha:editor", args=[self.ficha.pk, seccion]),
                                {"datos_json": json.dumps(datos), "accion": accion, "version": version})

    def test_rechaza_clave_desconocida_sin_guardar(self):
        response = self.post({"ajeno": {"nombre": "No guardar"}})
        self.ficha.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.ficha.datos, {})

    def test_no_envia_ficha_vacia(self):
        self.post({}, "finalizar")
        self.ficha.refresh_from_db()
        self.assertEqual(self.ficha.estado, FichaClinica.Estado.BORRADOR)

    def test_post_seccion_invalida(self):
        self.assertEqual(self.post({}, seccion="inventada").status_code, 404)

    def test_guardado_obsoleto_no_sobrescribe(self):
        self.post({"identidad": {"nombre": "Primero"}})
        response = self.post({"identidad": {"nombre": "Obsoleto"}})
        self.ficha.refresh_from_db()
        self.assertEqual(response.status_code, 409)
        self.assertEqual(self.ficha.datos["identidad"]["nombre"], "Primero")

    def test_envio_incompleto_conserva_avance(self):
        self.post({"identidad": {"nombre": "Ficticio"}}, "finalizar")
        self.ficha.refresh_from_db()
        self.assertEqual(self.ficha.datos["identidad"]["nombre"], "Ficticio")
        self.assertEqual(self.ficha.estado, "BORRADOR")

    def test_envio_completo_y_bloqueo_posterior(self):
        from .ficha_config import SECCIONES
        self.ficha.datos = {k: {"no_aplica": True} for k, _, _ in SECCIONES if k != "identidad"}
        self.ficha.save()
        response = self.post({"identidad": {"nombre": "Paciente ficticio", "rut": "FICTICIO-1", "edad": "20", "sexo": "Mujer"}}, "finalizar")
        self.assertEqual(response.status_code, 302)
        self.ficha.refresh_from_db()
        self.assertEqual(self.ficha.estado, "ENVIADA")
        self.assertIsNotNone(self.ficha.enviada_en)
        self.post({"identidad": {"nombre": "Cambio posterior"}}, version=1)
        self.ficha.refresh_from_db()
        self.assertEqual(self.ficha.datos["identidad"]["nombre"], "Paciente ficticio")

    def test_tipos_limites_y_catalogos(self):
        inputs = [{"identidad": {"edad": "NaN"}}, {"identidad": {"edad": "121"}},
                  {"identidad": {"sexo": "inventado"}}, {"identidad": {"no_aplica": True}},
                  {"identidad": {"nombre": "a" * 5001}}, {"farmacos": {"filas": [{}] * 201}},
                  {"riesgos": {"glasgow_1": "inventado"}}, {"necesidades": {"henderson": ["inventado"]}}]
        for data in inputs:
            with self.subTest(data=str(data)[:60]):
                section = next(iter(data))
                self.assertEqual(self.post(data, seccion=section).status_code, 400)
        self.ficha.refresh_from_db()
        self.assertEqual(self.ficha.datos, {})

    def test_campo_aislado_no_completa_seccion(self):
        from .validation import pendientes
        missing = pendientes({"signos": {"fc": "70"}})
        self.assertIn("Signos Vitales", missing)

    def test_otro_estudiante_no_abre_ficha(self):
        self.client.force_login(usuario("otro_alumno"))
        self.assertEqual(self.client.get(reverse("clinitensficha:caso", args=[self.ficha.pk])).status_code, 404)

    def test_curso_restringe_ingreso_y_acceso_directo(self):
        from CliniTensDocenteApp.models import Curso
        from .forms import IngresoFichaForm
        curso = Curso.objects.create(nombre="Curso ficticio", creado_por=self.docente)
        self.codigo.curso = curso
        self.codigo.save()
        self.assertNotIn(self.codigo, IngresoFichaForm(actor=self.alumno).fields["codigo_actividad"].queryset)
        self.assertEqual(self.client.get(reverse("clinitensficha:caso", args=[self.ficha.pk])).status_code, 404)
        curso.estudiantes.add(self.alumno)
        self.assertIn(self.codigo, IngresoFichaForm(actor=self.alumno).fields["codigo_actividad"].queryset)
        self.assertEqual(self.client.get(reverse("clinitensficha:caso", args=[self.ficha.pk])).status_code, 200)

    def test_docente_del_codigo_es_obligatorio_y_super_sin_perfil_valido(self):
        from .forms import IngresoFichaForm
        otro = usuario("otro_docente", "MANAGER")
        form = IngresoFichaForm({"codigo_actividad": self.codigo.pk, "docente": otro.pk}, actor=self.alumno)
        self.assertFalse(form.is_valid())
        root = usuario("root", None, is_superuser=True)
        self.codigo.creado_por = root
        self.codigo.save()
        form = IngresoFichaForm({"codigo_actividad": self.codigo.pk, "docente": root.pk}, actor=self.alumno)
        self.assertTrue(form.is_valid(), form.errors)
