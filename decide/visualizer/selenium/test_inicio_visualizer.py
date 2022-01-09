from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from base.tests import BaseTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from django.conf import settings

class TestTestcrearpregunta(StaticLiveServerTestCase):
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
  
  def test_acceso_resultados_votacion_por_inicio_visualizer(self):
    self.driver.get("{}/visualizer".format(self.live_server_url))
    self.driver.implicitly_wait(2)
    self.driver.set_window_size(1848, 1016)
    self.driver.find_element(By.CSS_SELECTOR, "a").click()
    self.driver.implicitly_wait(2)
    elements = self.driver.find_elements(By.CSS_SELECTOR, "button")
    self.driver.implicitly_wait(2)
    assert len(elements) > 0


    
