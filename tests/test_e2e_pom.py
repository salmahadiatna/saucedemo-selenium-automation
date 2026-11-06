import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils import take_screenshot


@pytest.mark.ui
@allure.title("E2E: standard_user berhasil checkout satu produk")
def test_e2e_checkout(setup_browser):
    driver = setup_browser
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    with allure.step("Login"):
        login_page.login("standard_user", "secret_sauce")
        assert inventory_page.get_title() == "Products"
        take_screenshot(driver, "01_after_login")

    with allure.step("Tambah produk ke keranjang"):
        item_name = inventory_page.add_first_item_to_cart()
        assert inventory_page.get_cart_badge_count() == "1"
        inventory_page.open_cart()
        assert item_name in cart_page.get_item_names()
        take_screenshot(driver, "02_shopping_cart")

    with allure.step("Isi informasi checkout"):
        cart_page.proceed_to_checkout()
        take_screenshot(driver, "03_checkout_information")
        checkout_page.fill_shipping_info("Budi", "Pekerti", "12345")
        take_screenshot(driver, "04_shipping_information")

    with allure.step("Selesaikan pesanan"):
        checkout_page.finish_checkout()
        take_screenshot(driver, "05_checkout_complete")
        assert checkout_page.get_success_message() == "Thank you for your order!"

