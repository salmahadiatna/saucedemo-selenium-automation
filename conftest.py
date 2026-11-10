import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils import take_screenshot

BASE_URL = "https://www.saucedemo.com/"


# ==========================================
# HOOK: simpan hasil test agar fixture tahu test gagal atau tidak
# ==========================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)


# ==========================================
# FIXTURE BROWSER
# Mode headless: set env HEADLESS=1 (dipakai di CI).
# ==========================================

@pytest.fixture
def driver(request):
    options = Options()

    options.add_experimental_option(
        "prefs",
        {
            "profile.password_manager_leak_detection": False,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        },
    )

    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
    else:
        options.add_argument("--start-maximized")

    browser = webdriver.Chrome(options=options)
    browser.get(BASE_URL)

    yield browser

    try:
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            take_screenshot(browser, f"FAILED_{request.node.name}")
    except Exception as error:
        print(f"\nGagal mengambil screenshot: {error}")
    finally:
        browser.quit()


# Alias supaya test lama yang memakai nama `setup_browser` tetap jalan
@pytest.fixture
def setup_browser(driver):
    return driver


# ==========================================
# FIXTURE: sudah login
# ==========================================

def _login(driver, username):
    LoginPage(driver).login(username, "secret_sauce")
    # get_title menunggu halaman produk benar-benar termuat
    assert InventoryPage(driver).get_title() == "Products"
    return driver


@pytest.fixture
def logged_in(driver):
    return _login(driver, "standard_user")


@pytest.fixture
def logged_in_problem_user(driver):
    return _login(driver, "problem_user")
