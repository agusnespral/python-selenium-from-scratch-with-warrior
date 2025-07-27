import pytest

from src.main.pages.login_page import LoginPage
from src.helpers.credentials_helper import get_credentials
from src.helpers.logger_helper import LoggerHelper
from src.helpers.browser_driver_helper import BrowserDriverHelperSync
from src.helpers.auth_helper import get_sso_token, plant_sstok_cookie




@pytest.mark.smoke
def test_login(browser_sync, screenshot_helper, base_url):

    credentials = get_credentials('valid')
    user = credentials.username
    pwd = credentials.password

    browser_sync.get(base_url)
    login_page = LoginPage(browser_sync)
    login_page.submit_login(user, pwd)


def test_invalid_username_login(browser_sync, screenshot_helper, base_url):

    credentials = get_credentials('invalid_username')
    user = credentials.username
    pwd = credentials.password

    browser_sync.get(base_url)
    login_page = LoginPage(browser_sync)
    login_page.submit_login(user, pwd)

    element = login_page.login_error_message()
    logger = LoggerHelper.get_instance()
    logger.info(element.text)
    assert element.is_displayed()

def test_auth_login(base_url):
    plant_sstok_cookie(base_url)
