"""
Test untuk akun `problem_user` di SauceDemo.

Akun ini sengaja dibuat bermasalah. Test di bawah memeriksa perilaku yang
SEHARUSNYA benar. Bug yang sudah dikenal ditandai xfail (non-strict):

  - XFAIL : bug masih ada (hasil yang diharapkan, CI tetap hijau)
  - XPASS : perilaku ternyata sudah benar, tinjau ulang test ini
"""
import allure
import pytest

from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from utils import take_screenshot

CHECKOUT_STEP_ONE_URL = "https://www.saucedemo.com/checkout-step-one.html"


@pytest.mark.ui
@allure.feature("problem_user")
@allure.title("problem_user bisa login dan masuk ke halaman produk")
def test_problem_user_can_login(logged_in_problem_user):
    driver = logged_in_problem_user

    assert "inventory.html" in driver.current_url
    take_screenshot(driver, "problem_user_after_login")


@pytest.mark.ui
@allure.feature("problem_user")
@allure.title("Setiap produk menampilkan gambar yang berbeda")
@pytest.mark.xfail(
    reason="Bug problem_user: semua produk menampilkan gambar yang sama",
    strict=False,
)
def test_product_images_are_unique(logged_in_problem_user):
    driver = logged_in_problem_user
    inventory_page = InventoryPage(driver)

    sources = inventory_page.get_item_image_sources()
    take_screenshot(driver, "problem_user_images")

    with allure.step(f"Gambar ditemukan: {len(sources)}, unik: {len(set(sources))}"):
        assert len(set(sources)) == len(sources)


@pytest.mark.ui
@allure.feature("problem_user")
@allure.title("Urutan harga rendah ke tinggi bekerja")
@pytest.mark.xfail(
    reason="Bug problem_user: pengurutan produk tidak berfungsi",
    strict=False,
)
def test_sort_works(logged_in_problem_user):
    driver = logged_in_problem_user
    inventory_page = InventoryPage(driver)

    inventory_page.sort_by("lohi")
    prices = inventory_page.get_item_prices()
    take_screenshot(driver, "problem_user_sort")

    assert prices == sorted(prices)


@pytest.mark.ui
@allure.feature("problem_user")
@allure.title("Semua produk bisa ditambahkan ke keranjang")
@pytest.mark.xfail(
    reason="Bug problem_user: sebagian produk tidak bisa ditambahkan ke keranjang",
    strict=False,
)
def test_all_items_can_be_added_to_cart(logged_in_problem_user):
    driver = logged_in_problem_user
    inventory_page = InventoryPage(driver)

    total_items = len(inventory_page.get_item_names())
    inventory_page.add_first_items_to_cart(total_items)
    take_screenshot(driver, "problem_user_add_all")

    assert inventory_page.get_cart_badge_count() == str(total_items)


@pytest.mark.ui
@allure.feature("problem_user")
@allure.title("Field informasi pengiriman menyimpan input dengan benar")
@pytest.mark.xfail(
    reason="Bug problem_user: input nama belakang tidak tersimpan dengan benar di checkout",
    strict=False,
)
def test_checkout_fields_keep_input(logged_in_problem_user):
    driver = logged_in_problem_user
    checkout_page = CheckoutPage(driver)

    # Langsung ke langkah 1 checkout agar tidak bergantung pada isi keranjang
    driver.get(CHECKOUT_STEP_ONE_URL)

    checkout_page.type_shipping_info("Budi", "Pekerti", "12345")
    values = checkout_page.get_shipping_field_values()
    take_screenshot(driver, "problem_user_checkout_fields")

    assert values == {
        "first_name": "Budi",
        "last_name": "Pekerti",
        "postal_code": "12345",
    }
