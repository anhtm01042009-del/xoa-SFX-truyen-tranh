"""Kiem tra nhanh truoc khi dong goi: cac module cua app nap duoc va phan cat trang chay dung.
Chay tu thu muc goc:  python packaging/kiem_tra_nap.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import numpy as np  # noqa: E402

import duong_dan  # noqa: E402,F401
import m0_clean  # noqa: E402
import phien_ban  # noqa: E402
import tai_mo_hinh  # noqa: E402

# Trang gia 2500 px, co dai trang o giua: phai cat thanh cac doan <= 1000 px, noi lien nhau.
img = np.full((2500, 300, 3), 30, np.uint8)
img[900:960] = 255
img[1800:1850] = 255
tiles, forced = m0_clean.split_tiles(img)
assert tiles[0][0] == 0 and tiles[-1][1] == 2500, tiles
assert all(b - a <= 1000 for a, b in tiles), tiles
assert all(tiles[i][1] == tiles[i + 1][0] for i in range(len(tiles) - 1)), tiles
assert tai_mo_hinh.TONG_BYTE > 250_000_000
print("KIEM TRA NAP DAT", phien_ban.__version__, tiles, "cat giua tranh:", forced)
