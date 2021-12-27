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

  def test_crearpregunta(self):
    url = settings.BASEURL
    self.driver.get(str(url)+"/admin/login/?next=/admin/")
    self.driver.set_window_size(909, 1016)
    self.driver.find_element(By.ID, "id_username").send_keys("veleta")
    self.driver.find_element(By.ID, "id_password").send_keys("veleta2021")
    self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
    self.driver.find_element(By.CSS_SELECTOR, ".model-question .addlink").click()
    self.driver.find_element(By.ID, "id_type_ratio_1").click()
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(4)").click()
    self.driver.find_element(By.ID, "id_question_desc").click()
    self.driver.find_element(By.ID, "id_question_desc").send_keys("Pregunta test selenium")
    self.driver.find_element(By.ID, "id_question_ratio_2").click()
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(6)").click()
    self.driver.find_element(By.LINK_TEXT, "Home").click()
    self.driver.find_element(By.CSS_SELECTOR, ".model-voting .addlink").click()
    self.driver.find_element(By.ID, "id_name").send_keys("Ejemplo selenium")
    self.driver.find_element(By.ID, "id_desc").click()
    self.driver.find_element(By.ID, "id_desc").send_keys("Ejemplo selenium")
    dropdown = self.driver.find_element(By.ID, "id_question")
    dropdown.find_element(By.XPATH, "//option[. = 'Pregunta test selenium']").click()
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
