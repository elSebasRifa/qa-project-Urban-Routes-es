import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    taxi_button = (By.XPATH, '//button[text()="Pedir un taxi"]')
    comfort_tariff_button = (By.CSS_SELECTOR, 'button[data-for="tariff-card-4"]')
    phone_button = (By.CLASS_NAME, 'np-text')  # Usando Class Name como tipo de selector adicional
    phone_input = (By.ID, 'phone')
    next_button = (By.XPATH, '//button[text()="Siguiente"]')
    confirm_button = (By.XPATH, '//button[text()="Confirmar"]')
    payment_button = (By.CLASS_NAME, 'pp-text')
    add_card_option = (By.CLASS_NAME, 'pp-title')
    card_number_input = (By.ID, 'number')
    card_cvv_input = (By.ID, 'code')
    add_card_button = (By.XPATH, '//button[text()="Agregar"]')
    driver_message_input = (By.ID, 'comment')
    blanket_option = (By.XPATH, '//div[contains(@class, "r-sw-label") and text()="Manta y pañuelos"]')
    ice_cream_plus = (By.CLASS_NAME, 'counter-plus')
    driver_info_modal = (By.CLASS_NAME, 'modal-driver-info')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def click_taxi_button(self):
        self.driver.find_element(*self.taxi_button).click()

    def select_comfort_tariff(self):
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
        self.driver.switch_to.active_element.send_keys(Keys.TAB)  # Simula TAB
        self.driver.find_element(*self.add_card_button).click()

    def add_driver_message(self, message):
        self.driver.find_element(*self.driver_message_input).send_keys(message)

    def request_blanket_and_tissues(self):
        self.driver.find_element(*self.blanket_option).click()

    def request_ice_creams(self, count=2):
        for _ in range(count):
            self.driver.find_element(*self.ice_cream_plus).click()

    def wait_for_driver_info_modal(self, timeout=30):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.driver_info_modal)
        )


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def setup_method(self):
        self.driver.get(data.urban_routes_url)
        self.routes_page = UrbanRoutesPage(self.driver)

    def test_set_route(self):
        self.routes_page.set_from(data.address_from)
        self.routes_page.set_to(data.address_to)
        assert self.routes_page.get_from() == data.address_from
        assert self.routes_page.get_to() == data.address_to

    def test_select_plan(self):
        self.routes_page.click_taxi_button()
        self.routes_page.select_comfort_tariff()

    def test_fill_phone_number(self):
        self.routes_page.enter_phone_number(data.phone_number)
        phone_code = retrieve_phone_code(self.driver)
        self.routes_page.confirm_phone_code(phone_code)

    def test_fill_card(self):
        self.routes_page.add_credit_card(data.card_number, data.card_code)

    def test_comment_for_driver(self):
        self.routes_page.add_driver_message(data.message_for_driver)

    def test_order_blanket_and_handkerchiefs(self):
        self.routes_page.request_blanket_and_tissues()

    def test_order_2_ice_creams(self):
        self.routes_page.request_ice_creams()

    def test_car_search_model_appears(self):
        self.routes_page.wait_for_driver_info_modal()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
