import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils import take_screenshot


@pytest.mark.ui
@allure.feature("Login")
@allure.title("Logout mengembalikan user ke halaman login")
def test_logout(logged_in):
    driver = logged_in
    inventory_page = InventoryPage(driver)
    login_page = LoginPage(driver)

    with allure.step("Logout lewat menu"):
        inventory_page.logout()

    with allure.step("Verifikasi kembali ke halaman login"):
        assert login_page.is_visible(login_page.LOGIN_BUTTON)
        assert "inventory.html" not in driver.current_url
        take_screenshot(driver, "after_logout")
