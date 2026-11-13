import pytest

from api.client import DEMO_PASSWORD, DEMO_USERNAME, DummyJsonClient


@pytest.fixture(scope="session")
def client():
    return DummyJsonClient()


@pytest.fixture(scope="session")
def auth_token(client):
    response = client.login(DEMO_USERNAME, DEMO_PASSWORD)
    assert response.status_code == 200, f"Login gagal: {response.text}"

    body = response.json()
    token = body.get("accessToken") or body.get("token")
    assert token, "Respons login tidak berisi token"
    return token
