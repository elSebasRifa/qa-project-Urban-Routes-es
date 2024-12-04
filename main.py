import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    taxi_button = (By.XPATH, '//button[text()="Pedir un taxi"]')
    comfort_tariff_button = (By.CSS_SELECTOR, 'button[data-for="tariff-card-4"]')
    phone_button = (By.CSS_SELECTOR, 'div.np-button div.np-text')
    phone_input = (By.ID, 'phone')
    next_button = (By.XPATH, '//button[text()="Siguiente"]')
    confirm_button = (By.XPATH, '//button[text()="Confirmar"]')
    payment_button = (By.CSS_SELECTOR, 'div.pp-text')
    add_card_option = (By.CSS_SELECTOR, 'div.pp-title')
    card_number_input = (By.ID, 'number')
    card_cvv_input = (By.ID, 'code')
    add_card_button = (By.XPATH, '//button[text()="Agregar"]')
    driver_message_input = (By.ID, 'comment')
    blanket_option = (By.XPATH, '//div[contains(@class, "r-sw-label") and text()="Manta y pañuelos"]')
    ice_cream_plus = (By.CSS_SELECTOR, 'div.counter-plus')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def select_comfort_tariff(self):
        self.driver.find_element(*self.taxi_button).click()
        self.driver.find_element(*self.comfort_tariff_button).click()

    def enter_phone_number(self, phone_number):
        self.driver.find_element(*self.phone_button).click()
        phone_field = self.driver.find_element(*self.phone_input)
        phone_field.send_keys(phone_number)
        self.driver.find_element(*self.next_button).click()

    def confirm_phone_code(self, code):
        self.driver.find_element(*self.confirm_button).click()

    def add_credit_card(self, card_number, card_code):
        self.driver.find_element(*self.payment_button).click()
        self.driver.find_element(*self.add_card_option).click()
        self.driver.find_element(*self.card_number_input).send_keys(card_number)
        cvv_field = self.driver.find_element(*self.card_cvv_input)
        cvv_field.send_keys(card_code)
        ActionChains(self.driver).send_keys(Keys.TAB).perform()
        self.driver.find_element(*self.add_card_button).click()

    def add_driver_message(self, message):
        self.driver.find_element(*self.driver_message_input).send_keys(message)

    def request_blanket_and_tissues(self):
        self.driver.find_element(*self.blanket_option).click()

    def request_ice_creams(self, count=2):
        for _ in range(count):
            self.driver.find_element(*self.ice_cream_plus).click()


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def test_order_taxi(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # 1. Configurar la dirección
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)

        # 2. Seleccionar la tarifa Comfort
        routes_page.select_comfort_tariff()

        # 3. Rellenar el número de teléfono y confirmar código
        routes_page.enter_phone_number(data.phone_number)
        phone_code = retrieve_phone_code(self.driver)
        routes_page.confirm_phone_code(phone_code)

        # 4. Agregar una tarjeta de crédito
        routes_page.add_credit_card(data.card_number, data.card_code)

        # 5. Escribir un mensaje para el controlador
        routes_page.add_driver_message(data.message_for_driver)

        # 6. Pedir manta y pañuelos
        routes_page.request_blanket_and_tissues()

        # 7. Pedir 2 helados
        routes_page.request_ice_creams()

        # 8. Esperar al modal
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.modal-driver-info'))
        )

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
