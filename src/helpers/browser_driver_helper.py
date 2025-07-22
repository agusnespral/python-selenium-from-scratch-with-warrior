import asyncio
import os
import random

import yaml
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from src.helpers.logger_helper import LoggerHelper

class BrowserDriverHelperSync:
    def __init__(self, browser_override=None):
        """

        Load .env.stg only if not running in Jenkins
        if not os.getenv("JENKINS_HOME"):
            load_dotenv()  # Load environment variables from .env.stg file

        # Set credentials from environment
        self.user_email = os.getenv("QA_USERNAME")
        self.user_pwd = os.getenv("QA_PWD")
        if not self.user_email or not self.user_pwd:
            raise ValueError(
                "QA_EMAIL and QA_PWD must be set in .env.stg or Jenkins environment."
            )
        """

        # Load config.yml
        self.config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../src/config/config.yml")
        )
        self.config = self.load_config()

        # Extract config values
        browser_cfg = self.config["browser"]
        self.browser_default = browser_override or browser_cfg["default"]

        self.headless = browser_cfg.get("headless", False)
        self.maximize = browser_cfg.get("maximize", True)
        self.tear_down = browser_cfg.get("tearDown", True)

        # Set random user-agent
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        ]
        self.user_agent = random.choice(self.user_agents)

        # Driver instance
        self.driver = None

        # Logger
        self.logger = LoggerHelper.get_instance()
        self.logger.info("BrowserDriverHelperSync initialized.")
    def load_config(self):
        """Load configuration from a YAML file."""
        with open(self.config_path, "r") as file:
            return yaml.safe_load(file)

    def get_driver(self):
        """Launch the browser and return the Selenium WebDriver instance."""
        if self.browser_default == "chrome":
            options = ChromeOptions()
            options.add_argument(f"user-agent={self.user_agent}")
            if self.headless:
                options.add_argument("--headless=new")
            if self.maximize:
                options.add_argument("--start-maximized")

            service = ChromeService(ChromeDriverManager().install())
            self.logger.info("ChromeDriverManager installed.")
            return webdriver.Chrome(service=service, options=options)


        elif self.browser_default == "firefox":
            options = FirefoxOptions()
            options.set_preference("general.useragent.override", self.user_agent)
            if self.headless:
                options.add_argument("--headless")
            self.driver = webdriver.Firefox(options=options)
            if self.maximize:
                self.driver.maximize_window()

            service = FirefoxService(GeckoDriverManager().install())
            return webdriver.Firefox(service=service, options=options)

        elif self.browser_default == "edge":
            options = EdgeOptions()
            options.add_argument(f"user-agent={self.user_agent}")
            if self.headless:
                options.add_argument("--headless=new")
            if self.maximize:
                options.add_argument("--start-maximized")

            service = EdgeService(EdgeChromiumDriverManager().install())
            return webdriver.Edge(service=service, options=options)

        else:
            raise ValueError(f"Unsupported browser: {self.browser_default}")

        return self.driver

    def quit_driver(self):
        """Closes the browser if tearDown is enabled."""
        if self.driver and self.tear_down:
            self.driver.quit()
        self.logger.info("BrowserDriverHelperSync closed.")



class BrowserDriverHelperAsync:
    """Asynchronous wrapper around BrowserDriverHelperSync for use in async test environments."""

    def __init__(self):
        self.sync_helper = BrowserDriverHelperSync()
        self.driver = None

    async def get_driver(self):
        await asyncio.sleep(0)  # Yield control to event loop
        self.driver = self.sync_helper.get_driver()
        return self.driver

    async def quit_driver(self):
        await asyncio.sleep(0)
        self.sync_helper.quit_driver()
