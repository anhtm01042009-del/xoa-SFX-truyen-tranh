# -*- mode: python ; coding: utf-8 -*-
# Dong goi kieu thu muc (onedir): khoi dong nhanh hon kieu 1 file vi khong phai giai nen torch moi lan mo.
# Chay tu thu muc goc du an:  pyinstaller --noconfirm packaging/XoaChuTruyenTranh.spec
from pathlib import Path

ROOT = Path(SPECPATH).parent

a = Analysis(
    [str(ROOT / "src" / "app.py")],
    pathex=[str(ROOT / "src")],
    datas=[(str(ROOT / "assets"), "assets")],
    hiddenimports=["onnx", "onnx.utils", "make_seg_model", "tai_mo_hinh", "duong_dan", "phien_ban"],
    excludes=["tkinter", "matplotlib", "IPython", "pytest", "torchvision", "torchaudio",
              "PySide6.QtWebEngineCore", "PySide6.QtWebEngineWidgets", "PySide6.Qt3DCore",
              "PySide6.QtMultimedia", "PySide6.QtQuick", "PySide6.QtQml", "PySide6.QtCharts",
              "PySide6.QtDataVisualization", "PySide6.QtPdf"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="XoaChuTruyenTranh",
    console=False,
    icon=str(ROOT / "assets" / "icon.ico"),
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="XoaChuTruyenTranh")
