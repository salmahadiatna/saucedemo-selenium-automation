import re
from pathlib import Path

import allure

SCREENSHOT_DIR = Path(__file__).resolve().parent / "screenshots"


def take_screenshot(driver, name):
    """Simpan screenshot ke folder screenshots/ dan tempel ke laporan Allure."""
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    # Nama test parametrize bisa memuat karakter seperti [ ] yang tidak aman di nama file
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", name)
    path = SCREENSHOT_DIR / f"{safe_name}.png"

    driver.save_screenshot(str(path))
    allure.attach.file(
        str(path), name=name, attachment_type=allure.attachment_type.PNG
    )
    return path
