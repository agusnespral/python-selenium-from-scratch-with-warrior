import os

from dotenv import load_dotenv

from src.main.pages.login_page import LoginPage

# Load environment variables from a .env file into the system environment variables
load_dotenv()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
base_url = os.getenv("BASE_URL")


def test_login(browser_sync):
    browser_sync.get(base_url)
    login_page = LoginPage(browser_sync)
    login_page.submit_login(username, password)
