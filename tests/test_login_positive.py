
import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pathlib import Path

SCREENSHOT_DIR = Path(__file__).resolve().parents[1] / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")

    yield driver

    driver.quit()


def test_login_success(driver):
    login_page = LoginPage(driver)

    login_page.login("standard_user", "secret_sauce")
    driver.save_screenshot(
    str(SCREENSHOT_DIR / "positive_login_success.png")
)
    assert "inventory.html" in driver.current_url
