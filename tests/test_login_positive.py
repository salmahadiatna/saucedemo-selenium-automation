import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils import take_screenshot


@pytest.mark.ui
@allure.feature("Login")
@allure.title("Login berhasil dengan standard_user")
def test_login_success(driver):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    with allure.step("Login dengan kredensial valid"):
        login_page.login("standard_user", "secret_sauce")

    with allure.step("Verifikasi masuk ke halaman produk"):
        # get_title menunggu halaman produk benar-benar termuat
        assert inventory_page.get_title() == "Products"
        assert "inventory.html" in driver.current_url
        take_screenshot(driver, "positive_login_success")
