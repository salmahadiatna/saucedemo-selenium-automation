import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    @allure.step("Isi informasi pengiriman")
    def fill_shipping_info(self, first_name, last_name, postal_code):
        self.enter_text(self.FIRST_NAME, first_name)
        self.enter_text(self.LAST_NAME, last_name)
        self.enter_text(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE_BUTTON)

    @allure.step("Selesaikan checkout")
    def finish_checkout(self):
        self.click(self.FINISH_BUTTON)

    def get_success_message(self):
        return self.text_of(self.COMPLETE_HEADER)
