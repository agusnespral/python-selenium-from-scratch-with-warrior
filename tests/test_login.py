import asyncio

import pytest

from src.main.pages.login_page import LoginPage


@pytest.mark.smoke
def test_login(browser_sync, get_credentials, screenshot_helper, base_url):

    user = get_credentials.username
    pwd = get_credentials.password

    browser_sync.get(base_url)
    login_page = LoginPage(browser_sync)
    login_page.submit_login(user, pwd)


@pytest.mark.asyncio
async def test_login_async(browser_async, get_credentials):

    await asyncio.sleep(0)
    browser_async.get(base_url)

    login_page = LoginPage(browser_async)

    await asyncio.sleep(0)
    login_page.submit_login(get_credentials.username, get_credentials.password)

    await asyncio.sleep(1)
