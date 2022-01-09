from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from base.tests import BaseTestCase
from selenium.webdriver.common.by import By

class TestTestgraficas(StaticLiveServerTestCase):
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

    def test_docu(self):
        self.driver.get("{}".format(self.live_server_url))
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.LINK_TEXT, "Documentación").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".title").text == "Decide API"