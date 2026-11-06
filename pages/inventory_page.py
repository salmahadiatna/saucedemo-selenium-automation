import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".btn_inventory")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def get_title(self):
        return self.text_of(self.TITLE)

    @allure.step("Tambah produk pertama ke keranjang")
    def add_first_item_to_cart(self):
        """Return nama produk yang ditambahkan, untuk diverifikasi di keranjang."""
        item_name = self.find_all(self.ITEM_NAMES)[0].text
        self.find_all(self.ADD_TO_CART_BUTTONS)[0].click()
        return item_name

    def get_cart_badge_count(self):
        return self.text_of(self.CART_BADGE)

    @allure.step("Buka keranjang")
    def open_cart(self):
        self.click(self.CART_LINK)
