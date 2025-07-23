from selenium.webdriver.common.by import By
from src.helpers.logger_helper import LoggerHelper
from src.helpers.log_step import log_step
from src.helpers.wait_helper import WaitHelper

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = LoggerHelper.get_instance()
        self.wait_helper = WaitHelper(self.driver)

    # locators
    email_input_locator = (By.ID, "login-email")
    password_input_locator = (By.ID, "login-password")
    submit_button_locator = (By.ID, "login-submit")
    invalid_user_or_pwd_message = (By.CSS_SELECTOR, ".form-text.error.ng-star-inserted")

    @log_step
    def submit_login(self, username, password):
        self.driver.find_element(*self.email_input_locator).clear()
        self.driver.find_element(*self.email_input_locator).send_keys(username)
        self.driver.find_element(*self.password_input_locator).clear()
        self.driver.find_element(*self.password_input_locator).send_keys(password)
        self.driver.find_element(*self.submit_button_locator).click()

    def login_error_message(self):
        return self.wait_helper.visible(self.invalid_user_or_pwd_message)



