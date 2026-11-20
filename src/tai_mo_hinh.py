"""Tai mo hinh ve thu muc models va tao ctd_seg.onnx.

Dung 2 cach:
  - Tu dong lenh (chay mot lan, can mang):  python src\\tai_mo_hinh.py
  - Tu app: goi tai_tat_ca(thu_muc, tien_do, huy) — app goi khi lan dau mo ma chua co mo hinh.
Tai ve file tam .part, du dung kich thuoc moi doi ten, nen mat mang giua chung khong de lai file hong.
"""
import ssl
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_seg_model import tao_seg  # noqa: E402

# Kich thuoc (byte) lay tu file da tai thanh cong tren may em Minh Anh ngay 2026-11-11.
FILES = {
    "comictextdetector.pt.onnx": (
        "https://github.com/zyddnys/manga-image-translator/releases/download/beta-0.2.1/comictextdetector.pt.onnx",
        94669756),
    "big-lama.pt": (
        "https://github.com/Sanster/models/releases/download/add_big_lama/big-lama.pt",
        205669692),
}
SEG = "ctd_seg.onnx"
TONG_BYTE = sum(size for _, size in FILES.values())


def ssl_context():
    """Kho chung chi cua may + bo chung chi certifi dong goi kem.

    Python dong goi tren Mac khong tu dung kho chung chi cua macOS -> loi CERTIFICATE_VERIFY_FAILED
    (may ban dung Mac M1, 2026-11-20). Giu kho cua may (Windows, mang co chung chi rieng) va them certifi.
    """
    ctx = ssl.create_default_context()
    try:
        import certifi
        ctx.load_verify_locations(cafile=certifi.where())
    except Exception:  # noqa: BLE001 - khong co certifi thi dung kho cua may
        pass
    return ctx


class DaHuy(Exception):
    """Nguoi dung bam Huy khi dang tai."""


def da_du(models_dir):
    """True neu da co du mo hinh de chay app."""
    d = Path(models_dir)
    return (d / SEG).exists() and (d / "big-lama.pt").exists() and \
        (d / "big-lama.pt").stat().st_size == FILES["big-lama.pt"][1]


def _tai_mot(url, dst, size, da_tai_truoc, tien_do, huy):
    tmp = dst.with_suffix(dst.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": "XoaChuTruyenTranh"})
    got = 0
    with urllib.request.urlopen(req, timeout=60, context=ssl_context()) as r, open(tmp, "wb") as f:
        while True:
            if huy and huy():
                f.close()
                tmp.unlink(missing_ok=True)
                raise DaHuy()
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
            got += len(chunk)
            if tien_do:
                tien_do(da_tai_truoc + got, TONG_BYTE, dst.name)
    if got != size:
        tmp.unlink(missing_ok=True)
        raise IOError(f"Tải {dst.name} không đủ ({got} / {size} byte). Kiểm tra mạng rồi thử lại.")
    tmp.replace(dst)


def tai_tat_ca(models_dir, tien_do=None, huy=None):
    """Tai cac file con thieu, roi tao ctd_seg.onnx. tien_do(byte_da_tai, tong_byte, ten_file)."""
    d = Path(models_dir)
    d.mkdir(parents=True, exist_ok=True)
    done = 0
    for name, (url, size) in FILES.items():
        dst = d / name
        if dst.exists() and dst.stat().st_size == size:
            done += size
            if tien_do:
                tien_do(done, TONG_BYTE, name)
            continue
        _tai_mot(url, dst, size, done, tien_do, huy)
        done += size
    seg = d / SEG
    if not seg.exists():
        if tien_do:
            tien_do(TONG_BYTE, TONG_BYTE, SEG)
        tmp = d / (SEG + ".part")
        tao_seg(d / "comictextdetector.pt.onnx", tmp)
        tmp.replace(seg)
    return seg


if __name__ == "__main__":
    MODELS = Path(__file__).resolve().parent.parent / "models"
    last = [-1]

    def in_tien_do(got, total, name):
        pct = int(got * 100 / total)
        if pct != last[0]:
            last[0] = pct
            print(f"\r{name}: {pct}%   ", end="", flush=True)

    tai_tat_ca(MODELS, in_tien_do)
    print("\nsan sang:", MODELS / SEG)
