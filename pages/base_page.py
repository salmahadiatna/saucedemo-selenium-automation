from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Helper umum (explicit wait) yang diwarisi semua page."""

    TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def enter_text(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator):
        return self.find(locator).text

    def is_visible(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
