#Imports de Visualizer
from django.conf import settings
import selenium
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
    
#class VisualizerTestCaseSelenium(BaseTestCase):

    #def test_texto_inicio_visualizer_correcto(self): 
        #options= webdriver.ChromeOptions()
        #options.headless = False
        #driver = webdriver.Chrome(options=options)                 
        #webdriver.Chrome.get(driver,f'{driver.current_url}/visualizer/')
        #driver.implicitly_wait(10)
        #webdriver.Chrome.find_element_by_class_name(driver,'col-md-8 offset-md-2 text-center')


