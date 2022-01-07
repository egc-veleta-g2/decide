from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from base.tests import BaseTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from django.conf import settings

class testPaginaPrincipal(StaticLiveServerTestCase):

  def setUp(self):
    options = webdriver.ChromeOptions()
    options.headless = False
    self.base = BaseTestCase()
    self.base.setUp()
    self.driver = webdriver.Chrome(options=options)
    self.vars = {}


  def tearDown(self):
    self.driver.quit()

  
  def test_comprobarAdministracion(self):
    self.driver.get("{}".format(self.live_server_url))
    self.driver.set_window_size(1294, 704)
    self.driver.find_element(By.LINK_TEXT, "Administración").click()
    elements = self.driver.find_elements(By.LINK_TEXT, "Django administration")
    assert len(elements) > 0

  
  def test_comprobarDocumentacion(self):
    self.driver.get("{}".format(self.live_server_url))
    self.driver.set_window_size(1294, 704)
    self.driver.find_element(By.LINK_TEXT, "Documentación").click()
    elements = self.driver.find_elements(By.CSS_SELECTOR, "span:nth-child(2)")
    assert len(elements) > 0
  
  
  def test_comprobarCabina(self):
    self.driver.get("{}".format(self.live_server_url))
    self.driver.set_window_size(1294, 704)
    self.driver.find_element(By.LINK_TEXT, "Cabina").click()
    elements = self.driver.find_elements(By.LINK_TEXT, "Bienvenido/a a la cabina de votación")
    assert len(elements) > 0
  
  
  def test_estilosFuncionan(self):
    self.driver.get("{}".format(self.live_server_url))
    self.driver.set_window_size(1294, 704)
    elements = self.driver.find_elements(By.ID, "nav-collapse")
    assert len(elements) > 0
    elements = self.driver.find_elements(By.CSS_SELECTOR, ".copyright")
    assert len(elements) > 0
    elements = self.driver.find_elements(By.CSS_SELECTOR, "h1")
    assert len(elements) > 0
    elements = self.driver.find_elements(By.CSS_SELECTOR, ".col-6:nth-child(1) h3")
    assert len(elements) > 0
    elements = self.driver.find_elements(By.CSS_SELECTOR, ".col-6:nth-child(2) h3")
    assert len(elements) > 0
    elements = self.driver.find_elements(By.LINK_TEXT, "Visualización")
    assert len(elements) > 0
    elements = self.driver.find_elements(By.LINK_TEXT, "Cabina")
    assert len(elements) > 0
    elements = self.driver.find_elements(By.LINK_TEXT, "Documentación")
    assert len(elements) > 0
    elements = self.driver.find_elements(By.LINK_TEXT, "Administración")
    assert len(elements) > 0
  
  