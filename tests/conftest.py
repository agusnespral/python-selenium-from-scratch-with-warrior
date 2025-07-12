import os
from dataclasses import dataclass

import pytest
import pytest_asyncio

from src.helpers.browser_driver_helper import (BrowserDriverHelperAsync,
                                               BrowserDriverHelperSync)
from src.helpers.screenshot_helper import ScreenshotHelper


@dataclass
class Credentials:
    username: str
    password: str


@pytest.fixture
def get_credentials():
    user_email = os.getenv("QA_USERNAME")
    user_pwd = os.getenv("QA_PWD")

    if not user_email or not user_pwd:
        raise ValueError(
            "QA_USERNAME and QA_PWD must be set in .env or Jenkins environment."
        )

    return Credentials(username=user_email, password=user_pwd)


@pytest.fixture(scope="function")
def browser_sync():
    helper = BrowserDriverHelperSync()
    driver = helper.get_driver()
    yield driver
    driver.quit()


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
    print("\n--- Ejecutando hookwrapper pytest_runtest_makereport ---")
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        print(
            f"Test '{item.name}' falló en la fase 'call'. Intentando tomar captura..."
        )
        driver = item.funcargs.get("browser_sync")
        screenshot_helper = item.funcargs.get("screenshot_helper")
        print(f"Driver objeto: {driver}")

        print(f"ScreenshotHelper objeto: {screenshot_helper}")

        if driver and screenshot_helper:
            print("Driver y screenshot_helper disponibles.")
            screenshot_helper.take_screenshot(driver, item.name, "failed")
