import json
import os

import allure
import requests

BASE_URL = os.getenv("API_BASE_URL", "https://dummyjson.com")
TIMEOUT = 10

# Akun demo yang memang disediakan DummyJSON untuk latihan (bukan rahasia)
DEMO_USERNAME = "emilys"
DEMO_PASSWORD = "emilyspass"

# Nilai field ini disamarkan di lampiran Allure, supaya token tidak
# ikut terpublikasi di laporan GitHub Pages.
SENSITIVE_KEYS = {"accessToken", "refreshToken", "token", "password"}


def _mask(value):
    if isinstance(value, dict):
        return {
            k: ("***" if k in SENSITIVE_KEYS else _mask(v)) for k, v in value.items()
        }
    if isinstance(value, list):
        return [_mask(v) for v in value]
    return value


def _describe(response):
    elapsed_ms = round(response.elapsed.total_seconds() * 1000)
    try:
        body = json.dumps(_mask(response.json()), indent=2, ensure_ascii=False)
    except ValueError:
        body = response.text
    return f"HTTP {response.status_code} ({elapsed_ms} ms)\n{body[:3000]}"


class DummyJsonClient:
    """Pembungkus kecil untuk https://dummyjson.com (API latihan e-commerce)."""

    def __init__(self, base_url=BASE_URL, timeout=TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, method, path, token=None, **kwargs):
        headers = kwargs.pop("headers", {})
        if token:
            headers["Authorization"] = f"Bearer {token}"

        # Parameter bernilai None tidak dikirim
        params = kwargs.pop("params", None)
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        with allure.step(f"{method} {path}"):
            response = self.session.request(
                method,
                f"{self.base_url}{path}",
                headers=headers,
                params=params,
                timeout=self.timeout,
                **kwargs,
            )
            allure.attach(
                _describe(response),
                name="Response",
                attachment_type=allure.attachment_type.TEXT,
            )

        # Client tanpa state: token hanya dikirim lewat header yang eksplisit
        self.session.cookies.clear()
        return response

    # ---------- produk ----------

    def products(self, limit=None, skip=None, sort_by=None, order=None):
        return self._request(
            "GET",
            "/products",
            params={"limit": limit, "skip": skip, "sortBy": sort_by, "order": order},
        )

    def product(self, product_id):
        return self._request("GET", f"/products/{product_id}")

    def search_products(self, query):
        return self._request("GET", "/products/search", params={"q": query})

    def categories(self):
        return self._request("GET", "/products/categories")

    # ---------- auth ----------

    def login(self, username, password):
        return self._request(
            "POST", "/auth/login", json={"username": username, "password": password}
        )

    def me(self, token=None):
        return self._request("GET", "/auth/me", token=token)

    # ---------- keranjang ----------

    def cart(self, cart_id):
        return self._request("GET", f"/carts/{cart_id}")

    def add_cart(self, user_id, products):
        return self._request(
            "POST", "/carts/add", json={"userId": user_id, "products": products}
        )