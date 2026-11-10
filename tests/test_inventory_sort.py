import allure
import pytest

from pages.inventory_page import InventoryPage
from utils import take_screenshot


@pytest.mark.ui
@allure.feature("Inventory")
@pytest.mark.parametrize(
    "option, field, reverse",
    [
        pytest.param("az", "names", False, id="name_a_to_z"),
        pytest.param("za", "names", True, id="name_z_to_a"),
        pytest.param("lohi", "prices", False, id="price_low_to_high"),
        pytest.param("hilo", "prices", True, id="price_high_to_low"),
    ],
)
def test_sort_products(logged_in, option, field, reverse, request):
    allure.dynamic.title(f"Urutkan produk: {request.node.callspec.id}")
    driver = logged_in
    inventory_page = InventoryPage(driver)

    with allure.step(f"Pilih urutan '{option}'"):
        inventory_page.sort_by(option)

    with allure.step("Verifikasi urutan produk"):
        actual = (
            inventory_page.get_item_names()
            if field == "names"
            else inventory_page.get_item_prices()
        )
        take_screenshot(driver, f"sort_{request.node.callspec.id}")

        assert actual == sorted(actual, reverse=reverse)
