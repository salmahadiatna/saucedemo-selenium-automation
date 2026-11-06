import allure
import pytest

from pages.login_page import LoginPage
from utils import take_screenshot


@pytest.mark.ui
@allure.feature("Login")
@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        pytest.param(
            "", "secret_sauce",
            "Epic sadface: Username is required",
            id="empty_username",
        ),
        pytest.param(
            "standard_user", "",
            "Epic sadface: Password is required",
            id="empty_password",
        ),
        pytest.param(
            "wrong_user", "secret_sauce",
            "Epic sadface: Username and password do not match any user in this service",
            id="invalid_username",
        ),
        pytest.param(
            "standard_user", "wrong_password",
            "Epic sadface: Username and password do not match any user in this service",
            id="invalid_password",
        ),
        pytest.param(
            "wrong_user", "wrong_password",
            "Epic sadface: Username and password do not match any user in this service",
            id="invalid_credentials",
        ),
        pytest.param(
            "locked_out_user", "secret_sauce",
            "Epic sadface: Sorry, this user has been locked out.",
            id="locked_out_user",
        ),
    ],
)
def test_login_negative(driver, username, password, expected_error, request):
    allure.dynamic.title(f"Login gagal: {request.node.callspec.id}")
    login_page = LoginPage(driver)

    with allure.step("Coba login dengan kredensial tidak valid"):
        login_page.login(username, password)

    with allure.step("Verifikasi pesan error tampil"):
        # get_error_message menunggu elemen terlihat (explicit wait)
        actual_error = login_page.get_error_message()
        take_screenshot(driver, f"negative_login_{request.node.callspec.id}")

        assert login_page.is_visible(login_page.ERROR_MESSAGE)
        assert actual_error == expected_error
