from selenium.webdriver.common.by import By
from src.helpers.logger_helper import LoggerHelper
from src.helpers.log_step import log_step

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = LoggerHelper.get_instance()

    # locators
    email_input_locator = (By.ID, "login-email")
    password_input_locator = (By.ID, "login-password")
    submit_button_locator = (By.ID, "login-submit")

    @log_step
    def submit_login(self, username, password):
        self.driver.find_element(*self.email_input_locator).clear()
        self.driver.find_element(*self.email_input_locator).send_keys(username)
        self.driver.find_element(*self.password_input_locator).clear()
        self.driver.find_element(*self.password_input_locator).send_keys(password)
        self.driver.find_element(*self.submit_button_locator).click()
