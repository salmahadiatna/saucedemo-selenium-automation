import re

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


def amount_from(text):
    """'Item total: $39.98' -> 39.98"""
    return float(re.search(r"\$([0-9]+(?:\.[0-9]+)?)", text).group(1))


class CheckoutPage(BasePage):
    # Langkah 1: informasi pengiriman
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")

    # Langkah 2: ringkasan pesanan
    SUMMARY_ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")

    # Langkah 3: selesai
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    # ---------- langkah 1 ----------

    @allure.step("Ketik informasi pengiriman (tanpa klik Continue)")
    def type_shipping_info(self, first_name, last_name, postal_code):
        self.enter_text(self.FIRST_NAME, first_name)
        self.enter_text(self.LAST_NAME, last_name)
        self.enter_text(self.POSTAL_CODE, postal_code)

    def get_shipping_field_values(self):
        """Isi field saat ini, untuk memverifikasi input tersimpan dengan benar."""
        return {
            "first_name": self.attribute_of(self.FIRST_NAME, "value"),
            "last_name": self.attribute_of(self.LAST_NAME, "value"),
            "postal_code": self.attribute_of(self.POSTAL_CODE, "value"),
        }

    @allure.step("Isi informasi pengiriman")
    def fill_shipping_info(self, first_name, last_name, postal_code):
        self.type_shipping_info(first_name, last_name, postal_code)
        self.click(self.CONTINUE_BUTTON)

    # ---------- ringkasan pesanan ----------

    def get_summary_item_prices(self):
        return [amount_from(t) for t in self.texts_of(self.SUMMARY_ITEM_PRICES)]

    def get_subtotal(self):
        return amount_from(self.text_of(self.SUBTOTAL_LABEL))

    def get_tax(self):
        return amount_from(self.text_of(self.TAX_LABEL))

    def get_total(self):
        return amount_from(self.text_of(self.TOTAL_LABEL))

    @allure.step("Selesaikan checkout")
    def finish_checkout(self):
        self.click(self.FINISH_BUTTON)

    def get_success_message(self):
        return self.text_of(self.COMPLETE_HEADER)