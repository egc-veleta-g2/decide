from base.tests import BaseTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class TestTestiniciosinlogear(StaticLiveServerTestCase):
  def setUp(self):
    options = webdriver.ChromeOptions()
    options.headless = True
    self.base = BaseTestCase()
    self.base.setUp()
    self.driver = webdriver.Chrome(options=options)
    self.vars = {}


  def tearDown(self):
    self.driver.quit()

  def test_test_inicio_sin_logear(self):
    self.driver.get("http://localhost:8000/booth/inicio/")
    self.driver.find_element(By.ID, "alertButton").click()