import asyncio

import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Load YAML config
with open("../src/config/config.yml") as f:
    config = yaml.safe_load(f)


class BrowserDriverHelperSync:

    def get_driver(self):
        browser = config["browser"].lower()
        headless = config.get("headless", False)

        if browser == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--start-maximized")
            return webdriver.Chrome(options=options)

        elif browser == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            return webdriver.Firefox(options=options)

        elif browser == "edge":
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless=new")
            return webdriver.Edge(options=options)

        else:
            raise ValueError(f"Unsupported browser: {browser}")


class BrowserDriverHelperAsync:

    def __init__(self):
        self.driver = None

    async def get_driver(self):
        # Ejecutar la creación del driver en un thread para no bloquear el event loop
        helper_sync = BrowserDriverHelperSync()
        self.driver = await asyncio.to_thread(helper_sync.get_driver)
        return self.driver

    async def get(self, url):
        if not self.driver:
            raise Exception("Driver no inicializado, llamar a get_driver primero")
        await asyncio.to_thread(self.driver.get, url)

    async def quit(self):
        if self.driver:
            await asyncio.to_thread(self.driver.quit)
