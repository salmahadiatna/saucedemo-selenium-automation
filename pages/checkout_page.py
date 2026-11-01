from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    # --- 1. Locators ---
    ADD_TO_CART_BTN = (By.ID, "add-to-cart-sauce-labs-backpack")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CHECKOUT_BTN = (By.ID, "checkout")
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    FINISH_BTN = (By.ID, "finish")
    SUCCESS_HEADER = (By.CLASS_NAME, "complete-header")
    BACK_HOME_BTN = (By.ID, "back-to-products")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- 2. Actions ---
    def add_item_and_go_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BTN)).click()
        self.driver.find_element(*self.CART_LINK).click()

    def proceed_to_checkout(self):
        # Memakai trik JS Click untuk mencegah error popup
        checkout_btn = self.wait.until(EC.presence_of_element_located(self.CHECKOUT_BTN))
        self.driver.execute_script("arguments[0].click();", checkout_btn)

    def fill_shipping_info(self, fname, lname, postal):
        self.wait.until(EC.presence_of_element_located(self.FIRST_NAME)).send_keys(fname)
        self.driver.find_element(*self.LAST_NAME).send_keys(lname)
        self.driver.find_element(*self.POSTAL_CODE).send_keys(postal)
        self.driver.find_element(*self.CONTINUE_BTN).click()

    def finish_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.FINISH_BTN)).click()

    def get_success_message(self):
        # Mengambil teks untuk divalidasi nanti
        return self.wait.until(EC.visibility_of_element_located(self.SUCCESS_HEADER)).text

    def back_to_home(self):
        self.wait.until(EC.element_to_be_clickable(self.BACK_HOME_BTN)).click()