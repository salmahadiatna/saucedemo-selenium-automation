
from selenium.webdriver.common.by import By

class LoginPage:
    # 1. Kumpulkan semua Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    # 2. Inisialisasi driver
    def __init__(self, driver):
        self.driver = driver

    # 3. Method untuk setiap aksi
    def input_username(self, username):
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)

    def input_password(self, password):
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    # 4. Method untuk menjalankan proses login
    def login(self, username, password):
        self.input_username(username)
        self.input_password(password)
        self.click_login()
