"""Regresión 034: categorías docentes, propiedad y rutas directas con datos ficticios."""
from datetime import date

from django.contrib.auth.models import AnonymousUser
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase
from django.urls import reverse

from CliniTensDocenteApp.forms import CursoColaboradorForm
from CliniTensDocenteApp.models import CasoClinico, CasoMultimedia, CodigoActividad, Curso
from CliniTensDocenteApp.views import fichas_visibles_para
from CliniTensFichaApp.models import FichaClinica
from FarmaTEFApp.models import Receta
from core.permissions import es_docente_de_area, recetas_visibles_para_docente
from core.test_helpers import usuario
from UsuarioApp.forms import AreaDocenteForm, ProfileCreateForm
from UsuarioApp.models import AreaDocente, Profile


class AreasDocentesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.farma = usuario("area-farma", "MANAGER", area_docente=AreaDocente.FARMACIA)
        cls.enfermeria = usuario("area-enfermeria", "MANAGER", area_docente=AreaDocente.ENFERMERIA)
        cls.ambos = usuario("area-ambos", "MANAGER")
        cls.admin = usuario("area-admin", "ADMIN")
        cls.root = usuario("area-root", None, is_superuser=True, is_staff=True)
        cls.alumno = usuario("area-alumno")
        cls.curso = Curso.objects.create(nombre="Curso ficticio 034", creado_por=cls.farma)
        cls.caso = CasoClinico.objects.create(titulo="Caso ficticio 034", contenido="<p>Simulación</p>", creado_por=cls.farma)
        cls.codigo = CodigoActividad.objects.create(codigo="AREA034", caso_clinico=cls.caso, creado_por=cls.farma)
        cls.ficha = FichaClinica.objects.create(codigo_actividad=cls.codigo, docente=cls.farma, estudiante=cls.alumno)

    def test_matriz_de_permisos_por_categoria_y_cargo(self):
        for user, farmacia, enfermeria in [
            (self.farma, True, False), (self.enfermeria, False, True),
            (self.ambos, True, True), (self.admin, True, True),
            (self.root, True, True), (self.alumno, False, False),
            (AnonymousUser(), False, False),
        ]:
            with self.subTest(user=str(user)):
                self.assertEqual(es_docente_de_area(user, AreaDocente.FARMACIA), farmacia)
                self.assertEqual(es_docente_de_area(user, AreaDocente.ENFERMERIA), enfermeria)
        self.farma.is_active = False
        self.assertFalse(es_docente_de_area(self.farma, AreaDocente.FARMACIA))

    def test_inicio_y_menu_solo_muestran_area_permitida(self):
        for user, farmacia, enfermeria in [
            (self.farma, True, False), (self.enfermeria, False, True),
            (self.ambos, True, True), (self.admin, True, True), (self.root, True, True),
        ]:
            self.client.force_login(user)
            response = self.client.get(reverse("Home"))
            for route, allowed in [("farmatef", farmacia), ("clinitens", enfermeria)]:
                with self.subTest(user=user.username, route=route):
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(f'href="{reverse(route)}"' in response.content.decode(), allowed)
            self.assertContains(response, f'href="{reverse("clinitensdocente:cursos")}"')

    def test_urls_clinicas_get_y_post_denegadas_a_farmacia(self):
        self.client.force_login(self.farma)
        routes = [
            ("clinitens", []), ("clinitensdocente:dashboard", []),
            ("clinitensdocente:casos", []), ("clinitensdocente:caso_editar", [self.caso.pk]),
            ("clinitensdocente:caso_eliminar", [self.caso.pk]),
            ("clinitensdocente:ficha_pdf", [self.ficha.pk]),
            ("clinitensdocente:ficha_rubrica", [self.ficha.pk]),
            ("clinitensficha:ingreso", []), ("clinitensficha:editor", [self.ficha.pk, "identificacion"]),
            ("clinitens_simulacion:docente_casos", []),
            ("clinitens_simulacion:publicar_caso", [999999]),
            ("clinitens_simulacion:dau_pdf", [999999]),
            ("clinitens_simulacion:orden_laboratorio_pdf", [999999]),
        ]
        for name, args in routes:
            for method in [self.client.get, self.client.post]:
                with self.subTest(route=name, method=method.__name__):
                    self.assertEqual(method(reverse(name, args=args)).status_code, 403)
        self.assertTrue(CasoClinico.objects.filter(pk=self.caso.pk).exists())

    def test_urls_farmacia_get_y_post_denegadas_a_enfermeria(self):
        self.client.force_login(self.enfermeria)
        for name, args in [
            ("farmatef", []), ("farmatef:inventario", []),
            ("farmatef:registro_inventario", []), ("farmatef:recetas", []),
            ("farmatef:etiquetado", []), ("farmatef:entregar_receta", [999999]),
            ("farmatef:eliminar_receta", [999999]), ("farmatef:vitrina", []),
            ("farmatef:comprobante_dispensacion", [999999]),
            ("clinitensdocente:curso_agregar_colaborador", [self.curso.pk]),
        ]:
            for method in [self.client.get, self.client.post]:
                with self.subTest(route=name, method=method.__name__):
                    self.assertEqual(method(reverse(name, args=args)).status_code, 403)

    def test_urls_permitidas_y_admin_global(self):
        for user, names in [
            (self.farma, ["farmatef", "farmatef:inventario", "farmatef:recetas"]),
            (self.enfermeria, ["clinitens", "clinitensdocente:casos", "clinitens_simulacion:docente_casos"]),
            (self.ambos, ["farmatef", "clinitens"]),
            (self.admin, ["farmatef", "clinitens"]), (self.root, ["farmatef", "clinitens"]),
        ]:
            self.client.force_login(user)
            for name in names:
                with self.subTest(user=user.username, route=name):
                    self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_cursos_compartidos_conservan_propiedad_y_menu(self):
        for owner in [self.farma, self.enfermeria]:
            curso = Curso.objects.create(nombre=f"Propio {owner.username}", creado_por=owner)
            self.client.force_login(owner)
            response = self.client.get(reverse("clinitensdocente:curso_detalle", args=[curso.pk]))
            self.assertEqual(response.status_code, 200)
            if owner == self.farma:
                self.assertNotContains(response, f'href="{reverse("clinitensdocente:casos")}"')
                self.assertContains(response, "Docentes colaboradores de FarmaTEF")
            else:
                self.assertNotContains(response, "Docentes colaboradores de FarmaTEF")
                self.assertEqual(self.client.get(reverse("clinitensdocente:curso_detalle", args=[self.curso.pk])).status_code, 404)
            response = self.client.post(reverse("clinitensdocente:cursos"), {"nombre": f"Nuevo {owner.username}"})
            self.assertEqual(response.status_code, 302)
            self.assertTrue(Curso.objects.filter(nombre=f"Nuevo {owner.username}", creado_por=owner).exists())

    def test_cambio_administrativo_aplica_en_la_siguiente_peticion(self):
        self.client.force_login(self.ambos)
        self.assertEqual(self.client.get(reverse("clinitens")).status_code, 200)
        # Simula la edición desde otra sesión administrativa.
        from django.test import Client
        administrador = Client()
        administrador.force_login(self.admin)
        response = administrador.post(reverse("UserTeacherArea", args=[self.ambos.pk]), {"area_docente": "FARMACIA"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get(reverse("clinitens")).status_code, 403)
        self.assertEqual(self.client.get(reverse("farmatef")).status_code, 200)
        self.ambos.profile.refresh_from_db()
        self.assertEqual(self.ambos.profile.area_docente, "FARMACIA")

    def test_solo_administrador_cambia_area_y_protege_superusuario(self):
        url = reverse("UserTeacherArea", args=[self.farma.pk])
        for user in [self.farma, self.enfermeria, self.alumno]:
            self.client.force_login(user)
            for method in [self.client.get, self.client.post]:
                self.assertEqual(method(url, {"area_docente": "AMBOS"}).status_code, 403)
        protegido = usuario("super-con-perfil", "MANAGER", is_superuser=True, is_staff=True)
        self.client.force_login(self.admin)
        url = reverse("UserTeacherArea", args=[protegido.pk])
        self.assertEqual(self.client.get(url).status_code, 403)
        self.assertEqual(self.client.post(url, {"area_docente": "FARMACIA"}).status_code, 403)
        self.assertEqual(self.client.get(reverse("UserTeacherArea", args=[self.alumno.pk])).status_code, 404)

    def test_creacion_exige_area_docente_y_descarta_area_de_estudiante(self):
        datos = {"position_FK": self.farma.profile.position_FK_id}
        form = ProfileCreateForm(datos, actor=self.admin)
        self.assertFalse(form.is_valid())
        self.assertIn("area_docente", form.errors)
        for area in AreaDocente.values:
            form = ProfileCreateForm({**datos, "area_docente": area}, actor=self.admin)
            self.assertTrue(form.is_valid(), form.errors)
        form = ProfileCreateForm({**datos, "area_docente": "OTRA"}, actor=self.admin)
        self.assertFalse(form.is_valid())
        form = ProfileCreateForm({"position_FK": self.alumno.profile.position_FK_id, "area_docente": "AMBOS"}, actor=self.admin)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["area_docente"], "")

    def test_edicion_area_valida_y_no_cambia_otros_campos(self):
        self.client.force_login(self.admin)
        url = reverse("UserTeacherArea", args=[self.farma.pk])
        for area in ["", "OTRA"]:
            response = self.client.post(url, {"area_docente": area})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["form"].errors)
        response = self.client.post(url, {"area_docente": "ENFERMERIA", "position_FK": self.admin.profile.position_FK_id, "user_FK": self.alumno.pk})
        self.assertEqual(response.status_code, 302)
        self.farma.profile.refresh_from_db()
        self.assertEqual(self.farma.profile.area_docente, "ENFERMERIA")
        self.assertEqual(self.farma.profile.position_FK.permission_code, "MANAGER")
        self.assertEqual(self.farma.profile.user_FK_id, self.farma.pk)
        self.assertNotIn("area_docente", AreaDocenteForm().initial)

    def test_perfil_personal_no_permite_escalar_area(self):
        self.client.force_login(self.farma)
        response = self.client.post(reverse("Profile"), {"username": self.farma.username, "email": self.farma.email, "area_docente": "AMBOS"})
        self.assertEqual(response.status_code, 302)
        self.farma.profile.refresh_from_db()
        self.assertEqual(self.farma.profile.area_docente, "FARMACIA")

    def test_sin_categoria_no_accede_a_modulos(self):
        Profile.objects.filter(user_FK=self.ambos).update(area_docente="")
        self.client.force_login(self.ambos)
        for name in ["farmatef", "clinitens"]:
            self.assertEqual(self.client.get(reverse(name)).status_code, 403)
        self.assertContains(self.client.get(reverse("Home")), "asigne tu área docente")
        # Un perfil incompleto muestra errores de validación, sin excepción por campos excluidos.
        self.assertEqual(self.client.post(reverse("Profile"), {"username": self.ambos.username}).status_code, 200)

    def test_colaboracion_filtra_area_y_conserva_vinculos_historicos(self):
        form = CursoColaboradorForm(curso=self.curso)
        choices = form.fields["docente"].queryset
        self.assertIn(self.ambos, choices)
        self.assertNotIn(self.enfermeria, choices)
        self.curso.docentes_colaboradores.add(self.ambos)
        receta = Receta.objects.create(numero="AREA034", persona_ficticia="Persona simulada", vence_el=date(2030, 1, 1), curso=self.curso, creado_por=self.farma)
        self.assertTrue(recetas_visibles_para_docente(Receta.objects.all(), self.ambos).filter(pk=receta.pk).exists())
        Profile.objects.filter(user_FK=self.ambos).update(area_docente="ENFERMERIA")
        self.ambos.refresh_from_db()
        self.assertFalse(recetas_visibles_para_docente(Receta.objects.all(), self.ambos).exists())
        self.assertTrue(self.curso.docentes_colaboradores.filter(pk=self.ambos.pk).exists())
        self.client.force_login(self.farma)
        response = self.client.post(reverse("clinitensdocente:curso_agregar_colaborador", args=[self.curso.pk]), {"docente": self.enfermeria.pk})
        self.assertRedirects(response, reverse("clinitensdocente:curso_detalle", args=[self.curso.pk]))
        self.assertFalse(self.curso.docentes_colaboradores.filter(pk=self.enfermeria.pk).exists())

    def test_consulta_fichas_y_actividad_clinica_retiradas(self):
        self.assertFalse(fichas_visibles_para(self.farma).exists())
        self.client.force_login(self.farma)
        response = self.client.get(reverse("Home"))
        self.assertNotContains(response, self.alumno.email)
        Profile.objects.filter(user_FK=self.farma).update(area_docente="ENFERMERIA")
        self.farma.refresh_from_db()
        self.assertTrue(fichas_visibles_para(self.farma).filter(pk=self.ficha.pk).exists())

    def test_archivo_clinico_denegado_a_farmacia_aunque_sea_propietario(self):
        nombre = default_storage.save("ficticios-034/caso.pdf", ContentFile(b"%PDF-1.4 ficticio"))
        self.addCleanup(default_storage.delete, nombre)
        CasoMultimedia.objects.create(caso=self.caso, archivo=nombre)
        self.client.force_login(self.farma)
        url = reverse("archivo_privado", args=[nombre])
        self.assertEqual(self.client.get(url).status_code, 404)
        Profile.objects.filter(user_FK=self.farma).update(area_docente="ENFERMERIA")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response.close()

    def test_estudiante_conserva_las_dos_areas_sin_gestion(self):
        self.client.force_login(self.alumno)
        response = self.client.get(reverse("Home"))
        self.assertContains(response, f'href="{reverse("clinitens")}"')
        self.assertContains(response, f'href="{reverse("farmatef:practica_recetas")}"')
        self.assertNotContains(response, f'href="{reverse("clinitensdocente:cursos")}"')
        self.assertEqual(self.client.get(reverse("farmatef:inventario")).status_code, 403)
