import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class CartPage(BasePage):
    ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, ".cart_button")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def get_item_names(self):
        return [element.text for element in self.find_all(self.ITEM_NAMES)]

    def wait_for_item_count(self, expected):
        """True jika jumlah item di keranjang menjadi `expected` (boleh 0)."""
        try:
            WebDriverWait(self.driver, self.TIMEOUT).until(
                lambda d: len(d.find_elements(*self.ITEMS)) == expected
            )
            return True
        except Exception:
            return False

    @allure.step("Hapus item pertama dari keranjang")
    def remove_first_item(self):
        self.find_all(self.REMOVE_BUTTONS)[0].click()

    @allure.step("Lanjut ke checkout")
    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
