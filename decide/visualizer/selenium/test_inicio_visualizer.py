from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from base.tests import BaseTestCase
from selenium.webdriver.common.by import By

class TestInicioVisualizerDatos(StaticLiveServerTestCase):
  fixtures = ['visualizer/migrations/datos_prueba.json', ]
  def setUp(self):
    options = webdriver.ChromeOptions()
    options.headless = False
    self.base = BaseTestCase()
    self.base.setUp()
    self.driver = webdriver.Chrome(options=options)
    self.vars = {}


  def tearDown(self):
    self.driver.quit()
 
  def test_texto_acceso_inicio_visualizer_correcto(self):
    self.driver.get("{}/visualizer".format(self.live_server_url))
    self.driver.implicitly_wait(2)
    a= self.driver.find_element(By.CSS_SELECTOR,'h1').get_attribute("innerHTML")
    self.driver.implicitly_wait(2)
    self.assertEquals(a,'¡Bienvenidos a los resultados de las votaciones en Decide!')

  def test_acceso_visualizer_desde_inicio(self):
    self.driver.get("{}".format(self.live_server_url))
    self.driver.set_window_size(1848, 1016)
    self.driver.implicitly_wait(2)
    self.driver.find_element(By.LINK_TEXT, "Visualización").click()
    self.driver.implicitly_wait(2)
    elements = self.driver.find_elements(By.CSS_SELECTOR, "h1")
    assert len(elements) > 0
    elements = self.driver.find_elements(By.CSS_SELECTOR, "th:nth-child(2)")
    assert len(elements) > 0
  
  def test_tabla_metricas_existe(self):
    self.driver.get("{}/visualizer".format(self.live_server_url))
    self.driver.set_window_size(1848, 1016)
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    elements = self.driver.find_elements(By.CSS_SELECTOR, ".heading")
    assert len(elements) > 0
    elements = self.driver.find_elements(By.CSS_SELECTOR, "tr:nth-child(1) > .table-dark")
    assert len(elements) > 0

  def test_acceso_resultados_votacion_por_inicio_visualizer(self):
    self.driver.get("{}/visualizer".format(self.live_server_url))
    self.driver.implicitly_wait(2)
    self.driver.set_window_size(1848, 1016)
    self.driver.find_element(By.CSS_SELECTOR, "a").click()
    self.driver.implicitly_wait(2)
    elements = self.driver.find_elements(By.CSS_SELECTOR, "button")
    self.driver.implicitly_wait(2)
    assert len(elements) > 0

class TestInicioVisualizerSinDatos(StaticLiveServerTestCase):

  def setUp(self):
    options = webdriver.ChromeOptions()
    options.headless = False
    self.base = BaseTestCase()
    self.base.setUp()
    self.driver = webdriver.Chrome(options=options)
    self.vars = {}


  def tearDown(self):
    self.driver.quit()

  def test_no_datos_votaciones(self):
    self.driver.get("{}/visualizer".format(self.live_server_url))
    self.driver.implicitly_wait(2)
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    self.driver.implicitly_wait(4)
    self.assertIsNotNone(self.driver.find_element_by_id("novotaciones"))