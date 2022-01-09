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

    def test_grafica_barras(self):
        self.driver.get("{}".format(self.live_server_url))
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.LINK_TEXT, "Visualización").click()
        self.driver.find_element(By.LINK_TEXT, "Saber sobre ti").click()
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .btn").click()
        elements = self.driver.find_elements(By.ID, "bar-resultados")
        assert len(elements) > 0

    def test_grafica_pie_porcentaje(self):
        self.driver.get("{}".format(self.live_server_url))
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.LINK_TEXT, "Visualización").click()
        self.driver.find_element(By.LINK_TEXT, "Saber sobre ti").click()
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .btn").click()
        elements = self.driver.find_elements(By.ID, "pie-porcentaje")
        assert len(elements) > 0

    def test_tabla_estadisitcas(self):
        self.driver.get("{}".format(self.live_server_url))
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.LINK_TEXT, "Visualización").click()
        self.driver.find_element(By.LINK_TEXT, "Saber sobre ti").click()
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .btn").click()
        assert self.driver.find_element(By.ID, "titulo_metricas").text == "Métricas"

    def test_titulo_votacion(self):
        self.driver.get("{}".format(self.live_server_url))
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.LINK_TEXT, "Visualización").click()
        self.driver.find_element(By.LINK_TEXT, "Saber sobre ti").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "h1").text == "Saber sobre ti"

    def test_titulo_votacion_2(self):
        self.driver.get("{}".format(self.live_server_url))
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.LINK_TEXT, "Visualización").click()
        self.driver.find_element(By.LINK_TEXT, "Lugares").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "h1").text == "Lugares"
