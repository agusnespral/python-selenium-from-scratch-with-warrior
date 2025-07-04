from selenium.webdriver.common.by import By


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    # locators
    email_input_locator = (By.ID, "login-email")
    password_input_locator = (By.ID, "login-password")
    submit_button_locator = (By.ID, "login-submit")

    def submit_login(self, username, password):
        self.driver.find_element(*self.email_input_locator).clear()
        self.driver.find_element(*self.email_input_locator).send_keys(username)
        self.driver.find_element(*self.password_input_locator).clear()
        self.driver.find_element(*self.password_input_locator).send_keys(password)
        self.driver.find_element(*self.submit_button_locator).click()
