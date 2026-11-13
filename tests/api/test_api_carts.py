import allure
import pytest

pytestmark = pytest.mark.api


@allure.feature("Carts")
@allure.title("Total dan jumlah di keranjang konsisten dengan isinya")
def test_cart_totals_are_consistent(client):
    response = client.cart(1)

    assert response.status_code == 200
    cart = response.json()
    products = cart["products"]

    assert len(products) > 0
    assert cart["total"] == pytest.approx(sum(p["total"] for p in products), abs=0.05)
    assert cart["totalQuantity"] == sum(p["quantity"] for p in products)


@allure.feature("Carts")
@allure.title("Keranjang yang tidak ada mengembalikan 404")
def test_unknown_cart_returns_404(client):
    response = client.cart(999999)

    assert response.status_code == 404


@allure.feature("Carts")
@allure.title("Menambah keranjang baru mengembalikan keranjang tersebut")
def test_add_cart(client):
    items = [{"id": 144, "quantity": 4}, {"id": 98, "quantity": 1}]

    response = client.add_cart(user_id=1, products=items)

    # DummyJSON hanya mensimulasikan: respons sukses, data tidak disimpan
    assert response.status_code in (200, 201)
    body = response.json()
    assert body["userId"] == 1
    assert len(body["products"]) == len(items)
