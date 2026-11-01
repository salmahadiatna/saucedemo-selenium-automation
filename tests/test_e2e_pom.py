import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage

# Fixture mengatur persiapan (setup) dan penutupan (teardown)

@pytest.fixture
def setup_browser():
    chrome_options = Options()

    chrome_options.add_experimental_option(
        "prefs",
        {
            "profile.password_manager_leak_detection": False,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
    )

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.saucedemo.com/")

    yield driver

    driver.quit()

def take_screenshot(driver, filename):
    os.makedirs("screenshots", exist_ok=True)
    driver.save_screenshot(f"screenshots/{filename}.png")

# Eksekusi utama
def test_e2e_checkout(setup_browser):
    driver = setup_browser
    login_page = LoginPage(driver)
    checkout_page = CheckoutPage(driver)

    login_page.login("standard_user", "secret_sauce")
    take_screenshot(driver, "01_after_login")
    checkout_page.add_item_and_go_to_cart()
    take_screenshot(driver, "02_shopping_cart")
    checkout_page.proceed_to_checkout()
    take_screenshot(driver, "03_checkout_information")
    checkout_page.fill_shipping_info("Budi", "Pekerti", "12345")
    take_screenshot(driver, "04_shipping_information")
    checkout_page.finish_checkout()
    take_screenshot(driver, "05_checkout_complete")

    assert checkout_page.get_success_message() == "Thank you for your order!"