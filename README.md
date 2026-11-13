# SauceDemo Selenium Automation

[![Tests](https://github.com/salmahadiatna/saucedemo-selenium-automation/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/salmahadiatna/saucedemo-selenium-automation/actions/workflows/tests.yml)

Project test automation dengan dua layer:

- **UI**: [SauceDemo](https://www.saucedemo.com/) diuji dengan Selenium WebDriver, Python, dan pytest, memakai pola Page Object Model (POM).
- **API**: [DummyJSON](https://dummyjson.com/) (API latihan e-commerce) diuji dengan `requests` dan pytest.

Hasil test dilaporkan lewat Allure dan dijalankan otomatis di GitHub Actions.

**[Lihat laporan Allure terbaru](https://salmahadiatna.github.io/saucedemo-selenium-automation/)**

## Tools & Teknologi

- Python 3.12
- Selenium WebDriver (UI) dan `requests` (API)
- pytest (fixture, parametrize, marker, xfail)
- Page Object Model (POM)
- Allure Report
- GitHub Actions + GitHub Pages

## Cakupan Skenario

Total **42 test**: 38 test normal dan 4 test known bug (`xfail`).
Detail langkah dan expected result tiap skenario ada di spreadsheet
`docs/test_scenarios.xlsx`.

### Layer UI (20 test)

| Modul | File | Skenario | Jumlah |
|---|---|---|---|
| E2E | `test_e2e_pom.py` | Login, tambah produk, checkout sampai pesan sukses | 1 |
| Login (positif) | `test_login_positive.py` | Login berhasil dengan `standard_user` | 1 |
| Login (negatif) | `test_login_negative.py` | Username kosong, password kosong, username salah, password salah, kredensial salah, `locked_out_user` | 6 |
| Logout | `test_logout.py` | Logout kembali ke halaman login | 1 |
| Inventory | `test_inventory_sort.py` | Urutkan nama A-Z, Z-A, harga rendah-tinggi, tinggi-rendah | 4 |
| Cart | `test_cart.py` | Hapus satu item dari keranjang | 1 |
| Checkout | `test_checkout_total.py` | Validasi harga item, subtotal, pajak, dan total | 1 |
| `problem_user` | `test_problem_user.py` | 1 login normal + 4 known bug | 5 |

### Layer API (22 test)

| Modul | File | Skenario | Jumlah |
|---|---|---|---|
| Products | `tests/api/test_api_products.py` | Daftar produk, limit, pagination, field wajib, produk per ID, 404, pencarian (ada dan tanpa hasil), kategori, sort harga, waktu respons | 11 |
| Auth | `tests/api/test_api_auth.py` | Login berhasil, 4 skenario login ditolak, `/auth/me` dengan token valid, tanpa token, dan token palsu | 8 |
| Carts | `tests/api/test_api_carts.py` | Total keranjang konsisten, keranjang tidak ada (404), tambah keranjang | 3 |

### Tentang test `problem_user` (xfail)

`problem_user` adalah akun SauceDemo yang sengaja bermasalah. Test untuk
akun ini memeriksa perilaku yang **seharusnya benar**, dan bug yang sudah
dikenal ditandai `xfail` (non-strict):

| Hasil | Arti |
|---|---|
| XFAIL | Bug masih ada (hasil yang diharapkan, CI tetap hijau) |
| XPASS | Perilaku ternyata sudah benar, test perlu ditinjau ulang |

Bug yang dicakup: semua produk menampilkan gambar yang sama, pengurutan
tidak berfungsi, sebagian produk tidak bisa ditambahkan ke keranjang, dan
input field checkout tidak tersimpan dengan benar.

### Catatan temuan API

- DummyJSON mengembalikan **HTTP 500** (bukan 401) untuk token yang tidak
  valid pada `/auth/me`. Test `test_me_with_invalid_token_is_not_authenticated`
  memastikan token palsu tetap tidak berhasil mengautentikasi.
- DummyJSON menyetel cookie saat login. Client test dibuat **tanpa state**
  (cookie dibersihkan setiap request) supaya test "tanpa token" benar-benar
  tidak membawa kredensial.
- `POST /carts/add` hanya mensimulasikan: respons sukses, tetapi data tidak
  disimpan di server.

## Struktur Project

```
├── .github/workflows/tests.yml   # CI: test API lalu UI + publikasi laporan Allure
├── api/
│   └── client.py                 # pembungkus requests untuk DummyJSON
├── pages/
│   ├── base_page.py              # helper umum (explicit wait, retry saat elemen basi)
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── api/
│   │   ├── conftest.py           # fixture client dan auth_token
│   │   ├── test_api_products.py
│   │   ├── test_api_auth.py
│   │   └── test_api_carts.py
│   ├── test_e2e_pom.py
│   ├── test_login_positive.py
│   ├── test_login_negative.py
│   ├── test_logout.py
│   ├── test_inventory_sort.py
│   ├── test_cart.py
│   ├── test_checkout_total.py
│   └── test_problem_user.py
├── docs/test_scenarios.xlsx      # detail skenario dan ringkasan hasil
├── conftest.py                   # fixture driver, logged_in, screenshot saat gagal
├── utils.py                      # helper screenshot (juga dilampirkan ke Allure)
├── pytest.ini                    # marker: ui, api
└── requirements.txt
```

## Cara Menjalankan

### 1. Instalasi

```bash
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 2. Jalankan test

```bash
python -m pytest -v -rxX          # semua (42 test)
python -m pytest -m api           # hanya API (cepat, tanpa browser)
python -m pytest -m ui            # hanya UI
```

Opsi `-rxX` menampilkan ringkasan test XFAIL dan XPASS di akhir.

### 3. Mode headless (UI tanpa jendela Chrome)

```powershell
# PowerShell
$env:HEADLESS = "1"
python -m pytest -m ui -v
```

```bash
# Linux / macOS
HEADLESS=1 python -m pytest -m ui -v
```

### 4. Laporan Allure lokal (opsional)

Hasil test tersimpan di `allure-results/`. Untuk melihat laporannya,
pasang [Allure CLI](https://allurereport.org/docs/install/), lalu:

```bash
allure serve allure-results
```

## Test Evidence

- **UI**: screenshot langkah penting disimpan otomatis di `screenshots/` dan
  dilampirkan ke Allure. Jika test gagal, `FAILED_<nama test>` diambil otomatis.
- **API**: setiap request dan respons dilampirkan ke Allure. Nilai token dan
  password disamarkan (`***`) supaya tidak ikut terbit di laporan publik.

## Continuous Integration

Setiap push dan pull request ke `main` menjalankan:

1. Test API (`pytest -m api`), cepat dan tanpa browser.
2. Test UI headless (`pytest -m ui`), tetap berjalan walaupun test API gagal.

Pada push ke `main`, laporan Allure gabungan dipublikasikan ke GitHub Pages
(link di bagian atas), dan hasil mentah serta screenshot diunggah sebagai
artifact.

## Teknik yang Digunakan

- Page Object Model dengan `BasePage` yang tahan terhadap elemen basi (retry)
- Explicit wait (`WebDriverWait`), tanpa `time.sleep`
- Data-driven test dengan `pytest.mark.parametrize` (UI dan API)
- Fixture terpusat (`driver`, `logged_in`, `logged_in_problem_user`, `client`, `auth_token`)
- Marker `ui` dan `api` untuk memilih layer yang dijalankan
- `xfail` untuk mendokumentasikan known bug tanpa merusak CI
- Validasi status code, struktur dan isi JSON, serta waktu respons
- Screenshot otomatis saat gagal, request/respons API di Allure
- Langkah dan judul test yang terbaca di Allure (`@allure.step`, `@allure.title`)

## Troubleshooting

- **`ModuleNotFoundError: No module named 'allure'` atau `'requests'`**:
  pastikan venv aktif dan jalankan `pip install -r requirements.txt`.
- **`fixture 'driver' not found`**: pastikan `conftest.py` berada di root
  project, sejajar dengan folder `tests/`.
- **Chrome tidak terbuka saat test UI berjalan**: variabel `HEADLESS` masih
  bernilai `1` di terminal. Jalankan `Remove-Item Env:HEADLESS` (PowerShell).
- **Test API gagal karena jaringan**: alamat API bisa diganti lewat variabel
  `API_BASE_URL` (default `https://dummyjson.com`).
