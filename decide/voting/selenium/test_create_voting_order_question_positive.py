import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from base.tests import BaseTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from django.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.contrib.auth.models import User

class TestCreateVotingOrdenQuestionPositive(StaticLiveServerTestCase):
    def setUp(self):

      options = webdriver.ChromeOptions()
      options.headless = False
      self.base = BaseTestCase()
      self.base.setUp()
      self.driver = webdriver.Chrome(options=options)
      self.vars = {}
      super().setUp()

    def tearDown(self):
      super().tearDown()
      self.driver.quit()

      self.base.tearDown()

    def test_crearotoConPreguntaPorPreferencia(self):
      url = settings.BASEURL
      self.driver.get(str(url)+"/admin/login/?next=/admin/")
      self.driver.set_window_size(909, 1016)
      self.driver.find_element(By.ID, "id_username").send_keys("veleta")
      self.driver.find_element(By.ID, "id_password").send_keys("veleta2021")
      self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
      time.sleep(2)
      self.driver.find_element(By.LINK_TEXT, "Votings").click()
      self.driver.find_element(By.CSS_SELECTOR, ".addlink").click()
      self.driver.find_element(By.ID, "id_name").click()
      self.driver.find_element(By.ID, "id_name").send_keys("prueba selenium")
      self.driver.find_element(By.ID, "id_desc").click()
      self.driver.find_element(By.ID, "id_desc").click()
      self.driver.find_element(By.ID, "id_desc").send_keys("prueba")
      dropdown = self.driver.find_element(By.ID, "id_question")
      dropdown.find_element(By.XPATH, "//option[. = 'elige por orden de preferencia']").click()
      element = self.driver.find_element(By.ID, "id_question")
      actions = ActionChains(self.driver)
      actions.move_to_element(element).click_and_hold().perform()
      element = self.driver.find_element(By.ID, "id_question")
      actions = ActionChains(self.driver)
      actions.move_to_element(element).perform()
      element = self.driver.find_element(By.ID, "id_question")
      actions = ActionChains(self.driver)
      actions.move_to_element(element).release().perform()
      dropdown = self.driver.find_element(By.ID, "id_auths")
      dropdown.find_element(By.XPATH, "//option[. = 'http://localhost:8000']").click()
      self.driver.find_element(By.NAME, "_save").click()