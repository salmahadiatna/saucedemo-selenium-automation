# SauceDemo Selenium Automation

[![Tests](https://github.com/salmahadiatna/saucedemo-selenium-automation/actions/workflows/tests.yml/badge.svg)](https://github.com/salmahadiatna/saucedemo-selenium-automation/actions/workflows/tests.yml)

Project web automation testing untuk [SauceDemo](https://www.saucedemo.com/)
menggunakan Selenium WebDriver, Python, dan pytest, dengan pola
Page Object Model (POM), laporan Allure, dan CI di GitHub Actions.

**[Lihat laporan Allure terbaru](https://salmahadiatna.github.io/saucedemo-selenium-automation/)**

## Tools & Teknologi

- Python 3.12
- Selenium WebDriver
- pytest (fixture, parametrize, marker, xfail)
- Page Object Model (POM)
- Allure Report
- GitHub Actions + GitHub Pages

## Cakupan Skenario

Total **20 test**: 16 test normal dan 4 test known bug (`xfail`).

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

Detail langkah dan expected result tiap skenario ada di spreadsheet
`docs/test_scenarios.xlsx`.

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

## Struktur Project

```
├── .github/workflows/tests.yml   # CI: test headless + publikasi laporan Allure
├── pages/
│   ├── base_page.py              # helper umum (explicit wait, klik, ketik)
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── test_e2e_pom.py
│   ├── test_login_positive.py
│   ├── test_login_negative.py
│   ├── test_logout.py
│   ├── test_inventory_sort.py
│   ├── test_cart.py
│   ├── test_checkout_total.py
│   └── test_problem_user.py
├── conftest.py                   # fixture driver, logged_in, screenshot saat gagal
├── utils.py                      # helper screenshot (juga dilampirkan ke Allure)
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
python -m pytest -v -rxX
```

Opsi `-rxX` menampilkan ringkasan test XFAIL dan XPASS di akhir.

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

### 4. Laporan Allure lokal (opsional)

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

Setiap push dan pull request ke `main` menjalankan seluruh test secara
headless di GitHub Actions. Pada push ke `main`, laporan Allure
dipublikasikan ke GitHub Pages (link di bagian atas README), dan hasil
mentah serta screenshot diunggah sebagai artifact.

## Teknik yang Digunakan

- Page Object Model dengan `BasePage` sebagai kelas dasar
- Explicit wait (`WebDriverWait`), tanpa `time.sleep`
- Data-driven test dengan `pytest.mark.parametrize`
- Fixture terpusat di `conftest.py` (`driver`, `logged_in`, `logged_in_problem_user`)
- `xfail` untuk mendokumentasikan known bug tanpa merusak CI
- Screenshot otomatis saat test gagal, dilampirkan ke Allure
- Langkah dan judul test yang terbaca di Allure (`@allure.step`, `@allure.title`)

## Troubleshooting

- **`ModuleNotFoundError: No module named 'allure'`**: pastikan venv aktif
  dan jalankan `pip install -r requirements.txt`.
- **`fixture 'driver' not found`**: pastikan `conftest.py` berada di root
  project, sejajar dengan folder `tests/`.
- **Chrome tidak terbuka saat test berjalan**: variabel `HEADLESS` masih
  bernilai `1` di terminal. Jalankan `Remove-Item Env:HEADLESS` (PowerShell).
