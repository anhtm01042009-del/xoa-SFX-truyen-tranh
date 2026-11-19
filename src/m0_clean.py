"""M0: xoa chu tren trang truyen dai bang dong lenh.

Quy trinh: cat trang dai thanh cac doan (uu tien cat o dai trang) -> nhan dien chu
(comic-text-detector, ONNX) -> gom vung chu -> va nen (vung nen don sac: to mau;
vung phuc tap: LaMa) -> ghep lai. Khong ghi de anh goc.

Chay:
  python m0_clean.py --input ../samples/anh.png --out ../outputs \
      --detector ../models/comictextdetector.pt.onnx --lama ../models/big-lama.pt
"""
import argparse
import json
import os
import time
from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort
import torch
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ort.set_default_logger_severity(3)  # chi hien loi, bo cac canh bao "VerifyOutputSizes" vo hai


def peak_ram_mb():
    """RAM dinh cua tien trinh (MB). Linux: module resource; Windows: psutil (peak_wset)."""
    try:
        import resource
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    except ImportError:
        try:
            import psutil
            return psutil.Process().memory_info().peak_wset / 1024 / 1024
        except Exception:
            return 0  # khong do duoc


def split_tiles(img, max_h=1000, min_h=500, white_thr=245):
    """Tra ve (danh sach (y0, y1), so lan phai cat giua tranh)."""
    h = img.shape[0]
    gray = img.min(axis=2)  # kenh toi nhat: hang trang khi ca 3 kenh deu sang
    white_row = (gray >= white_thr).all(axis=1)
    tiles, y, forced = [], 0, 0
    while y < h:
        end = min(y + max_h, h)
        if end < h:
            cut = None
            for yy in range(end, y + min_h, -1):
                if white_row[yy - 1]:
                    cut = yy
                    break
            if cut is None:
                cut, forced = end, forced + 1
            end = cut
        tiles.append((y, end))
        y = end
    return tiles, forced


def detect_mask(sess, tile, thresh, det_scale):
    """Chay mo hinh phan doan chu (chi nhanh 'seg') tren doan anh, co the thu nho
    de nhanh hon (det_scale < 1). Dau vao khong can vuong, bat buoc chia het cho 64."""
    h, w = tile.shape[:2]
    nh, nw = max(32, int(round(h * det_scale))), max(32, int(round(w * det_scale)))
    resized = cv2.resize(tile, (nw, nh), interpolation=cv2.INTER_AREA if det_scale < 1 else cv2.INTER_LINEAR)
    ph, pw = (64 - nh % 64) % 64, (64 - nw % 64) % 64
    canvas = np.full((nh + ph, nw + pw, 3), 114, np.uint8)
    canvas[:nh, :nw] = resized
    x = canvas.astype(np.float32).transpose(2, 0, 1)[None] / 255.0
    seg = sess.run(None, {"images": x})[0][0, 0]
    seg = seg[:nh, :nw]
    seg = cv2.resize(seg, (tile.shape[1], tile.shape[0]), interpolation=cv2.INTER_LINEAR)
    return seg, (seg > thresh).astype(np.uint8)


def group_boxes(mask, grow=21, margin=40):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (grow, grow))
    merged = cv2.dilate(mask, k)
    n, _, stats, _ = cv2.connectedComponentsWithStats(merged, connectivity=8)
    h, w = mask.shape
    boxes = []
    for i in range(1, n):
        x, y, bw, bh, area = stats[i]
        if mask[y:y + bh, x:x + bw].sum() < 12:
            continue
        boxes.append((max(0, x - margin), max(0, y - margin),
                      min(w, x + bw + margin), min(h, y + bh + margin)))
    return boxes


def lama_inpaint(model, rgb, m):
    h, w = rgb.shape[:2]
    scale = 1.0
    if max(h, w) > 800:
        scale = 800 / max(h, w)
        rgb = cv2.resize(rgb, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
        m = cv2.resize(m, (rgb.shape[1], rgb.shape[0]), interpolation=cv2.INTER_NEAREST)
    hh, ww = rgb.shape[:2]
    ph, pw = (8 - hh % 8) % 8, (8 - ww % 8) % 8
    rgb_p = np.pad(rgb, ((0, ph), (0, pw), (0, 0)), mode="symmetric")
    m_p = np.pad(m, ((0, ph), (0, pw)), mode="symmetric")
    im_t = torch.from_numpy(rgb_p).permute(2, 0, 1)[None].float() / 255.0
    m_t = torch.from_numpy((m_p > 0).astype(np.float32))[None, None]
    with torch.inference_mode():
        out = model(im_t, m_t)
    out = (out[0].permute(1, 2, 0).clamp(0, 1).numpy() * 255).astype(np.uint8)[:hh, :ww]
    if scale != 1.0:
        out = cv2.resize(out, (w, h), interpolation=cv2.INTER_CUBIC)
    return out, scale != 1.0


def clean_box(model, crop, cmask, flat_std):
    """Tra ve (anh da va, kieu: 'flat'|'lama'|'lama_scaled')."""
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    ring = cv2.dilate(cmask, k) - cmask
    ring_px = crop[ring > 0]
    if len(ring_px) > 50 and ring_px.std(axis=0).max() < flat_std:
        fill = np.median(ring_px, axis=0).astype(np.uint8)
        out = crop.copy()
        out[cmask > 0] = fill
        return out, "flat"
    out, scaled = lama_inpaint(model, crop, cmask)
    return out, ("lama_scaled" if scaled else "lama")


def clean_region(img, poly, mode, sess, lama, thresh=0.2, dilate=11, det_scale=1.0,
                 flat_std=8.0, margin=48):
    """Xu ly mot vung nguoi dung khoanh (poly = [(x, y), ...] theo toa do anh).

    mode "auto": nhan dien chu nhay hon (nguong thap, do phan giai day du) CHI trong vung khoanh roi va.
    mode "all":  coi ca vung khoanh la vung can xoa (dung cho SFX ma may khong nhan ra).
    Tra ve None neu khong co gi de xoa; nguoc lai dict {x0, y0, old, new, stats}.
    Khong sua img; ben goi tu ghi new vao img[y0:y0+h, x0:x0+w].
    """
    h, w = img.shape[:2]
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    x0, y0 = max(0, int(min(xs)) - margin), max(0, int(min(ys)) - margin)
    x1, y1 = min(w, int(max(xs)) + margin), min(h, int(max(ys)) + margin)
    if x1 - x0 < 8 or y1 - y0 < 8:
        return None
    crop = img[y0:y1, x0:x1].copy()
    pm = np.zeros(crop.shape[:2], np.uint8)
    pts = np.array([[p[0] - x0, p[1] - y0] for p in poly], np.int32)
    cv2.fillPoly(pm, [pts], 1)
    if mode == "auto":
        _, m = detect_mask(sess, crop, thresh, det_scale)
        m = m & pm
    else:
        m = pm.copy()
    if int(m.sum()) < 12:
        return None
    m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate, dilate)))
    out = crop.copy()
    stats = {"flat": 0, "lama": 0, "lama_scaled": 0}
    for (bx0, by0, bx1, by1) in group_boxes(m):
        c = crop[by0:by1, bx0:bx1]
        cm = m[by0:by1, bx0:bx1]
        fixed, kind = clean_box(lama, c, cm, flat_std)
        stats[kind] += 1
        out[by0:by1, bx0:bx1][cm > 0] = fixed[cm > 0]
    return {"x0": x0, "y0": y0, "old": crop, "new": out, "stats": stats}


def load_models(detector, lama, threads=None):
    """Nap mo hinh nhan dien (ONNX) va LaMa (TorchScript). Tra ve (sess, lama)."""
    threads = threads or os.cpu_count()
    torch.set_num_threads(threads)
    so = ort.SessionOptions()
    so.intra_op_num_threads = threads
    sess = ort.InferenceSession(str(detector), so, providers=["CPUExecutionProvider"])
    model = torch.jit.load(str(lama), map_location="cpu").eval()
    return sess, model


class Cancelled(Exception):
    """Nguoi dung bam Dung."""


def process(path, out_dir, sess, lama, args, progress=None, cancel=None):
    """progress(so_doan_xong, tong_so_doan) duoc goi sau moi doan; cancel() tra ve True thi dung (nem Cancelled)."""
    t0 = time.time()
    img = np.array(Image.open(path).convert("RGB"))
    h, w = img.shape[:2]
    tiles, forced = split_tiles(img, args.max_tile)
    result = img.copy()
    full_mask = np.zeros((h, w), np.uint8)
    stats = {"flat": 0, "lama": 0, "lama_scaled": 0}
    t_det = t_inp = 0.0
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (args.dilate, args.dilate))
    for ti, (y0, y1) in enumerate(tiles):
        if cancel and cancel():
            raise Cancelled()
        if progress:
            progress(ti, len(tiles))
        tile = img[y0:y1]
        t = time.time()
        _, m = detect_mask(sess, tile, args.thresh, args.det_scale)
        t_det += time.time() - t
        if not m.any():
            continue
        m = cv2.dilate(m, k)
        full_mask[y0:y1] = np.maximum(full_mask[y0:y1], m)
        t = time.time()
        for (bx0, by0, bx1, by1) in group_boxes(m):
            crop = tile[by0:by1, bx0:bx1]
            cm = m[by0:by1, bx0:bx1]
            fixed, kind = clean_box(lama, crop, cm, args.flat_std)
            stats[kind] += 1
            region = result[y0 + by0:y0 + by1, bx0 + 0:bx1]
            region[cm > 0] = fixed[cm > 0]
        t_inp += time.time() - t
    if progress:
        progress(len(tiles), len(tiles))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / (Path(path).stem + "_clean.png")
    Image.fromarray(result).save(out_path)
    if args.save_mask:
        Image.fromarray(full_mask * 255).save(out_dir / (Path(path).stem + "_mask.png"))
    return {
        "file": Path(path).name, "size": [w, h], "tiles": len(tiles), "forced_cuts": forced,
        "boxes": stats, "sec_total": round(time.time() - t0, 1),
        "sec_detect": round(t_det, 1), "sec_inpaint": round(t_inp, 1),
        "peak_ram_mb": round(peak_ram_mb()), "output": out_path.name,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--detector", required=True)
    ap.add_argument("--lama", required=True)
    ap.add_argument("--thresh", type=float, default=0.3)
    ap.add_argument("--det-scale", type=float, default=0.75, help="thu nho doan anh truoc khi nhan dien (nhanh hon)")
    ap.add_argument("--dilate", type=int, default=7)
    ap.add_argument("--max-tile", type=int, default=1000)
    ap.add_argument("--flat-std", type=float, default=8.0)
    ap.add_argument("--save-mask", action="store_true")
    ap.add_argument("--threads", type=int, default=os.cpu_count())
    args = ap.parse_args()
    torch.set_num_threads(args.threads)
    so = ort.SessionOptions()
    so.intra_op_num_threads = args.threads
    sess = ort.InferenceSession(args.detector, so, providers=["CPUExecutionProvider"])
    lama = torch.jit.load(args.lama, map_location="cpu").eval()
    report = []
    for p in args.input:
        r = process(p, Path(args.out), sess, lama, args)
        print(json.dumps(r, ensure_ascii=False))
        report.append(r)
    (Path(args.out) / "m0_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
