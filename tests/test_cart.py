import allure
import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from utils import take_screenshot


@pytest.mark.ui
@allure.feature("Cart")
@allure.title("Hapus satu item dari keranjang")
def test_remove_item_from_cart(logged_in):
    driver = logged_in
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    with allure.step("Tambah dua produk ke keranjang"):
        added = inventory_page.add_first_items_to_cart(2)
        assert inventory_page.get_cart_badge_count() == "2"

    with allure.step("Buka keranjang dan pastikan dua item ada"):
        inventory_page.open_cart()
        assert cart_page.wait_for_item_count(2)
        assert cart_page.get_item_names() == [name for name, _ in added]
        take_screenshot(driver, "cart_two_items")

    with allure.step("Hapus item pertama"):
        cart_page.remove_first_item()

    with allure.step("Verifikasi tinggal satu item (yang kedua)"):
        assert cart_page.wait_for_item_count(1)
        assert cart_page.get_item_names() == [added[1][0]]
        assert inventory_page.get_cart_badge_count() == "1"
        take_screenshot(driver, "cart_one_item")
