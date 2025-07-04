import pytest
import pytest_asyncio

from src.helpers.browser_driver_helper import (
    BrowserDriverHelperAsync,
    BrowserDriverHelperSync,
)


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
    await helper.quit()
