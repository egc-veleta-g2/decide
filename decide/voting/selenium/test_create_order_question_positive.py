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

class TestCreateOrderQuestionPositive(StaticLiveServerTestCase):
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

    def test_crearPreguntaPorOrdenPreferencia(self):
      url = settings.BASEURL
      self.driver.get(str(url)+"/admin/login/?next=/admin/")
      self.driver.set_window_size(909, 1016)
      self.driver.find_element(By.ID, "id_username").send_keys("lizesqsaa")
      self.driver.find_element(By.ID, "id_password").send_keys("lizesqsaa1")
      self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
      time.sleep(2)
      self.driver.find_element(By.LINK_TEXT, "Questions").click()
      self.driver.find_element(By.CSS_SELECTOR, ".addlink").click()
      dropdown = self.driver.find_element(By.ID, "id_option_types")
      dropdown.find_element(By.XPATH, "//option[. = 'Rank order']").click()
      element = self.driver.find_element(By.ID, "id_option_types")
      actions = ActionChains(self.driver)
      actions.move_to_element(element).click_and_hold().perform()
      element = self.driver.find_element(By.ID, "id_option_types")
      actions = ActionChains(self.driver)
      actions.move_to_element(element).perform()
      element = self.driver.find_element(By.ID, "id_option_types")
      actions = ActionChains(self.driver)
      actions.move_to_element(element).release().perform()
      self.driver.find_element(By.ID, "id_desc").click()
      self.driver.find_element(By.ID, "id_desc").send_keys("elige por orden de preferencia")
      self.driver.find_element(By.ID, "id_options-0-number").send_keys("0")
      self.driver.find_element(By.ID, "id_options-0-number").click()
      self.driver.find_element(By.CSS_SELECTOR, ".field-type > div").click()
      dropdown = self.driver.find_element(By.ID, "id_type")
      dropdown.find_element(By.XPATH, "//option[. = 'BORDA']").click()
      element = self.driver.find_element(By.ID, "id_type")
      actions = ActionChains(self.driver)
      actions.move_to_element(element).click_and_hold().perform()
      element = self.driver.find_element(By.ID, "id_type")
      actions = ActionChains(self.driver)
      actions.move_to_element(element).perform()
      element = self.driver.find_element(By.ID, "id_type")
      actions = ActionChains(self.driver)
      actions.move_to_element(element).release().perform()
      self.driver.find_element(By.ID, "id_options-0-number").click()
      self.driver.find_element(By.ID, "id_options-0-number").send_keys("1")
      self.driver.find_element(By.ID, "id_options-0-option").click()
      self.driver.find_element(By.ID, "id_options-0-option").send_keys("rojo")
      self.driver.find_element(By.ID, "id_options-1-number").click()
      self.driver.find_element(By.ID, "id_options-1-number").send_keys("2")
      self.driver.find_element(By.ID, "id_options-1-option").click()
      self.driver.find_element(By.ID, "id_options-1-option").send_keys("amarillo")
      self.driver.find_element(By.ID, "id_options-2-number").click()
      self.driver.find_element(By.ID, "id_options-2-number").send_keys("3")
      self.driver.find_element(By.ID, "id_options-2-option").click()
      self.driver.find_element(By.ID, "id_options-2-option").send_keys("azul")
      time.sleep(3)
      self.driver.find_element(By.NAME, "_save").click()
      self.driver.find_element(By.CSS_SELECTOR, "html").click()
      self.driver.find_element(By.CSS_SELECTOR, "html").click()