from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from base.tests import BaseTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from django.conf import settings

class TestTestcrearpregunta(StaticLiveServerTestCase):

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
    a= self.driver.find_element(By.CSS_SELECTOR,'h1').get_attribute("innerHTML")
    self.assertEquals(a,'¡Bienvenidos a los resultados de las votaciones en Decide!')

  def test_acceso_visualizer_desde_inicio(self):
    self.driver.get("{}".format(self.live_server_url))
    self.driver.set_window_size(1848, 1016)
    self.driver.find_element(By.LINK_TEXT, "Visualización").click()
    elements = self.driver.find_elements(By.CSS_SELECTOR, "h1")
    assert len(elements) > 0
    elements = self.driver.find_elements(By.CSS_SELECTOR, "th:nth-child(2)")
    assert len(elements) > 0
  
  def test_estilo_presente_inicio_visualizer(self):
    self.driver.get("{}/visualizer".format(self.live_server_url))
    self.driver.set_window_size(1848, 1016)
    elements = self.driver.find_elements(By.ID, "nav-collapse")
    assert len(elements) > 0
    elements = self.driver.find_elements(By.CSS_SELECTOR, ".copyright")
    assert len(elements) > 0
  
  def test_acceso_resultados_votacion_por_inicio_visualizer(self):
    self.driver.get("{}/visualizer".format(self.live_server_url))
    self.driver.set_window_size(1848, 1016)
    self.driver.find_element(By.CSS_SELECTOR, "a").click()
    elements = self.driver.find_elements(By.CSS_SELECTOR, "button")
    assert len(elements) > 0


    
