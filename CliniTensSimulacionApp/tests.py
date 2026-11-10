"""Regresiones RAE con identidades/casos sintéticos y base aislada."""
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from CliniTensDocenteApp.models import Curso
from core.test_helpers import usuario
from .models import AtencionDAU, AtencionEnfermeria, CasoSimulacion


class PreparacionGuiadaTests(TestCase):
    def setUp(self):
        self.docente = usuario("guia-docente", "MANAGER")
        self.ajeno = usuario("guia-ajeno", "MANAGER")
        curso = Curso.objects.create(nombre="Curso guía", creado_por=self.docente)
        self.caso = CasoSimulacion.objects.create(curso=curso, creado_por=self.docente, titulo="Caso elegido", resumen="Ejercicio")
        self.otro = CasoSimulacion.objects.create(curso=curso, creado_por=self.docente, titulo="Otro caso", resumen="Otro ejercicio")
        self.client.force_login(self.docente)

    def url(self, modulo):
        return reverse(f"clinitens_simulacion:docente_{modulo}") + f"?caso={self.caso.pk}"

    def test_seleccion_y_errores_conservan_un_solo_caso(self):
        response = self.client.get(self.url("enfermeria"))
        self.assertContains(response, "Caso elegido")
        self.assertNotContains(response, "Otro caso")
        response = self.client.post(self.url("enfermeria"), {"caso_id": self.caso.pk})
        self.assertContains(response, "Caso elegido")
        self.assertNotContains(response, "Otro caso")
        self.assertTrue(response.context["filas"][0]["form"].errors)

    def test_guardar_continua_y_no_admite_otro_caso(self):
        url = self.url("laboratorio")
        data = {"caso_id": self.otro.pk, "escenario_laboratorio": "Contexto ficticio", "ordenes": "Examen de prueba | Muestra ficticia | Tubo de práctica"}
        self.assertEqual(self.client.post(url, data).status_code, 404)
        data["caso_id"] = self.caso.pk
        self.assertRedirects(self.client.post(url, data), self.url("diagnostico"))
        self.caso.refresh_from_db()
        self.assertEqual(len(self.caso.ordenes_laboratorio), 1)
        self.assertEqual(self.caso.escenario_dau, "")

    def test_revision_y_publicacion_revalidan_requisitos(self):
        review = reverse("clinitens_simulacion:preparar_caso", args=[self.caso.pk])
        publish = reverse("clinitens_simulacion:publicar_caso", args=[self.caso.pk])
        response = self.client.get(review)
        self.assertContains(response, "Antes de publicar")
        self.assertNotContains(response, 'type="submit"')
        self.client.post(publish, {"volver_preparacion": "1"})
        self.caso.refresh_from_db()
        self.assertFalse(self.caso.publicado)
        CasoSimulacion.objects.filter(pk=self.caso.pk).update(paciente_codigo="SIM-GUIA-001", paciente_nombre="Paciente ficticio", escenario_dau="Escenario", ordenes_laboratorio=[{"examen":"Prueba"}], documentos_diagnosticos=[{"titulo":"Informe"}])
        self.assertContains(self.client.get(review), "Publicar caso para mi curso")
        self.assertRedirects(self.client.post(publish, {"volver_preparacion": "1"}), review)
        self.caso.refresh_from_db()
        self.assertTrue(self.caso.publicado)
        self.assertNotContains(self.client.get(self.url("laboratorio")), "Guardar y continuar")

    def test_ajeno_estudiante_e_identificador_invalido_denegados(self):
        review = reverse("clinitens_simulacion:preparar_caso", args=[self.caso.pk])
        self.client.force_login(self.ajeno)
        self.assertEqual(self.client.get(review).status_code, 404)
        self.assertEqual(self.client.get(self.url("enfermeria")).status_code, 404)
        self.client.force_login(self.docente)
        self.assertEqual(self.client.get(reverse("clinitens_simulacion:docente_enfermeria")+"?caso=abc").status_code, 404)
        self.client.force_login(usuario("guia-alumno"))
        self.assertEqual(self.client.get(review).status_code, 403)

    def test_creacion_comienza_por_paciente(self):
        curso = self.caso.curso
        response = self.client.post(reverse("clinitens_simulacion:docente_casos"), {"curso":curso.pk,"titulo":"Nuevo caso guiado","resumen":"Ejercicio"})
        nuevo = CasoSimulacion.objects.get(titulo="Nuevo caso guiado")
        self.assertRedirects(response, reverse("clinitens_simulacion:docente_enfermeria")+f"?caso={nuevo.pk}")


class EnfermeriaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.docente = usuario("docente-rae", "MANAGER")
        cls.otro_docente = usuario("docente-ajeno-rae", "MANAGER")
        cls.alumno = usuario("alumno-rae")
        cls.otro_alumno = usuario("alumno-ajeno-rae")
        cls.sin_matricula = usuario("sin-matricula-rae")
        cls.admin = usuario("admin-rae", "ADMIN")
        cls.superusuario = usuario("super-rae", None, is_superuser=True, is_staff=True)
        cls.sin_perfil = usuario("sin-perfil-rae", None)
        cls.inactivo = usuario("inactivo-rae", is_active=False)
        cls.curso = Curso.objects.create(nombre="Curso ficticio RAE", creado_por=cls.docente)
        cls.curso.estudiantes.add(cls.alumno, cls.otro_alumno)
        cls.caso = CasoSimulacion.objects.create(
            curso=cls.curso, creado_por=cls.docente, titulo="Caso ficticio RAE",
            resumen="Ejercicio educativo", paciente_codigo="SIM-RAE-001",
            paciente_nombre="Paciente de demostración", publicado=True,
            escenario_dau="Escenario DAU conservado", escenario_laboratorio="Contexto conservado",
        )
        cls.borrador = CasoSimulacion.objects.create(
            curso=cls.curso, creado_por=cls.docente, titulo="Caso no publicado",
            resumen="Ejercicio no disponible", paciente_codigo="SIM-RAE-002",
            paciente_nombre="Paciente reservado",
            escenario_dau="DAU de borrador conservado", escenario_laboratorio="Laboratorio conservado",
            ordenes_laboratorio=[{"id": "orden-ficticia", "examen": "Examen de práctica"}],
            documentos_diagnosticos=[{"id": "informe-ficticio", "tipo": "informe"}],
        )

    def setUp(self):
        self.client.force_login(self.alumno)
        self.inicio = reverse("clinitens_simulacion:enfermeria_inicio")
        self.historial = reverse("clinitens_simulacion:enfermeria_historial")

    def abrir(self):
        response = self.client.post(self.inicio, {"codigo": " sim-rae-001 "})
        self.assertEqual(response.status_code, 302)
        return AtencionEnfermeria.objects.get(estudiante=self.alumno, finalizada=False)

    def url(self, atencion):
        return reverse("clinitens_simulacion:enfermeria_registro", args=[atencion.pk])

    def payload(self, **kwargs):
        return {"version": 1, "accion": "guardar", "cuidados": "Cuidados ficticios", "observaciones": "Observación ficticia", **kwargs}

    def test_busqueda_continua_borrador_y_no_crea_dau(self):
        atencion = self.abrir()
        self.assertEqual(self.abrir().pk, atencion.pk)
        self.assertEqual(AtencionEnfermeria.objects.count(), 1)
        self.assertEqual(AtencionDAU.objects.count(), 0)
        self.assertContains(self.client.get(self.url(atencion)), self.caso.paciente_nombre)

    def test_borrador_parcial_cierre_y_nueva_atencion(self):
        atencion = self.abrir()
        response = self.client.post(self.url(atencion), self.payload(cuidados="", observaciones="Avance"))
        self.assertEqual(response.status_code, 302)
        atencion.refresh_from_db()
        self.assertEqual(atencion.version, 2)
        self.assertFalse(atencion.finalizada)
        response = self.client.post(self.url(atencion), self.payload(version=2, accion="finalizar"))
        self.assertEqual(response.status_code, 302)
        atencion.refresh_from_db()
        self.assertTrue(atencion.finalizada)
        self.assertIsNotNone(atencion.finalizada_en)
        self.assertEqual(atencion.estudiante, self.alumno)
        self.assertEqual(atencion.version, 3)
        closed = self.client.get(self.url(atencion))
        self.assertContains(closed, "Cuidados ficticios")
        self.assertNotContains(closed, 'name="cuidados"')
        nueva = self.abrir()
        self.assertNotEqual(nueva.pk, atencion.pk)
        self.assertEqual(nueva.cuidados, "")

    def test_finalizar_exige_cuidados_y_conserva_texto(self):
        atencion = self.abrir()
        response = self.client.post(self.url(atencion), self.payload(accion="finalizar", cuidados="  ", observaciones="Texto conservado"))
        self.assertContains(response, "Texto conservado", status_code=400)
        self.assertContains(response, "Registra los cuidados", status_code=400)
        atencion.refresh_from_db()
        self.assertFalse(atencion.finalizada)
        self.assertEqual(atencion.version, 1)

    def test_dos_pestanas_no_sobrescriben_y_no_pueden_cerrar_version_antigua(self):
        atencion = self.abrir()
        self.client.post(self.url(atencion), self.payload(cuidados="Primera pestaña"))
        response = self.client.post(self.url(atencion), self.payload(accion="finalizar", cuidados="Segunda pestaña"))
        self.assertContains(response, "Segunda pestaña", status_code=409)
        self.assertContains(response, "Recargar registro vigente", status_code=409)
        atencion.refresh_from_db()
        self.assertEqual(atencion.cuidados, "Primera pestaña")
        self.assertEqual(atencion.version, 2)
        self.assertFalse(atencion.finalizada)

    def test_no_se_modifica_registro_finalizado(self):
        atencion = self.abrir()
        self.client.post(self.url(atencion), self.payload(accion="finalizar"))
        response = self.client.post(self.url(atencion), self.payload(version=2, cuidados="Cambio rechazado"))
        self.assertContains(response, "Cambio rechazado", status_code=409)
        atencion.refresh_from_db()
        self.assertEqual(atencion.cuidados, "Cuidados ficticios")
        self.assertEqual(atencion.version, 2)

    def test_version_accion_y_limites_son_obligatorios_en_servidor(self):
        atencion = self.abrir()
        for changed in ({"version": ""}, {"version": 0}, {"version": "abc"}, {"accion": "borrar"}, {"cuidados": "x" * 5001}, {"observaciones": "x" * 2001}):
            with self.subTest(changed=list(changed)):
                response = self.client.post(self.url(atencion), self.payload(**changed))
                self.assertEqual(response.status_code, 400)
        data = self.payload()
        data.pop("version")
        self.assertEqual(self.client.post(self.url(atencion), data).status_code, 400)
        atencion.refresh_from_db()
        self.assertEqual(atencion.version, 1)
        self.assertEqual(atencion.cuidados, "")

    def test_texto_se_escapa_al_mostrar(self):
        atencion = self.abrir()
        self.client.post(self.url(atencion), self.payload(accion="finalizar", cuidados='<script>alert("ficticio")</script>'))
        response = self.client.get(self.url(atencion))
        self.assertContains(response, "&lt;script&gt;")
        self.assertNotContains(response, '<script>alert("ficticio")</script>')

    def test_datos_ajenos_y_caso_no_publicado_no_se_revelan(self):
        atencion = self.abrir()
        self.client.force_login(self.otro_alumno)
        self.assertEqual(self.client.get(self.url(atencion)).status_code, 404)
        self.assertEqual(self.client.post(self.url(atencion), self.payload()).status_code, 404)
        self.assertNotContains(self.client.get(self.historial), f"RAE #{atencion.pk}")
        self.assertNotContains(self.client.get(self.inicio), self.borrador.paciente_nombre)
        self.assertContains(self.client.post(self.inicio, {"codigo": self.borrador.paciente_codigo}), "No encontramos ese código")
        self.client.force_login(self.sin_matricula)
        self.assertEqual(self.client.get(self.url(atencion)).status_code, 404)
        self.assertContains(self.client.post(self.inicio, {"codigo": self.caso.paciente_codigo}), "No encontramos ese código")

    def test_revalida_matricula_y_publicacion_antes_de_guardar(self):
        atencion = self.abrir()
        self.curso.estudiantes.remove(self.alumno)
        self.assertEqual(self.client.post(self.url(atencion), self.payload()).status_code, 404)
        self.curso.estudiantes.add(self.alumno)
        CasoSimulacion.objects.filter(pk=self.caso.pk).update(publicado=False)
        self.assertEqual(self.client.get(self.url(atencion)).status_code, 404)
        self.assertEqual(self.client.post(self.url(atencion), self.payload()).status_code, 404)
        self.assertNotContains(self.client.get(self.historial), f"RAE #{atencion.pk}")

    def test_perfiles_no_estudiantes_no_entran_a_practica(self):
        atencion = self.abrir()
        for user in (self.docente, self.admin, self.superusuario, self.sin_perfil, self.inactivo):
            with self.subTest(user=user.username):
                self.client.force_login(user)
                for url in (self.inicio, self.historial, self.url(atencion)):
                    self.assertEqual(self.client.get(url).status_code, 403)
                self.assertEqual(self.client.post(self.url(atencion), self.payload()).status_code, 403)
        self.client.logout()
        self.assertEqual(self.client.get(self.inicio).status_code, 403)
        self.assertEqual(self.client.post(self.url(atencion), self.payload()).status_code, 403)
        self.assertEqual(self.client.get(reverse("clinitens")).status_code, 302)

    def test_un_borrador_por_alumno_caso_en_base(self):
        self.abrir()
        with self.assertRaises(IntegrityError), transaction.atomic():
            AtencionEnfermeria.objects.create(caso=self.caso, estudiante=self.alumno)
        otro = AtencionEnfermeria.objects.create(caso=self.caso, estudiante=self.otro_alumno)
        self.assertNotEqual(otro.estudiante, self.alumno)

    def test_historial_paginado_y_solo_propio(self):
        AtencionEnfermeria.objects.bulk_create([
            AtencionEnfermeria(caso=self.caso, estudiante=self.alumno, finalizada=True)
            for _ in range(21)
        ])
        response = self.client.get(self.historial)
        self.assertEqual(len(response.context["page_obj"]), 20)
        self.assertTrue(response.context["page_obj"].has_next())
        self.assertEqual(len(self.client.get(self.historial, {"page": 2}).context["page_obj"]), 1)

    def test_preparacion_docente_conserva_otros_modulos(self):
        self.client.force_login(self.docente)
        url = reverse("clinitens_simulacion:docente_enfermeria")
        prefix = f"rae-{self.borrador.pk}-"
        data = {"caso_id": self.borrador.pk, **{prefix + k: v for k, v in {
            "paciente_codigo": "SIM-RAE-002", "paciente_nombre": "Paciente editado",
            "paciente_sexo": "O", "paciente_edad": 25, "paciente_fecha_nacimiento": "2001-01-01",
            "paciente_comuna": "Comuna ficticia", "paciente_antecedentes": "Antecedentes ficticios",
        }.items()}}
        self.assertEqual(self.client.post(url, data).status_code, 302)
        self.borrador.refresh_from_db()
        self.assertEqual(self.borrador.paciente_nombre, "Paciente editado")
        self.assertEqual(self.borrador.escenario_dau, "DAU de borrador conservado")
        self.assertEqual(self.borrador.escenario_laboratorio, "Laboratorio conservado")
        self.assertEqual(self.borrador.ordenes_laboratorio, [{"id": "orden-ficticia", "examen": "Examen de práctica"}])
        self.assertEqual(self.borrador.documentos_diagnosticos, [{"id": "informe-ficticio", "tipo": "informe"}])
        data["caso_id"] = self.caso.pk
        self.assertEqual(self.client.post(url, data).status_code, 302)
        self.caso.refresh_from_db()
        self.assertEqual(self.caso.paciente_nombre, "Paciente de demostración")
        self.assertEqual(self.caso.escenario_dau, "Escenario DAU conservado")
        self.client.force_login(self.otro_docente)
        self.assertEqual(self.client.post(url, data).status_code, 404)
        for user in (self.alumno, self.sin_perfil, self.inactivo):
            self.client.force_login(user)
            self.assertEqual(self.client.get(url).status_code, 403)
        for user in (self.admin, self.superusuario):
            self.client.force_login(user)
            self.assertEqual(self.client.get(url).status_code, 200)

    def test_preparacion_rechaza_identificador_no_sim_y_codigo_duplicado(self):
        from .forms import PacienteEnfermeriaDocenteForm
        for codigo in ("12.345.678-9", "SIM-RAE-001"):
            form = PacienteEnfermeriaDocenteForm({
                "paciente_codigo": codigo, "paciente_nombre": "Paciente ficticio",
                "paciente_sexo": "O", "paciente_edad": 25, "paciente_fecha_nacimiento": "2001-01-01",
                "paciente_comuna": "Comuna ficticia",
            }, instance=self.borrador)
            self.assertFalse(form.is_valid())
            self.assertIn("paciente_codigo", form.errors)
