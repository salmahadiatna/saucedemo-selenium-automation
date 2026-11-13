import allure
import pytest

from api.client import DEMO_PASSWORD as VALID_PASSWORD
from api.client import DEMO_USERNAME as VALID_USERNAME

pytestmark = pytest.mark.api


@allure.feature("Auth")
@allure.title("Login berhasil mengembalikan token")
def test_login_success(client):
    response = client.login(VALID_USERNAME, VALID_PASSWORD)

    assert response.status_code == 200
    body = response.json()
    assert body["username"] == VALID_USERNAME
    assert body.get("accessToken") or body.get("token")


@allure.feature("Auth")
@pytest.mark.parametrize(
    "username, password",
    [
        pytest.param(VALID_USERNAME, "password_salah", id="wrong_password"),
        pytest.param("user_tidak_ada_xyz", VALID_PASSWORD, id="unknown_user"),
        pytest.param(VALID_USERNAME, "", id="empty_password"),
        pytest.param("", VALID_PASSWORD, id="empty_username"),
    ],
)
def test_login_rejected(client, username, password, request):
    allure.dynamic.title(f"Login ditolak: {request.node.callspec.id}")

    response = client.login(username, password)

    assert response.status_code == 400
    assert "message" in response.json()


@allure.feature("Auth")
@allure.title("Endpoint /auth/me dengan token valid")
def test_me_with_valid_token(client, auth_token):
    response = client.me(token=auth_token)

    assert response.status_code == 200
    assert response.json()["username"] == VALID_USERNAME


@allure.feature("Auth")
@allure.title("Endpoint /auth/me tanpa token ditolak")
def test_me_without_token_is_rejected(client):
    response = client.me()

    assert response.status_code in (401, 403)


@allure.feature("Auth")
@allure.title("Endpoint /auth/me dengan token palsu tidak mengautentikasi")
def test_me_with_invalid_token_is_not_authenticated(client):
    response = client.me(token="token_palsu_xyz")