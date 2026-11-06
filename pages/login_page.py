import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    # 1. Kumpulkan semua locator
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # 2. Method untuk setiap aksi (nama sama seperti versi lama)
    def input_username(self, username):
        self.enter_text(self.USERNAME_INPUT, username)

    def input_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    # 3. Proses login lengkap
    @allure.step("Login dengan username '{username}'")
    def login(self, username, password):
        self.input_username(username)
        self.input_password(password)
        self.click_login()

    # 4. Pesan error (untuk test login negatif)
    def get_error_message(self):
        return self.text_of(self.ERROR_MESSAGE)
