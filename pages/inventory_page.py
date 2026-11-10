import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


def parse_price(text):
    """'$29.99' -> 29.99"""
    return float(text.replace("$", "").strip())


class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ITEM_IMAGES = (By.CSS_SELECTOR, ".inventory_item_img img")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".btn_inventory")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def get_title(self):
        return self.text_of(self.TITLE)

    # ---------- daftar produk ----------

    def get_item_names(self):
        return [e.text for e in self.find_all(self.ITEM_NAMES)]

    def get_item_prices(self):
        return [parse_price(e.text) for e in self.find_all(self.ITEM_PRICES)]

    def get_item_image_sources(self):
        return [e.get_attribute("src") for e in self.find_all(self.ITEM_IMAGES)]

    @allure.step("Urutkan produk: {option_value}")
    def sort_by(self, option_value):
        """option_value: az, za, lohi, atau hilo."""
        Select(self.find(self.SORT_DROPDOWN)).select_by_value(option_value)

    # ---------- keranjang ----------

    @allure.step("Tambah produk pertama ke keranjang")
    def add_first_item_to_cart(self):
        """Return nama produk yang ditambahkan, untuk diverifikasi di keranjang."""
        item_name = self.find_all(self.ITEM_NAMES)[0].text
        self.find_all(self.ADD_TO_CART_BUTTONS)[0].click()
        return item_name

    @allure.step("Tambah {count} produk pertama ke keranjang")
    def add_first_items_to_cart(self, count):
        """Return list (nama, harga) produk yang ditambahkan."""
        names = self.get_item_names()[:count]
        prices = self.get_item_prices()[:count]
        buttons = self.find_all(self.ADD_TO_CART_BUTTONS)
        for button in buttons[:count]:
            button.click()
        return list(zip(names, prices))

    def get_cart_badge_count(self):
        return self.text_of(self.CART_BADGE)

    @allure.step("Buka keranjang")
    def open_cart(self):
        self.click(self.CART_LINK)

    # ---------- menu ----------

    @allure.step("Logout")
    def logout(self):
        # Buka menu; kalau link logout belum terlihat, coba klik burger sekali lagi
        for _ in range(2):
            self.click(self.MENU_BUTTON)
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(self.LOGOUT_LINK)
                )
                break
            except TimeoutException:
                continue

        self.click(self.LOGOUT_LINK)
