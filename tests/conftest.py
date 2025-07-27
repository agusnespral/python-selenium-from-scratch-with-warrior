import os
from dataclasses import dataclass

import pytest
import pytest_asyncio
import yaml
from pathlib import Path

from src.helpers.browser_driver_helper import (BrowserDriverHelperAsync,
                                               BrowserDriverHelperSync)
from src.helpers.remote_driver_helper import GridDriverHelper
from src.helpers.screenshot_helper import ScreenshotHelper
from src.helpers.logger_helper import LoggerHelper
from src.helpers.load_env_helper import set_env


set_env()

@pytest.fixture(scope="session")
def base_url():
    url = os.getenv("BASE_URL")
    if not url:
        raise ValueError("BASE_URL is not set in environment.")
    return url

def auth_url():
    url = os.getenv("AUTH_URL")
    if not url:
        raise ValueError("AUTH_URL is not set in environment.")
    return url

@dataclass
class Credentials:
    username: str
    password: str



def get_credentials():
    user_email = os.getenv("QA_USERNAME")
    user_pwd = os.getenv("QA_PWD")
    print(f'this is the user mail= {user_email}')


    if not user_email or not user_pwd:
        raise ValueError(
            "QA_EMAIL and QA_PWD must be set in .env.stg")

    return Credentials(username=user_email, password=user_pwd)


def pytest_addoption(parser):
    parser.addoption("--grid", action="store_true", help="Run tests using Selenium Grid")
    parser.addoption("--browser", action="store",
                     help="Define browser: chrome, firefox or edge")

@pytest.fixture(scope="function")
def browser_sync(request, logger):
    logger = LoggerHelper.get_instance()

    config_path = Path(__file__).parent.parent / "src" / "config" / "config.yml"

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    default_browser = config.get("browser", {}).get("default", "chrome")

    use_grid = request.config.getoption("--grid")
    cli_browser = request.config.getoption("--browser")

    browser = cli_browser if cli_browser else default_browser

    if use_grid:
        driver = GridDriverHelper().get_driver()
        logger.info("Using Selenium Grid")
        yield driver
        driver.quit()
    else:
        helper = BrowserDriverHelperSync(browser)
        driver = helper.get_driver()
        logger.info("Using local browser")
        yield driver
        helper.quit_driver()


@pytest_asyncio.fixture(scope="function")
async def browser_async():
    helper = BrowserDriverHelperAsync()
    await helper.get_driver()
    yield helper.driver
    await helper.quit_driver()





@pytest.fixture(scope="function")
def screenshot_helper():
    return ScreenshotHelper()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    print("\n--- Executing hookwrapper pytest_runtest_makereport ---")
    outcome = yield
    report = outcome.get_result()
    logger = LoggerHelper.get_instance()

    if report.when == "call":
        if report.failed:
            logger.error(f"--- RESULT: {item.nodeid} [FAILED] ---")
            print(
                f"Test '{item.name}' failed in call phase. Taking screenshot..."
            )
            driver = item.funcargs.get("browser_sync")
            screenshot_helper = item.funcargs.get("screenshot_helper")
            print(f"Driver objeto: {driver}")

            print(f"ScreenshotHelper object: {screenshot_helper}")

            if driver and screenshot_helper:
                print("Driver and screenshot_helper available.")
                screenshot_helper.take_screenshot(driver, item.name, "failed")
        elif report.passed:
            logger.info(f"--- RESULT: {item.nodeid} [PASSED] ---")


@pytest.fixture(scope="session")
def logger():
    return LoggerHelper.get_instance()


def pytest_runtest_protocol(item, nextitem):
    """
    Hook executed before each test starts.
    Logs the test start time and name.
    """
    logger = LoggerHelper.get_instance()

    if logger:
        # Log the start of the test using the full node ID (file::test_name)
        logger.info(f"--- STARTING TEST: {item.nodeid} ---")


