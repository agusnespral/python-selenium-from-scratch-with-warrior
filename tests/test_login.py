import os
import time

from dotenv import load_dotenv
from selenium import webdriver

from src.pages.login_page import LoginPage

driver = webdriver.Chrome()
login_page = LoginPage(driver)

load_dotenv()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
base_url = os.getenv("BASE_URL")


def test_login():
    url = base_url

    driver.get(url)
    time.sleep(3)
    login_page.submit_login(username, password)
