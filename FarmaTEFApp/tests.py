from django.test import TestCase
from django.urls import reverse
from core.test_helpers import usuario
from .forms import EtiquetaLoteForm, LoteInventarioForm, RecetaLineaForm
from .models import Medicamento, LoteInventario


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
