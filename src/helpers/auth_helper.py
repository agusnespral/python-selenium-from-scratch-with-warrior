import requests
from src.helpers.credentials_helper import get_credentials
from tests.conftest import auth_url
from tests.conftest import base_url
from src.helpers.browser_driver_helper import BrowserDriverHelperSync
import time

def get_sso_token():
    """
    Get the SSO token by logging in the user via the authentication endpoint.
    :param email: The email of the user
    :return:  str or None
    """
    credentials = get_credentials()
    email = credentials.username
    pwd = credentials.password
    url = auth_url()

    session = requests.Session()

    login_url = url
    payload = {
        "j_username": email,
        "j_password": pwd,
        "source": ""
    }

    response = session.post(login_url, data=payload)

    if response.status_code == 200:
        token = session.cookies.get("OESSOTOK")
        if token:
            print("SSO token:", token)
            return token
        else:
            print("Token not found")
            return None
    else:
        print("Login error:", response.status_code)
        return None


def plant_sstok_cookie(base_url):
    token = get_sso_token()
    driver = BrowserDriverHelperSync().get_driver()
    driver.get(base_url)
    driver.add_cookie({
        'name': 'OESSOTOK',
        'value': token
    })

    driver.refresh()
    driver.get(base_url)
    time.sleep(25)


