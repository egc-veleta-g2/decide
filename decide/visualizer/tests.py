#Imports de Visualizer
from django.conf import settings
from base.tests import BaseTestCase
import visualizer.views as vw

#Imports de Selenium
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class VisualizerTestCase(BaseTestCase):
    fixtures = ['visualizer/migrations/datos_prueba.json', ]

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()


    def test_obtener_resultado_votacion_no_existe(self):
        response = self.client.get('/visualizer/10000/')
        self.assertEqual(response.status_code, 404)
    
    def test_obtener_resultado_votacion_existe(self):
        response = self.client.get('/visualizer/1/')
        self.assertEqual(response.status_code, 200)

    #TESTS DE PÁGINA INICIO VISUALIZER
    #Para que funcione, es necesario eliminar linea staticfiles del settings
    def test_acceso_inicio_visualizer(self):
         response = self.client.get('/visualizer/')
         self.assertEqual(response.status_code, 200)

    #TESTS DE FUNCIONES AUXILIARES DE VIEWS.PY
    def test_date_comparer(self):
        fecha1 = "2021-12-18T10:48:22.969419Z"
        fecha2 = "2021-12-18T11:07:51.009086Z"
        resultado = "0 días, 0 horas, 19 minutos y 28 segundos "
        diferencia = vw.dateComparer(fecha1, fecha2)[0]
        self.assertEqual(diferencia, resultado)
    
class VisualizerTestCaseSelenium(BaseTestCase):
    fixtures = ['visualizer/migrations/datos_prueba.json', ]

    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = False
        self.driver = webdriver.Chrome(options=options)
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    #def test_texto_inicio_visualizer(self):                    
    #    self.driver.get(f'{self.live_server_url}/visualizer/')
    #    self.assertTrue(self.driver.find_element(By.CSS_SELECTOR,"h1")== "¡Bienvenidos a los resultados de las votaciones en Decide!")
    def test_update_voting_400(self):
        v = self.create_voting()
        data = {} #El campo action es requerido en la request
        self.login()
        response = self.client.put('/voting/{}/'.format(v.pk), data, format= 'json')
        self.assertEquals(response.status_code, 400)
    

