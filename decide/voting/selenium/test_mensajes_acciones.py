from selenium import webdriver
from selenium.webdriver.common.by import By
from base.tests import BaseTestCase
from selenium.webdriver.common.action_chains import ActionChains

class Testmensajesacciones():
  def setUp(self):
    options = webdriver.ChromeOptions()
    options.headless = False
    self.base = BaseTestCase()
    self.base.setUp()
    self.driver = webdriver.Chrome(options=options)
    self.vars = {}

  def tearDown(self):
    self.driver.quit()

  def test_testmensajesacciones(self):
    self.driver.get("http://localhost:8000/admin/login/?next=/admin/")
    self.driver.set_window_size(878, 1028)
    self.driver.find_element(By.ID, "id_username").send_keys("veleta")
    self.driver.find_element(By.ID, "id_password").send_keys("veleta2021")
    self.driver.find_element(By.CSS_SELECTOR, ".submit-row > input").click()
    self.driver.find_element(By.CSS_SELECTOR, ".model-question .addlink").click()
    self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(2) > label").click()
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(4)").click()
    self.driver.find_element(By.ID, "id_question_desc").click()
    self.driver.find_element(By.ID, "id_question_desc").send_keys("Prueba")
    self.driver.find_element(By.ID, "id_question_ratio_3").click()
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(6)").click()
    self.driver.find_element(By.LINK_TEXT, "Voting").click()
    self.driver.find_element(By.CSS_SELECTOR, ".model-voting .addlink").click()
    self.driver.find_element(By.ID, "id_name").send_keys("Votación de ejemplo")
    self.driver.find_element(By.ID, "id_desc").send_keys("Descripción")
    dropdown = self.driver.find_element(By.ID, "id_question")
    dropdown.find_element(By.XPATH, "//option[. = 'Prueba']").click()
    element = self.driver.find_element(By.ID, "id_question")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    element = self.driver.find_element(By.ID, "id_question")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.ID, "id_question")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    self.driver.find_element(By.ID, "id_url").click()
    self.driver.find_element(By.ID, "id_url").click()
    dropdown = self.driver.find_element(By.ID, "id_auths")
    dropdown.find_element(By.XPATH, "//option[. = 'http://localhost:8000']").click()
    self.driver.find_element(By.NAME, "_save").click()
    self.driver.find_element(By.ID, "container").click()
    self.driver.find_element(By.NAME, "_selected_action").click()
    dropdown = self.driver.find_element(By.NAME, "action")
    dropdown.find_element(By.XPATH, "//option[. = 'Reset']").click()
    element = self.driver.find_element(By.NAME, "action")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    element = self.driver.find_element(By.NAME, "action")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.NAME, "action")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    self.driver.find_element(By.NAME, "index").click()
    elements = self.driver.find_elements(By.XPATH, "//li[contains(.,\'Las votaciones [Votación de ejemplo] han sido reseteadas correctamente\')]")
    assert len(elements) > 0
    self.driver.find_element(By.NAME, "_selected_action").click()
    dropdown = self.driver.find_element(By.NAME, "action")
    dropdown.find_element(By.XPATH, "//option[. = 'Stop']").click()
    element = self.driver.find_element(By.NAME, "action")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    element = self.driver.find_element(By.NAME, "action")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.NAME, "action")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    self.driver.find_element(By.NAME, "index").click()
    elements = self.driver.find_elements(By.XPATH, "//li[contains(.,\'Las votaciones [Votación de ejemplo] no se pueden detener porque no han sido iniciadas anteriormente\')]")
    assert len(elements) > 0
    self.driver.find_element(By.NAME, "_selected_action").click()
    dropdown = self.driver.find_element(By.NAME, "action")
    dropdown.find_element(By.XPATH, "//option[. = 'Start']").click()
    element = self.driver.find_element(By.NAME, "action")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    element = self.driver.find_element(By.NAME, "action")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    element = self.driver.find_element(By.NAME, "action")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    self.driver.find_element(By.NAME, "index").click()
    elements = self.driver.find_elements(By.CSS_SELECTOR, ".info")
    assert len(elements) > 0
