from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Helper umum (explicit wait + retry saat elemen basi) untuk semua page."""

    TIMEOUT = 10
    RETRIES = 3

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT)

    def _retry(self, action):
        """Jalankan `action`; jika elemen basi (React render ulang), ulangi.

        `action` harus mengambil elemennya sendiri di dalam fungsi, supaya
        tiap percobaan memakai elemen yang baru.
        """
        for attempt in range(self.RETRIES):
            try:
                return action()
            except StaleElementReferenceException:
                if attempt == self.RETRIES - 1:
                    raise

    # ---------- mencari ----------

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    # ---------- aksi ----------

    def click(self, locator):
        self._retry(
            lambda: self.wait.until(EC.element_to_be_clickable(locator)).click()
        )

    def click_nth(self, locator, index):
        """Klik elemen ke-`index` dari daftar elemen yang cocok."""
        self._retry(lambda: self.find_all(locator)[index].click())

    def enter_text(self, locator, text):
        def action():
            element = self.find(locator)
            element.clear()
            element.send_keys(text)

        self._retry(action)

    # ---------- membaca ----------

    def text_of(self, locator):
        return self._retry(lambda: self.find(locator).text)

    def texts_of(self, locator):
        return self._retry(lambda: [e.text for e in self.find_all(locator)])

    def attribute_of(self, locator, name):
        return self._retry(lambda: self.find(locator).get_attribute(name))

    def attributes_of(self, locator, name):
        return self._retry(
            lambda: [e.get_attribute(name) for e in self.find_all(locator)]
        )

    def is_visible(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
