import time
# import json

#from django.conf import settings
from base.tests import BaseTestCase
# from django.urls import reverse
import visualizer.views as vw
# from voting.models import Voting
# from base import mods


class VisualizerTestCase(BaseTestCase):
    fixtures = ['visualizer/migrations/datos_prueba.json', ]

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    # def test_obtener_inicio_visualizer(self):
    #     response = self.client.get('/visualizer/')
    #     self.assertEqual(response.status_code, 200)

    # def test_obtener_inicio_visualizer_votaciones(self):
    #     response = self.client.get('/visualizer/')
    #     votaciones_finalizadas = Voting.objects.filter(end_date__isnull=False, tally__isnull=False)
    #     self.assertEqual(response.context['vot_finalizadas'][0], votaciones_finalizadas[0])
    #     self.assertEqual(response.context['vot_finalizadas'][1], votaciones_finalizadas[1])

    def test_obtener_resultado_votacion_no_existe(self):
        response = self.client.get('/visualizer/10000/')
        self.assertEqual(response.status_code, 404)

    # def test_obtener_resultados_votacion(self):
    #     response = self.client.get('/visualizer/1/')
    #     self.assertEqual(response.context['voting'], json.dumps(mods.get('voting', params={'id': 1})[0]))

    def test_date_comparer(self):
        fecha1 = "2021-12-18T10:48:22.969419Z"
        fecha2 = "2021-12-18T11:07:51.009086Z"
        resultado = "0 días, 0 horas, 19 minutos y 28 segundos "
        diferencia = vw.dateComparer(fecha1, fecha2)[0]
        self.assertEqual(diferencia, resultado)