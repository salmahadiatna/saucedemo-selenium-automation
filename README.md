# SauceDemo Selenium Automation

![Tests](https://github.com/salmahadiatna/saucedemo-selenium-automation/actions/workflows/tests.yml/badge.svg)

[Lihat laporan Allure](https://salmahadiatna.github.io/saucedemo-selenium-automation/)

Project web automation testing untuk [SauceDemo](https://www.saucedemo.com/)
menggunakan Selenium WebDriver, Python, dan pytest, dengan pola
Page Object Model (POM) dan laporan Allure.

## Tools & Teknologi

- Python 3.12
- Selenium WebDriver
- pytest (parametrize, marker, fixture)
- Page Object Model (POM)
- Allure Report
- GitHub Actions (CI)

## Skenario Test

| File | Skenario |
|---|---|
| `test_e2e_pom.py` | Login, tambah produk ke keranjang, isi data pengiriman, selesaikan checkout, verifikasi pesan sukses |
| `test_login_positive.py` | Login berhasil dengan `standard_user` |
| `test_login_negative.py` | 6 skenario login gagal: username kosong, password kosong, username salah, password salah, kredensial salah, dan `locked_out_user` |

Total: 8 test.

## Struktur Project

```
├── pages/
│   ├── base_page.py        # helper umum (explicit wait, klik, ketik)
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── test_e2e_pom.py
│   ├── test_login_positive.py
│   └── test_login_negative.py
├── conftest.py             # fixture driver, screenshot otomatis saat gagal
├── utils.py                # helper screenshot (juga dilampirkan ke Allure)
├── pytest.ini
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
python -m pytest -v
```

### 3. Mode headless (tanpa jendela Chrome)

```powershell
# PowerShell
$env:HEADLESS = "1"
python -m pytest -v
```

```bash
# Linux / macOS
HEADLESS=1 python -m pytest -v
```

### 4. Laporan Allure (opsional)

Hasil test tersimpan di `allure-results/`. Untuk melihat laporannya,
pasang [Allure CLI](https://allurereport.org/docs/install/), lalu:

```bash
allure serve allure-results
```

## Test Evidence

Screenshot langkah penting disimpan otomatis di folder `screenshots/`
dan dilampirkan ke laporan Allure. Jika test gagal, screenshot
`FAILED_<nama test>` diambil otomatis.

## Continuous Integration

Test dijalankan otomatis (headless) di GitHub Actions setiap push dan
pull request ke branch `main`. Hasil Allure diunggah sebagai artifact
pada setiap run.

## Teknik yang Digunakan

- Page Object Model dengan `BasePage` sebagai kelas dasar
- Explicit wait (`WebDriverWait`), tanpa `time.sleep`
- Data-driven test dengan `pytest.mark.parametrize`
- Fixture terpusat di `conftest.py`
- Screenshot otomatis saat test gagal
- Langkah dan judul test yang terbaca di Allure (`@allure.step`)