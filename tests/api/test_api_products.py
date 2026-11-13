import allure
import pytest

pytestmark = pytest.mark.api

MAX_RESPONSE_SECONDS = 5  # batas longgar agar tidak flaky di CI


@allure.feature("Products")
@allure.title("Daftar produk mengembalikan data")
def test_list_products_returns_data(client):
    response = client.products()

    assert response.status_code == 200
    body = response.json()
    assert len(body["products"]) > 0
    assert isinstance(body["total"], int)
    assert body["total"] >= len(body["products"])


@allure.feature("Products")
@allure.title("Parameter limit membatasi jumlah produk")
def test_limit_parameter(client):
    response = client.products(limit=5)

    assert response.status_code == 200
    body = response.json()
    assert len(body["products"]) == 5
    assert body["limit"] == 5


@allure.feature("Products")
@allure.title("Halaman pertama dan kedua tidak saling tumpang tindih")
def test_pagination_pages_do_not_overlap(client):
    page_one = client.products(limit=3, skip=0).json()
    page_two = client.products(limit=3, skip=3).json()

    ids_one = {p["id"] for p in page_one["products"]}
    ids_two = {p["id"] for p in page_two["products"]}

    assert page_two["skip"] == 3
    assert ids_one.isdisjoint(ids_two)


@allure.feature("Products")
@allure.title("Satu produk memiliki field wajib dengan tipe benar")
def test_product_has_required_fields(client):
    product = client.product(1).json()

    for field in ("id", "title", "price", "category"):
        assert field in product, f"Field '{field}' tidak ada"
    assert isinstance(product["title"], str)
    assert isinstance(product["price"], (int, float))


@allure.feature("Products")
@allure.title("Ambil produk berdasarkan ID")
def test_get_single_product(client):
    response = client.product(1)

    assert response.status_code == 200
    assert response.json()["id"] == 1


@allure.feature("Products")
@allure.title("Produk yang tidak ada mengembalikan 404")
def test_unknown_product_returns_404(client):
    response = client.product(999999)

    assert response.status_code == 404
    assert "message" in response.json()


@allure.feature("Products")
@allure.title("Pencarian produk mengembalikan hasil")
def test_search_products(client):
    response = client.search_products("phone")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] >= 1
    assert len(body["products"]) >= 1


@allure.feature("Products")
@allure.title("Pencarian tanpa hasil mengembalikan daftar kosong")
def test_search_without_results(client):
    response = client.search_products("zzzzxxxxyyyy")

    assert response.status_code == 200
    body = response.json()
    assert body["products"] == []
    assert body["total"] == 0


@allure.feature("Products")
@allure.title("Daftar kategori tidak kosong")
def test_categories_not_empty(client):
    response = client.categories()

    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)
    assert len(categories) > 0


@allure.feature("Products")
@allure.title("Pengurutan harga naik")
def test_sort_by_price_ascending(client):
    response = client.products(limit=10, sort_by="price", order="asc")

    assert response.status_code == 200
    prices = [p["price"] for p in response.json()["products"]]
    assert prices == sorted(prices)


@allure.feature("Products")
@allure.title("Waktu respons daftar produk di bawah batas")
def test_response_time_is_acceptable(client):
    response = client.products()

    assert response.elapsed.total_seconds() < MAX_RESPONSE_SECONDS
