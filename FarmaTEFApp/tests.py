from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Barrier
from unittest import skipUnless

from django.core.exceptions import ValidationError
from django.db import connection, connections
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.utils import timezone
from CliniTensDocenteApp.models import Curso
from core.test_helpers import usuario
from .forms import EtiquetaLoteForm, LoteInventarioForm, RecetaLineaForm
from .models import Dispensacion, DispensacionLote, LoteInventario, Medicamento, Receta, RecetaLinea, RespuestaReceta
from .services import entregar_receta


class SelectorMedicamentosTests(TestCase):
    def setUp(self):
        self.docente = usuario('busqueda-docente', 'MANAGER')
        self.ajeno = usuario('busqueda-ajeno', 'MANAGER')
        self.med = Medicamento.objects.create(nombre='Medicamento ficticio', principio_activo='Principio ficticio', concentracion='Presentación de práctica', creado_por=self.docente)
        self.otro = Medicamento.objects.create(nombre='Medicamento ajeno', creado_por=self.ajeno)
        self.lote = LoteInventario.objects.create(medicamento=self.med, registrado_por=self.docente, numero_lote='LOTE-PRUEBA', vence_el='2030-01-01', unidades=10)
        self.lote_ajeno = LoteInventario.objects.create(medicamento=self.otro, registrado_por=self.ajeno, numero_lote='LOTE-AJENO', vence_el='2030-01-01', unidades=10)

    def test_widgets_conservan_opciones_y_metadatos_autorizados(self):
        for form in (EtiquetaLoteForm(actor=self.docente), LoteInventarioForm(actor=self.docente), RecetaLineaForm(actor=self.docente)):
            html = str(form['medicamento'])
            self.assertIn('data-medicamento-search', html)
            self.assertIn('data-search=', html)
            self.assertIn('Principio ficticio', html)
            self.assertNotIn('Medicamento ajeno', html)

    def test_registro_lote_solo_incluye_codigos_de_productos_visibles(self):
        Medicamento.objects.filter(pk=self.med.pk).update(codigo_barras="0012345678905")
        Medicamento.objects.filter(pk=self.otro.pk).update(codigo_barras="0076543210982")
        self.client.force_login(self.docente)
        registro = reverse("farmatef:registro_inventario")
        vista = self.client.get(registro)
        self.assertContains(vista, 'data-medicine-accepts-barcode')
        self.assertContains(vista, 'data-medicine-barcode="0012345678905"')
        self.assertNotContains(vista, "0076543210982")

    def test_texto_libre_y_opcion_ajena_no_son_selecciones_validas(self):
        for value in ('Texto sin seleccionar', str(self.otro.pk)):
            form = RecetaLineaForm({'medicamento':value, 'unidades':1}, actor=self.docente)
            self.assertFalse(form.is_valid())
            self.assertIn('medicamento', form.errors)

    def test_relacion_lote_y_seleccion_tras_error_se_conservan(self):
        data = {'medicamento':self.med.pk, 'lote':self.lote_ajeno.pk, 'ancho_mm':55, 'alto_mm':44, 'copias':1}
        form = EtiquetaLoteForm(data, actor=self.docente)
        self.assertFalse(form.is_valid())
        self.assertIn('lote', form.errors)
        self.assertIn(f'value="{self.med.pk}" selected', str(form['medicamento']))
        data['lote'] = self.lote.pk
        self.assertTrue(EtiquetaLoteForm(data, actor=self.docente).is_valid())

    def test_inicio_ofrece_areas_y_destino_estudiantil(self):
        alumno = usuario('busqueda-alumno')
        self.client.force_login(alumno)
        response = self.client.get(reverse('Home'))
        self.assertContains(response, reverse('farmatef:practica_recetas'))
        self.assertContains(response, 'area-launch-grid')
        self.assertNotContains(response, 'Aprender cuidando.')


class NumeroLoteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.docente = usuario("lotes-docente", "MANAGER")
        cls.admin = usuario("lotes-admin", "ADMIN")
        cls.superusuario = usuario("lotes-super", None, is_staff=True, is_superuser=True)
        cls.medicamento = Medicamento.objects.create(
            nombre="Amoxicilina de práctica", creado_por=cls.docente,
        )

    def datos_lote(self, numero):
        return {
            "medicamento": self.medicamento.pk, "numero_lote": numero,
            "vence_el": "2099-01-01", "unidades": 4,
        }

    def post_inventario(self, numero, ruta="registro_inventario"):
        return self.client.post(
            reverse(f"farmatef:{ruta}"),
            {"crear_lote": "", **{f"lote-{campo}": valor for campo, valor in self.datos_lote(numero).items()}},
        )

    def test_inventario_normaliza_y_rechaza_duplicados_para_cargos_autorizados(self):
        for indice, actor in enumerate((self.docente, self.admin, self.superusuario), start=1):
            with self.subTest(actor=actor):
                self.client.force_login(actor)
                self.assertRedirects(
                    self.post_inventario(f" AMOx-{indice:03d} "),
                    reverse("farmatef:inventario"),
                )
                lote = self.medicamento.lotes.get(registrado_por=actor)
                self.assertEqual(lote.numero_lote, f"AMOX-{indice:03d}")
                repetido = self.post_inventario(f"amox-{indice:03d}", ruta="inventario")
                self.assertFormError(
                    repetido.context["form_lote"], "numero_lote", "Ese lote ya existe para el medicamento.",
                )
        self.assertEqual(self.medicamento.lotes.count(), 3)
        self.assertEqual(self.medicamento.stock_total, 12)

    def test_rechaza_duplicado_de_lote_historico_con_minusculas(self):
        LoteInventario.objects.create(
            medicamento=self.medicamento, registrado_por=self.docente,
            numero_lote="AMOx-002", vence_el="2099-01-01", unidades=4,
        )
        self.client.force_login(self.docente)
        repetido = self.post_inventario("AMOX-002")
        self.assertEqual(repetido.status_code, 200)
        self.assertFormError(
            repetido.context["form_lote"], "numero_lote", "Ese lote ya existe para el medicamento.",
        )
        self.assertEqual(self.medicamento.lotes.get().numero_lote, "AMOx-002")
        self.assertEqual(self.medicamento.stock_total, 4)

    def test_django_admin_normaliza_y_rechaza_duplicados(self):
        self.client.force_login(self.superusuario)
        ruta = reverse("admin:FarmaTEFApp_loteinventario_add")
        self.assertEqual(self.client.post(ruta, self.datos_lote("AMOx-001")).status_code, 302)
        lote = self.medicamento.lotes.get()
        self.assertEqual(lote.numero_lote, "AMOX-001")
        repetido = self.client.post(ruta, self.datos_lote("amox-001"))
        self.assertFormError(
            repetido.context["adminform"].form, "numero_lote", "Ese lote ya existe para el medicamento.",
        )
        self.assertEqual(self.medicamento.lotes.count(), 1)

    def test_django_admin_puede_editar_lote_historico_sin_cambiar_su_numero(self):
        for numero in ("AMOX-002", "AMOx-002"):
            lote = LoteInventario.objects.create(
                medicamento=self.medicamento, registrado_por=self.docente,
                numero_lote=numero, vence_el="2099-01-01", unidades=4,
            )
        self.client.force_login(self.superusuario)
        ruta = reverse("admin:FarmaTEFApp_loteinventario_change", args=[lote.pk])
        datos = {**self.datos_lote("AMOx-002"), "unidades": 5}
        self.assertEqual(self.client.post(ruta, datos).status_code, 302)
        lote.refresh_from_db()
        self.assertEqual(lote.numero_lote, "AMOx-002")
        self.assertEqual(lote.unidades, 5)

    def test_estudiante_no_puede_registrar_lote_por_url_directa(self):
        self.client.force_login(usuario("lotes-estudiante"))
        self.assertEqual(self.post_inventario("AMOx-001").status_code, 403)
        self.assertFalse(self.medicamento.lotes.exists())


class InventarioAlertasTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.docente = usuario("alertas-docente", "MANAGER")
        cls.otro = usuario("alertas-otro", "MANAGER")
        cls.bajo = Medicamento.objects.create(
            nombre="Solución alfa", clasificacion="Analgésicos", creado_por=cls.docente, stock_minimo=3,
        )
        cls.vencimiento = Medicamento.objects.create(
            nombre="Solución beta", clasificacion="Antisépticos", creado_por=cls.docente,
            stock_minimo=3, dias_alerta_vencimiento=5,
        )
        cls.inactivo = Medicamento.objects.create(
            nombre="Registro desactivado", activo=False, creado_por=cls.docente, stock_minimo=4,
        )
        cls.ajeno = Medicamento.objects.create(
            nombre="Producto reservado", creado_por=cls.otro, stock_minimo=10,
        )
        hoy = timezone.localdate()
        for med, dias, unidades in (
            (cls.bajo, -1, 20), (cls.bajo, 0, 0),
            (cls.vencimiento, 0, 1), (cls.vencimiento, 5, 2),
            (cls.inactivo, 1, 1), (cls.ajeno, 1, 1),
        ):
            LoteInventario.objects.create(
                medicamento=med, numero_lote=f"QA-{dias}", vence_el=hoy + timedelta(days=dias),
                unidades=unidades, registrado_por=med.creado_por,
            )

    def test_alertas_coinciden_con_resultados_y_permisos(self):
        inventario = reverse("farmatef:inventario")
        for actor, bajos, proximos in (
            (self.docente, [self.bajo], [self.vencimiento]),
            (usuario("alertas-sin-existencias", "MANAGER"), [], []),
            (usuario("alertas-admin", "ADMIN"), [self.ajeno, self.bajo], [self.ajeno, self.vencimiento]),
            (usuario("alertas-super", None, is_superuser=True), [self.ajeno, self.bajo], [self.ajeno, self.vencimiento]),
        ):
            with self.subTest(actor=actor):
                self.client.force_login(actor)
                portada = self.client.get(reverse("farmatef"))
                self.assertNotContains(portada, "Flujo de farmacia")
                for alerta, esperados in zip(portada.context["alertas"], (bajos, proximos)):
                    self.assertEqual(alerta["total"], len(esperados))
                    enlace = f'{inventario}?alerta={alerta["tipo"]}'
                    self.assertContains(portada, enlace)
                    self.assertCountEqual(self.client.get(enlace).context["medicamentos"], esperados)

    def test_filtrar_y_registrar_son_recorridos_separados(self):
        inventario = reverse("farmatef:inventario")
        registro = reverse("farmatef:registro_inventario")
        self.assertEqual(self.client.get(registro).status_code, 302)
        self.client.force_login(usuario("alertas-alumno"))
        self.assertEqual(self.client.get(inventario).status_code, 403)
        self.assertEqual(self.client.post(registro, {"crear_medicamento": ""}).status_code, 403)
        self.client.force_login(self.docente)
        response = self.client.get(inventario, {"q": "solucion", "clasificacion": "Analgésicos"})
        self.assertEqual(response.context["medicamentos"], [self.bajo])
        self.assertNotContains(response, 'name="crear_medicamento"')
        self.assertContains(self.client.get(registro), 'name="crear_medicamento"')
        data = {
            "crear_medicamento": "", "medicamento-nombre": "Producto nuevo",
            "medicamento-stock_minimo": 4, "medicamento-dias_alerta_vencimiento": 10,
        }
        self.assertRedirects(self.client.post(registro, data), inventario)
        nuevo = Medicamento.objects.get(nombre="Producto nuevo", creado_por=self.docente)
        repetido = self.client.post(inventario, data)
        self.assertTemplateUsed(repetido, "pages/farmatef/registro_inventario.html")
        self.assertFormError(repetido.context["form_medicamento"], "nombre", "Ya registraste un medicamento con ese nombre.")
        lote = {
            "crear_lote": "", "lote-medicamento": self.ajeno.pk, "lote-numero_lote": "PRUEBA",
            "lote-unidades": 6, "lote-vence_el": "2099-01-01",
        }
        self.assertTrue(self.client.post(registro, lote).context["form_lote"].errors["medicamento"])
        lote["lote-medicamento"] = nuevo.pk
        self.assertRedirects(self.client.post(registro, lote), inventario)
        self.assertEqual(nuevo.stock_disponible, 6)

    def test_codigo_largo_requiere_ancho_suficiente(self):
        lote = self.bajo.lotes.first()
        self.bajo.codigo_barras = "A" * 40
        self.bajo.save(update_fields=["codigo_barras"])
        self.client.force_login(self.docente)
        url = reverse("farmatef:etiquetado")
        data = {"medicamento": self.bajo.pk, "lote": lote.pk, "ancho_mm": 55, "alto_mm": 55, "copias": 1}
        self.assertTrue(self.client.post(url, data).context["form"].errors["ancho_mm"])
        parcial = self.client.post(url, data, HTTP_X_LABEL_PREVIEW="1")
        self.assertTemplateUsed(parcial, "pages/farmatef/_etiqueta_preview.html")
        self.assertContains(parcial, "para imprimir este código de barras")
        self.assertNotContains(parcial, "data-print-button")
        data["ancho_mm"] = 150
        self.assertContains(self.client.post(url, data), "data:image/png;base64,")
        parcial = self.client.post(url, data, HTTP_X_LABEL_PREVIEW="1")
        self.assertContains(parcial, "data:image/png;base64,")
        self.assertNotContains(parcial, 'id="etiquetado-form"')
        self.client.force_login(self.otro)
        self.assertNotContains(self.client.post(url, data, HTTP_X_LABEL_PREVIEW="1"), "data-print-button")


class PracticaConInventarioTests(TestCase):
    def setUp(self):
        self.docente = usuario("docente-practica", "MANAGER")
        self.alumno = usuario("alumno-practica")
        self.otro_alumno = usuario("otro-alumno-practica")
        externo = usuario("docente-externo", "MANAGER")
        curso = Curso.objects.create(nombre="Farmacia de práctica", creado_por=self.docente)
        curso.estudiantes.add(self.alumno, self.otro_alumno)
        self.receta = Receta.objects.create(
            numero="PRACTICA-23", persona_ficticia="Paciente ficticio",
            vence_el="2099-01-01", creado_por=self.docente, curso=curso,
        )
        self.lote = self.crear_lote(self.docente, "Producto indicado", "LOTE-INDICADO", 8)
        self.alternativa = self.crear_lote(self.docente, "Producto alternativo", "LOTE-ALTERNATIVO", 7)
        self.ajeno = self.crear_lote(externo, "Producto privado", "LOTE-AJENO", 100)
        self.linea = RecetaLinea.objects.create(receta=self.receta, medicamento=self.lote.medicamento, unidades=5)
        self.campo = f"lote_{self.linea.pk}"
        self.detalle = reverse("farmatef:practica_receta", args=[self.receta.pk])
        self.responder = reverse("farmatef:responder_receta", args=[self.receta.pk])
        self.client.force_login(self.alumno)

    @staticmethod
    def crear_lote(docente, nombre, numero, unidades):
        medicamento = Medicamento.objects.create(nombre=nombre, creado_por=docente)
        return LoteInventario.objects.create(
            medicamento=medicamento, registrado_por=docente, numero_lote=numero,
            vence_el="2099-01-01", unidades=unidades,
        )

    def test_busqueda_docente_parcial_y_detalle_conservan_el_ambito(self):
        url = reverse("farmatef:recetas")
        con_prefijo = Receta.objects.create(
            numero="PRACTICA-23-B", persona_ficticia="Segundo alias",
            vence_el="2099-01-01", creado_por=self.docente, curso=self.receta.curso,
        )
        ajena = Receta.objects.create(
            numero="PRACTICA-23-AJENA", persona_ficticia="Alias reservado",
            vence_el="2099-01-01", creado_por=self.ajeno.medicamento.creado_por,
        )
        self.assertEqual(self.client.get(url, {"q": "PRACTICA"}).status_code, 403)
        self.client.force_login(self.docente)

        resultados = self.client.get(url, {"q": " practICA-23 "})
        self.assertEqual(
            resultados.context["coincidencias"],
            [{"numero": self.receta.numero}, {"numero": con_prefijo.numero}],
        )
        self.assertNotContains(resultados, ajena.numero)
        self.assertNotContains(resultados, 'id="detalle-receta"')
        seleccion = self.client.get(url, {"q": "PRACTICA-23", "numero": con_prefijo.numero})
        self.assertEqual(seleccion.context["receta"], con_prefijo)
        self.assertEqual(seleccion.context["coincidencias"], resultados.context["coincidencias"])
        self.assertContains(seleccion, 'id="detalle-receta"')
        self.assertContains(seleccion, "Segundo alias")
        for numero, receta in ((self.receta.numero, self.receta), (ajena.numero, None)):
            self.assertEqual(self.client.get(url, {"numero": numero}).context["receta"], receta)
        self.assertContains(self.client.get(url, {"q": "INEXISTENTE"}), "No hay recetas que coincidan")

    def test_busqueda_y_catalogo_limitados_a_la_practica(self):
        Medicamento.objects.filter(pk=self.lote.medicamento_id).update(
            concentracion="20 mg", forma_farmaceutica="Tableta", principio_activo="Principio QA",
        )
        listado = reverse("farmatef:practica_recetas")
        self.assertContains(self.client.get(listado, {"numero": "practica-23"}), self.detalle)
        self.assertNotContains(self.client.get(listado, {"numero": "OTRO"}), self.detalle)
        response = self.client.get(self.detalle)
        self.assertContains(response, f'aria-describedby="indicacion-{self.linea.pk}"')
        self.assertContains(response, 'data-medicine-title="Producto indicado · 20 mg · Tableta"')
        self.assertContains(response, "En la receta: <strong>Producto indicado</strong> · 20 mg · Tableta · <strong>5 unidades</strong>")
        self.assertContains(response, "LOTE-ALTERNATIVO")
        self.assertContains(response, f'data-medicine-label-code="FT-{self.lote.medicamento_id}"')
        self.assertNotContains(response, "LOTE-AJENO")
        self.client.force_login(usuario("no-matriculado"))
        self.assertEqual(self.client.get(self.detalle).status_code, 404)

    def test_dispensacion_correcta_imprime_solo_el_lote_usado(self):
        otro_lote = LoteInventario.objects.create(
            medicamento=self.lote.medicamento, registrado_por=self.docente,
            numero_lote="LOTE-ANTERIOR", vence_el="2098-01-01", unidades=12,
        )
        data = {"decision": "DISPENSAR", self.campo: self.lote.pk}
        self.assertRedirects(self.client.post(self.responder, data), self.detalle)
        self.lote.refresh_from_db()
        otro_lote.refresh_from_db()
        self.assertEqual(self.lote.unidades, 3)
        self.assertEqual(otro_lote.unidades, 12)
        uso = DispensacionLote.objects.get(lote=self.lote)
        etiqueta = reverse("farmatef:etiqueta_dispensacion", args=[uso.pk])
        self.assertContains(self.client.get(self.detalle), etiqueta)
        listado = reverse("farmatef:mis_etiquetas")
        self.assertContains(self.client.get(reverse("farmatef:practica_recetas")), listado)
        self.assertContains(self.client.get(listado), etiqueta)
        self.assertContains(self.client.get(etiqueta), "data:image/png;base64,")
        preview = self.client.post(etiqueta, {
            "medicamento": self.ajeno.medicamento_id, "lote": self.ajeno.pk,
            "ancho_mm": 55, "alto_mm": 44, "copias": 1,
        })
        self.assertContains(preview, "Unidades dispensadas: 5")
        self.assertNotContains(preview, "LOTE-AJENO")
        comprobante = reverse("farmatef:comprobante_dispensacion", args=[uso.dispensacion_id])
        self.assertContains(self.client.get(self.detalle), comprobante)
        for _ in range(2):
            pdf = self.client.get(comprobante)
            self.assertEqual(pdf["Content-Type"], "application/pdf")
            self.assertEqual(pdf["Cache-Control"], "private, no-store")
            self.assertTrue(b"".join(pdf.streaming_content).startswith(b"%PDF"))
        self.client.post(self.responder, data)
        self.lote.refresh_from_db()
        self.assertEqual(self.lote.unidades, 3)
        self.client.force_login(self.otro_alumno)
        self.assertNotContains(self.client.get(listado), etiqueta)
        self.assertEqual(self.client.get(etiqueta).status_code, 404)
        self.assertEqual(self.client.get(comprobante).status_code, 404)
        self.receta.curso.estudiantes.remove(self.alumno)
        self.client.force_login(self.alumno)
        self.assertNotContains(self.client.get(listado), etiqueta)
        self.assertEqual(self.client.get(etiqueta).status_code, 404)


    def test_lote_ajeno_se_rechaza_y_alternativo_se_evalua_como_error(self):
        response = self.client.post(self.responder, {"decision": "DISPENSAR", self.campo: self.ajeno.pk})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(RespuestaReceta.objects.exists())
        self.client.post(self.responder, {"decision": "DISPENSAR", self.campo: self.alternativa.pk})
        self.assertFalse(RespuestaReceta.objects.get().correcta)
        self.assertFalse(DispensacionLote.objects.exists())
        self.lote.refresh_from_db()
        self.assertEqual(self.lote.unidades, 8)

    def test_falta_de_stock_es_una_respuesta_evaluable(self):
        LoteInventario.objects.filter(pk=self.lote.pk).update(unidades=4)
        self.assertRedirects(self.client.post(self.responder, {
            "decision": "RECHAZAR", "motivo_rechazo": "SIN_STOCK",
        }), self.detalle)
        self.assertTrue(RespuestaReceta.objects.get().correcta)
        self.assertFalse(DispensacionLote.objects.exists())

    def test_segunda_linea_sin_stock_no_descuenta_la_primera(self):
        segunda = RecetaLinea.objects.create(
            receta=self.receta, medicamento=self.alternativa.medicamento, unidades=8,
        )
        data = {
            "decision": "DISPENSAR", self.campo: self.lote.pk,
            f"lote_{segunda.pk}": self.alternativa.pk,
        }
        self.assertRedirects(self.client.post(self.responder, data), self.detalle)
        self.assertFalse(RespuestaReceta.objects.get().correcta)
        self.assertFalse(DispensacionLote.objects.exists())
        self.lote.refresh_from_db()
        self.alternativa.refresh_from_db()
        self.assertEqual((self.lote.unidades, self.alternativa.unidades), (8, 7))

    def test_reintento_corrige_sin_revelar_respuesta_ni_repetir_descuento(self):
        Receta.objects.filter(pk=self.receta.pk).update(pista_estudiante="Revisa la presentación.")
        primer = {"decision": "DISPENSAR", self.campo: self.alternativa.pk, "intento": 1}
        self.assertRedirects(self.client.post(self.responder, primer), self.detalle)
        vista = self.client.get(self.detalle)
        self.assertContains(vista, "Te queda un intento")
        self.assertContains(vista, "Revisa la presentación.")
        self.assertNotContains(vista, "Ver respuesta esperada")
        self.assertNotContains(vista, "Descargar comprobante")
        self.assertEqual(vista.context["form"]["intento"].value(), 2)
        self.client.post(self.responder, primer)
        self.assertEqual(RespuestaReceta.objects.count(), 1)
        self.lote.refresh_from_db()
        self.assertEqual(self.lote.unidades, 8)

        segundo = {"decision": "DISPENSAR", self.campo: self.lote.pk, "intento": 2}
        self.assertRedirects(self.client.post(self.responder, segundo), self.detalle)
        self.assertContains(self.client.get(self.detalle), "Descargar comprobante PDF")
        self.client.post(self.responder, segundo)
        self.assertEqual(list(RespuestaReceta.objects.order_by("intento").values_list("correcta", flat=True)), [False, True])
        self.lote.refresh_from_db()
        self.assertEqual(self.lote.unidades, 3)

    def test_otro_motivo_exige_explicacion_y_la_guarda_en_el_intento(self):
        Receta.objects.filter(pk=self.receta.pk).update(motivo_rechazo_esperado="OTRO")
        data = {"decision": "RECHAZAR", "motivo_rechazo": "OTRO"}
        for texto in ("", "   ", "a" * 301):
            response = self.client.post(self.responder, {**data, "explicacion_otro_motivo": texto})
            self.assertTrue(response.context["form"]["explicacion_otro_motivo"].errors)
            self.assertFalse(RespuestaReceta.objects.exists())

        texto = "La instrucción de la receta simulada requiere aclaración."
        self.assertRedirects(self.client.post(self.responder, {
            **data, "explicacion_otro_motivo": f"  {texto}  ",
        }), self.detalle)
        respuesta = RespuestaReceta.objects.get()
        self.assertEqual(respuesta.explicacion_otro_motivo, texto)
        self.assertTrue(respuesta.correcta)
        self.assertFalse(Dispensacion.objects.exists())
        self.assertContains(self.client.get(self.detalle), texto)
        self.client.force_login(self.docente)
        self.assertContains(self.client.get(reverse("farmatef:intentos_receta", args=[self.receta.pk])), texto)

    def test_motivo_predefinido_no_almacena_explicacion_de_otro(self):
        data = {
            "decision": "RECHAZAR", "motivo_rechazo": "DATOS_INCONSISTENTES",
            "explicacion_otro_motivo": "Texto residual",
        }
        self.assertRedirects(self.client.post(self.responder, data), self.detalle)
        self.assertEqual(RespuestaReceta.objects.get().explicacion_otro_motivo, "")

    def test_dos_errores_muestran_explicacion_sin_emitir_documentos(self):
        for intento in (1, 2):
            self.assertRedirects(self.client.post(self.responder, {
                "decision": "DISPENSAR", self.campo: self.alternativa.pk, "intento": intento,
            }), self.detalle)
        vista = self.client.get(self.detalle)
        self.assertContains(vista, "En la línea 1, el producto o la presentación elegida difiere de la receta.")
        self.assertContains(vista, "Ver respuesta esperada")
        self.assertNotContains(vista, "Confirmar decisión")
        self.assertNotContains(vista, "Descargar comprobante")
        self.assertFalse(DispensacionLote.objects.exists())

        intentos_url = reverse("farmatef:intentos_receta", args=[self.receta.pk])
        self.assertEqual(self.client.get(intentos_url).status_code, 403)
        self.client.force_login(self.ajeno.medicamento.creado_por)
        self.assertEqual(self.client.get(intentos_url).status_code, 404)
        self.client.force_login(self.docente)
        lista = self.client.get(reverse("farmatef:recetas"), {"numero": self.receta.numero})
        self.assertContains(lista, intentos_url)
        self.assertNotContains(lista, "Motivo de rechazo")
        pagina = self.client.get(intentos_url)
        self.assertContains(pagina, "Incorrecta", count=2)
        self.assertNotContains(pagina, "Registrar receta para simulación")

    def test_receta_y_etiqueta_conservan_dosis_e_indicaciones(self):
        self.client.force_login(self.docente)
        self.assertEqual(self.client.post(reverse("farmatef:recetas"), {
            "numero": "PRACTICA-DO-24", "persona_ficticia": "Paciente simulado", "vence_el": "2099-01-01",
            "curso": self.receta.curso_id, "form-TOTAL_FORMS": "1", "form-INITIAL_FORMS": "0",
            "form-0-medicamento": self.lote.medicamento_id, "form-0-unidades": "4",
            "form-0-dosis": "Dosis A", "form-0-indicaciones": "Indicación de prueba",
        }).status_code, 302)
        receta = Receta.objects.get(numero="PRACTICA-DO-24")
        linea = receta.lineas.get()
        self.client.force_login(self.alumno)
        self.client.post(reverse("farmatef:responder_receta", args=[receta.pk]), {
            "decision": "DISPENSAR", f"lote_{linea.pk}": self.lote.pk, "intento": 1,
        })
        uso = DispensacionLote.objects.get(linea=linea)
        preview = self.client.post(reverse("farmatef:etiqueta_dispensacion", args=[uso.pk]), {
            "ancho_mm": 55, "alto_mm": 44, "copias": 1,
        })
        self.assertContains(preview, "Dosis ficticia: Dosis A")
        self.assertContains(preview, "Indicación de prueba")


@skipUnless(connection.vendor == "postgresql", "El bloqueo por fila requiere PostgreSQL.")
class DispensacionConcurrenteTests(TransactionTestCase):
    def test_dos_recetas_compiten_por_el_mismo_lote(self):
        docente = usuario("qa-concurrencia", "MANAGER")
        med = Medicamento.objects.create(nombre="Producto QA", creado_por=docente)
        lote = LoteInventario.objects.create(
            medicamento=med, numero_lote="QA", vence_el="2099-01-01", unidades=7, registrado_por=docente,
        )
        lineas = [
            RecetaLinea.objects.create(
                receta=Receta.objects.create(
                    numero=f"CONC-{n}", persona_ficticia="Persona QA", vence_el="2099-01-01", creado_por=docente,
                ),
                medicamento=med,
                unidades=5,
            )
            for n in range(2)
        ]
        inicio = Barrier(2, timeout=10)

        def dispensar(linea):
            try:
                inicio.wait()
                entregar_receta(linea.receta_id, docente, {linea.pk: 5})
                return "confirmada"
            except ValidationError as exc:
                return exc.messages[0]
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as ejecutor:
            resultados = list(ejecutor.map(dispensar, lineas))
        self.assertEqual(resultados.count("confirmada"), 1)
        self.assertTrue(any("Stock insuficiente" in resultado for resultado in resultados))
        lote.refresh_from_db()
        self.assertEqual(lote.unidades, 2)
        self.assertEqual(Dispensacion.objects.count(), 1)
        self.assertEqual(DispensacionLote.objects.get().unidades, 5)
        self.assertCountEqual(RecetaLinea.objects.values_list("unidades_entregadas", flat=True), [0, 5])
