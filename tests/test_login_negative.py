
import pytest
from pathlib import Path
from selenium import webdriver
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By


# Screenshot directory
SCREENSHOT_DIR = Path(__file__).resolve().parents[1] / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")

    yield driver

    driver.quit()


@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        pytest.param(
            "", "secret_sauce",
            "Epic sadface: Username is required",
            id="empty_username"
        ),
        pytest.param(
            "standard_user", "",
            "Epic sadface: Password is required",
            id="empty_password"
        ),
        pytest.param(
            "wrong_user", "secret_sauce",
            "Epic sadface: Username and password do not match any user in this service",
            id="invalid_username"
        ),
        pytest.param(
            "standard_user", "wrong_password",
            "Epic sadface: Username and password do not match any user in this service",
            id="invalid_password"
        ),
        pytest.param(
            "wrong_user", "wrong_password",
            "Epic sadface: Username and password do not match any user in this service",
            id="invalid_credentials"
        ),
        pytest.param(
            "locked_out_user", "secret_sauce",
            "Epic sadface: Sorry, this user has been locked out.",
            id="locked_out_user"
        )
    ]
)
def test_login_negative(driver, username, password, expected_error, request):
    login_page = LoginPage(driver)

    login_page.login(username, password)

    # Capture screenshot evidence
    case_name = request.node.callspec.id
    screenshot_path = SCREENSHOT_DIR / f"negative_login_{case_name}.png"

    driver.save_screenshot(str(screenshot_path))

    # Validate error message visibility
    error_element = driver.find_element(
        By.CSS_SELECTOR, "[data-test='error']"
    )

    assert error_element.is_displayed()
    assert error_element.text == expected_error
