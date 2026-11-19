"""Duong dan dung chung cho app.

- Chay tu ma nguon (py src\\app.py): mo hinh o <du an>\\models, ket qua o <du an>\\outputs (nhu truoc).
- Chay ban dong goi (XoaChuTruyenTranh.exe): mo hinh o %LOCALAPPDATA%\\XoaChuTruyenTranh\\models
  (giu lai khi tai ban moi, khong phai tai lai), ket qua mac dinh o Pictures\\XoaChuTruyenTranh.
"""
import os
import sys
from pathlib import Path

APP_NAME = "XoaChuTruyenTranh"
FROZEN = bool(getattr(sys, "frozen", False))

if FROZEN:
    APP_DIR = Path(sys.executable).resolve().parent
    _local = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    DATA_DIR = Path(_local) / APP_NAME
    MODELS_DIR = DATA_DIR / "models"
    OUTPUTS_DIR = Path.home() / "Pictures" / APP_NAME
else:
    APP_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = APP_DIR
    MODELS_DIR = APP_DIR / "models"
    OUTPUTS_DIR = APP_DIR / "outputs"

ASSETS_DIR = Path(getattr(sys, "_MEIPASS", APP_DIR)) / "assets"
LOG_FILE = DATA_DIR / "nhat-ky-loi.txt"
