import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def get_item_names(self):
        return [element.text for element in self.find_all(self.ITEM_NAMES)]

    @allure.step("Lanjut ke checkout")
    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
