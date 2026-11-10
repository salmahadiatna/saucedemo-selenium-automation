import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from utils import take_screenshot


@pytest.mark.ui
@allure.feature("Checkout")
@allure.title("Total harga di ringkasan pesanan sesuai perhitungan")
def test_checkout_total_is_correct(logged_in):
    driver = logged_in
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    with allure.step("Tambah tiga produk ke keranjang"):
        added = inventory_page.add_first_items_to_cart(3)
        expected_prices = [price for _, price in added]

    with allure.step("Lanjut sampai ringkasan pesanan"):
        inventory_page.open_cart()
        cart_page.proceed_to_checkout()
        checkout_page.fill_shipping_info("Budi", "Pekerti", "12345")
        take_screenshot(driver, "checkout_overview")

    with allure.step("Verifikasi harga item, subtotal, pajak, dan total"):
        summary_prices = checkout_page.get_summary_item_prices()
        subtotal = checkout_page.get_subtotal()
        tax = checkout_page.get_tax()
        total = checkout_page.get_total()

        # Harga di ringkasan sama dengan harga di halaman produk
        assert summary_prices == expected_prices
        # Subtotal = jumlah harga item
        assert subtotal == pytest.approx(sum(expected_prices), abs=0.005)
        # Total = subtotal + pajak
        assert total == pytest.approx(subtotal + tax, abs=0.005)
