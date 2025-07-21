from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class GridDriverHelper:

    def get_driver(self):
        options = webdriver.ChromeOptions()

        # options.add_argument('--headless=new')

        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=options
        )
        return driver
