"""Giao dien M1: xoa chu thoai tren trang truyen (ke ca trang dai).

Chay:  py -3.12 src\\app.py     (hoac bam doi chay_app.bat)
Quy tac: khong bao gio ghi de anh goc; ket qua luu thanh <ten>_clean.png trong thu muc luu.
"""
import re
import sys
import time
from argparse import Namespace
from pathlib import Path

# QUAN TRONG: nap m0_clean (numpy, cv2, onnxruntime, torch) TRUOC PySide6.
# Neu nap sau, co che nhap cua PySide6 doc ma nguon tung module va lam cham hang chuc lan.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import m0_clean  # noqa: E402
import tai_mo_hinh  # noqa: E402
from duong_dan import ASSETS_DIR, FROZEN, LOG_FILE, MODELS_DIR, OUTPUTS_DIR  # noqa: E402
from phien_ban import __version__  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

import shutil
import os
import traceback

from PySide6.QtCore import QPointF, QThread, QTimer, Qt, QUrl, Signal
from PySide6.QtGui import (QAction, QColor, QDesktopServices, QIcon, QImage, QImageReader, QKeySequence, QPainter,
                           QPen,
                           QPixmap, QPolygonF, QShortcut)
from PySide6.QtWidgets import (
    QApplication, QComboBox, QDockWidget, QDoubleSpinBox, QFileDialog, QFormLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QMainWindow, QMessageBox, QProgressBar, QProgressDialog, QPushButton,
    QScrollArea, QSplitter, QSpinBox, QToolBar, QVBoxLayout, QWidget,
)

MODEL_DET = MODELS_DIR / "ctd_seg.onnx"
MODEL_LAMA = MODELS_DIR / "big-lama.pt"
EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

STYLE = """
QMainWindow, QWidget { font-size: 13px; }
QToolBar { spacing: 6px; padding: 4px; }
QPushButton#primary { background: #2d6cdf; color: white; border: none; padding: 6px 16px; border-radius: 4px; font-weight: bold; }
QPushButton#primary:disabled { background: #9db7e8; }
QPushButton#stop { padding: 6px 14px; }
QListWidget { border: 1px solid #c8c8c8; }
QProgressBar { text-align: center; height: 18px; }
QLabel#hint { color: #666; }
QToolButton:checked { background: #e03131; color: white; border-radius: 4px; }
"""


def natural_key(p):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p.name)]


def read_image(path):
    reader = QImageReader(str(path))
    try:
        reader.setAllocationLimit(0)  # trang dai co the vuot gioi han mac dinh cua Qt
    except AttributeError:
        pass
    return reader.read()


class CanvasLabel(QLabel):
    """Nhan hien anh, cho phep khoanh vung bang chuot (hinh chu nhat hoac tu do)."""

    lasso = Signal(list)  # [(x, y), ...] theo toa do cua anh dang hien (pixmap)

    def __init__(self, text):
        super().__init__(text)
        self.active = False
        self.shape = "rect"
        self.pts = []
        self.drawing = False

    def set_active(self, on):
        self.active = on
        self.pts = []
        self.drawing = False
        self.setCursor(Qt.CrossCursor if on else Qt.ArrowCursor)
        self.update()

    def _has_pixmap(self):
        pm = self.pixmap()
        return pm is not None and not pm.isNull()

    def mousePressEvent(self, e):
        if self.active and e.button() == Qt.LeftButton and self._has_pixmap():
            p = e.position()
            self.drawing = True
            self.pts = [(p.x(), p.y())]
            self.update()
        else:
            super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if self.drawing:
            p = e.position()
            if self.shape == "rect":
                self.pts = [self.pts[0], (p.x(), p.y())]
            else:
                self.pts.append((p.x(), p.y()))
            self.update()
        else:
            super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        if self.drawing:
            self.drawing = False
            pts, self.pts = self.pts, []
            self.update()
            if self.shape == "rect" and len(pts) == 2:
                (ax, ay), (bx, by) = pts
                if abs(bx - ax) < 6 or abs(by - ay) < 6:
                    return
                pts = [(ax, ay), (bx, ay), (bx, by), (ax, by)]
            if len(pts) >= 3:
                self.lasso.emit(pts)
        else:
            super().mouseReleaseEvent(e)

    def paintEvent(self, e):
        super().paintEvent(e)
        if not self.pts:
            return
        pts = self.pts
        if self.shape == "rect" and len(pts) == 2:
            (ax, ay), (bx, by) = pts
            pts = [(ax, ay), (bx, ay), (bx, by), (ax, by)]
        painter = QPainter(self)
        pen = QPen(QColor("#e03131"), 2, Qt.DashLine)
        painter.setPen(pen)
        painter.setBrush(QColor(224, 49, 49, 45))
        painter.drawPolygon(QPolygonF([QPointF(x, y) for x, y in pts]))
        painter.end()


class ImageView(QScrollArea):
    """Hien anh dai, thu phong theo chieu rong (hoac ty le co dinh)."""

    lasso = Signal(list)

    def __init__(self, title):
        super().__init__()
        self.setWidgetResizable(False)
        self.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.label = CanvasLabel(title)
        self.label.lasso.connect(self.lasso)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("hint")
        self.setWidget(self.label)
        self.label.resize(300, 120)
        self.image = None
        self.mode = "fit"
        self._last = None
        self._empty_text = title
        # thanh cuon doc luon hien de chieu rong khung khong dao dong khi no bat/tat
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def set_empty(self, text):
        self.image = None
        self.label.setPixmap(QPixmap())
        self.label.setText(text)
        self.label.resize(max(200, self.viewport().width()), 120)

    def set_image(self, image):
        self.image = image
        self._last = None
        self._render()

    def set_mode(self, mode):
        self.mode = mode
        self._last = None
        self._render()

    def _render(self):
        if self.image is None or self.image.isNull():
            return
        iw = self.image.width()
        if self.mode == "fit":
            target = max(100, self.viewport().width() - 4)
        else:
            target = int(iw * self.mode)
        if (id(self.image), target) == self._last:
            return  # tranh ve lai vo ich (va vong lap resize)
        self._last = (id(self.image), target)
        pm = QPixmap.fromImage(self.image)
        if target != iw:
            pm = pm.scaledToWidth(target, Qt.SmoothTransformation)
        self.label.setText("")
        self.label.setPixmap(pm)
        self.label.resize(pm.size())

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if self.mode == "fit":
            self._render()


class DownloadWorker(QThread):
    """Tai mo hinh lan dau (khoang 300 MB)."""

    progress = Signal(int, int, str)  # MB da tai, tong MB, ten file
    done = Signal()
    failed = Signal(str)

    def __init__(self):
        super().__init__()
        self._cancel = False

    def cancel(self):
        self._cancel = True

    def run(self):
        try:
            tai_mo_hinh.tai_tat_ca(
                MODELS_DIR,
                tien_do=lambda got, total, name: self.progress.emit(got >> 20, total >> 20, name),
                huy=lambda: self._cancel)
            self.done.emit()
        except tai_mo_hinh.DaHuy:
            self.failed.emit("")
        except Exception as e:  # noqa: BLE001
            self.failed.emit(str(e))


class EditWorker(QThread):
    """Chay mot viec nen (xu ly vung khoanh, hoan tac) roi bao ket qua."""

    done = Signal(object)
    failed = Signal(str)

    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def run(self):
        try:
            self.done.emit(self.fn())
        except Exception as e:  # noqa: BLE001
            self.failed.emit(str(e))


class Worker(QThread):
    status = Signal(str)
    started_file = Signal(int)
    progress = Signal(int, int, int)  # chi so file, so doan xong, tong so doan
    file_done = Signal(int, dict)
    file_failed = Signal(int, str)

    def __init__(self, jobs, out_dir, params):
        super().__init__()
        self.jobs = jobs  # [(chi so, duong dan)]
        self.out_dir = Path(out_dir)
        self.params = params
        self._cancel = False

    def cancel(self):
        self._cancel = True

    def run(self):
        try:
            self.status.emit("Đang nạp mô hình (lần đầu hơi lâu)...")
            sess, lama = m0_clean.load_models(MODEL_DET, MODEL_LAMA)
        except Exception as e:  # noqa: BLE001
            for idx, _ in self.jobs:
                self.file_failed.emit(idx, f"Không nạp được mô hình: {e}")
            return
        for idx, path in self.jobs:
            if self._cancel:
                break
            self.started_file.emit(idx)
            try:
                res = m0_clean.process(
                    path, self.out_dir, sess, lama, self.params,
                    progress=lambda d, t, i=idx: self.progress.emit(i, d, t),
                    cancel=lambda: self._cancel,
                )
                self.file_done.emit(idx, res)
            except m0_clean.Cancelled:
                self.file_failed.emit(idx, "Đã dừng")
                break
            except Exception as e:  # noqa: BLE001
                self.file_failed.emit(idx, str(e))


class MainWindow(QMainWindow):
    def __init__(self, out_dir=None):
        super().__init__()
        self.setWindowTitle(f"Xóa chữ truyện tranh {__version__}")
        if (ASSETS_DIR / "icon.ico").exists():
            self.setWindowIcon(QIcon(str(ASSETS_DIR / "icon.ico")))
        self.dl_worker = None
        self.resize(1280, 800)
        self.setAcceptDrops(True)
        self.out_dir = Path(out_dir) if out_dir else OUTPUTS_DIR
        self.files = []      # duong dan anh goc
        self.results = {}    # chi so -> duong dan anh da xoa
        self.worker = None
        self._t0 = 0.0
        self._syncing = False
        self.edit_arr = None   # anh ket qua dang sua (numpy), cua dong edit_row
        self.edit_row = -1
        self.undo = {}         # chi so -> danh sach (x0, y0, mang_cu)
        self.edit_worker = None

        # ----- thanh cong cu
        tb = QToolBar()
        tb.setMovable(False)
        self.addToolBar(tb)
        for text, slot, tip in (
                ("Mở ảnh…", self.open_images, ""), ("Mở thư mục…", self.open_folder, ""),
                ("Thư mục lưu…", self.choose_out, "Chọn nơi kết quả được tự động lưu"),
                ("Lưu bản sao…", self.save_copy, "Lưu thêm một bản sao ảnh kết quả đang xem vào chỗ em chọn"),
                ("Mở nơi lưu", self.open_out_dir, "Mở thư mục chứa các ảnh kết quả (_clean.png)")):
            act = QAction(text, self)
            act.setToolTip(tip)
            act.triggered.connect(slot)
            tb.addAction(act)
        tb.addSeparator()
        self.btn_run = QPushButton("Xóa chữ")
        self.btn_run.setObjectName("primary")
        self.btn_run.clicked.connect(self.run_all)
        self.btn_stop = QPushButton("Dừng")
        self.btn_stop.setObjectName("stop")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop)
        tb.addWidget(self.btn_run)
        tb.addWidget(self.btn_stop)
        tb.addSeparator()
        tb.addWidget(QLabel(" Thu phóng: "))
        self.zoom = QComboBox()
        for label, mode in (("Vừa chiều rộng", "fit"), ("100%", 1.0), ("50%", 0.5), ("25%", 0.25)):
            self.zoom.addItem(label, mode)
        self.zoom.currentIndexChanged.connect(self.on_zoom)
        tb.addWidget(self.zoom)
        tb.addSeparator()
        self.act_sel = QAction("Khoanh vùng", self)
        self.act_sel.setCheckable(True)
        self.act_sel.setToolTip("Bật rồi kéo chuột trên ảnh kết quả (bên phải) để khoanh chỗ còn sót chữ")
        self.act_sel.toggled.connect(self.on_sel_toggled)
        tb.addAction(self.act_sel)
        self.lbl_sel = QLabel("")
        self.lbl_sel.setStyleSheet("color: white; background: #e03131; font-weight: bold; border-radius: 3px;")
        tb.addWidget(self.lbl_sel)
        self.cb_shape = QComboBox()
        self.cb_shape.addItem("Chữ nhật", "rect")
        self.cb_shape.addItem("Vẽ tự do", "free")
        self.cb_shape.currentIndexChanged.connect(self.on_sel_toggled)
        tb.addWidget(self.cb_shape)
        self.cb_mode = QComboBox()
        self.cb_mode.addItem("Tự tìm chữ trong vùng", "auto")
        self.cb_mode.addItem("Xóa hết vùng khoanh", "all")
        self.cb_mode.addItem("Khôi phục bản gốc trong vùng", "restore")
        self.cb_mode.setToolTip("'Xóa hết vùng khoanh': cho SFX máy không nhận ra, khoanh sát chữ.\n"
                                "'Khôi phục bản gốc': trả vùng khoanh về như ảnh gốc (giữ lại số chương, hình bị xóa nhầm).")
        tb.addWidget(self.cb_mode)
        self.act_undo = QAction("Hoàn tác", self)
        self.act_undo.setShortcut(QKeySequence.Undo)
        self.act_undo.triggered.connect(self.undo_edit)
        tb.addAction(self.act_undo)

        # ----- danh sach file (ben trai)
        self.listw = QListWidget()
        self.listw.currentRowChanged.connect(self.show_row)
        self.listw.setSelectionMode(QListWidget.ExtendedSelection)
        left = QWidget()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 0, 0)
        ll.addWidget(self.listw, 1)
        row_btn = QHBoxLayout()
        b1 = QPushButton("Gỡ ảnh đã chọn")
        b1.setToolTip("Chỉ gỡ khỏi danh sách cho gọn (phím Delete). Không xóa file nào trên máy.")
        b1.clicked.connect(self.remove_selected)
        b2 = QPushButton("Gỡ ảnh đã xong")
        b2.setToolTip("Gỡ khỏi danh sách các ảnh đã xử lý xong. Ảnh kết quả vẫn nằm trong thư mục lưu.")
        b2.clicked.connect(self.remove_done)
        row_btn.addWidget(b1)
        row_btn.addWidget(b2)
        ll.addLayout(row_btn)
        QShortcut(QKeySequence.Delete, self.listw, activated=self.remove_selected)
        dock = QDockWidget("Danh sách ảnh", self)
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        dock.setWidget(left)
        dock.setMinimumWidth(240)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        # ----- cai dat nang cao (ben phai)
        adv = QWidget()
        form = QFormLayout(adv)
        self.sp_scale = QDoubleSpinBox(); self.sp_scale.setRange(0.4, 1.0); self.sp_scale.setSingleStep(0.05); self.sp_scale.setValue(0.75)
        self.sp_dilate = QSpinBox(); self.sp_dilate.setRange(3, 31); self.sp_dilate.setSingleStep(2); self.sp_dilate.setValue(11)
        self.sp_thresh = QDoubleSpinBox(); self.sp_thresh.setRange(0.1, 0.9); self.sp_thresh.setSingleStep(0.05); self.sp_thresh.setValue(0.3)
        form.addRow("Độ phân giải nhận diện", self.sp_scale)
        form.addRow("Nới vùng chữ (px)", self.sp_dilate)
        form.addRow("Ngưỡng nhận diện", self.sp_thresh)
        tip = QLabel("Nhận diện nhỏ hơn thì nhanh hơn nhưng dễ sót chữ nhỏ. Nới vùng chữ lớn hơn thì ít vệt chữ mờ hơn.")
        tip.setWordWrap(True)
        tip.setObjectName("hint")
        form.addRow(tip)
        dock2 = QDockWidget("Nâng cao", self)
        dock2.setFeatures(QDockWidget.NoDockWidgetFeatures)
        dock2.setWidget(adv)
        dock2.setMinimumWidth(230)
        self.addDockWidget(Qt.RightDockWidgetArea, dock2)

        # ----- khu xem truoc/sau
        self.view_a = ImageView("Ảnh gốc")
        self.view_b = ImageView("Kết quả")
        self.view_a.set_empty("Mở ảnh hoặc kéo thả ảnh vào cửa sổ")
        self.view_b.set_empty("Kết quả hiện ở đây sau khi bấm Xóa chữ")
        for va, vb in ((self.view_a, self.view_b), (self.view_b, self.view_a)):
            va.verticalScrollBar().valueChanged.connect(lambda v, o=vb: self._sync(o, v))
        self.view_b.lasso.connect(lambda pts: self.on_lasso(pts, self.view_b))
        self.view_a.lasso.connect(lambda pts: self.on_lasso(pts, self.view_a))  # khoanh ben ảnh gốc cũng được
        split = QSplitter()
        for title, v in (("Ảnh gốc", self.view_a), ("Đã xóa chữ", self.view_b)):
            box = QWidget()
            lay = QVBoxLayout(box)
            lay.setContentsMargins(4, 4, 4, 4)
            lay.addWidget(QLabel(f"<b>{title}</b>"))
            lay.addWidget(v)
            split.addWidget(box)
        # ----- thanh duoi: tien do
        self.bar = QProgressBar()
        self.bar.setRange(0, 1)
        self.bar.setValue(0)
        self.lbl = QLabel("Sẵn sàng.")
        bottom = QWidget()
        bl = QHBoxLayout(bottom)
        bl.setContentsMargins(6, 2, 6, 6)
        bl.addWidget(self.lbl, 3)
        bl.addWidget(self.bar, 2)
        central = QWidget()
        cl = QVBoxLayout(central)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.addWidget(split, 1)
        cl.addWidget(bottom)
        self.setCentralWidget(central)
        self.statusBar().showMessage(f"Lưu kết quả vào: {self.out_dir}")

    # ---------------- thao tac file
    def _start_dir(self):
        """Thu muc mo san trong hop thoai chon anh."""
        if not FROZEN and (MODELS_DIR.parent / "samples").exists():
            return str(MODELS_DIR.parent / "samples")
        return str(Path.home() / "Pictures")

    # ---------------- mo hinh
    def models_ready(self):
        return tai_mo_hinh.da_du(MODELS_DIR)

    def ensure_models(self, then=None):
        """Neu chua co mo hinh: hoi roi tai (co thanh tien do). Xong thi goi then(). Tra ve True neu da san sang."""
        if self.models_ready():
            return True
        if self.dl_worker and self.dl_worker.isRunning():
            self.dl_dialog.show()
            return False
        ans = QMessageBox.question(
            self, "Tải mô hình lần đầu",
            f"Lần đầu dùng, app cần tải mô hình AI (khoảng {tai_mo_hinh.TONG_BYTE >> 20} MB, chỉ tải một lần).\n"
            "Cần có mạng. Tải ngay bây giờ?\n\n"
            "Lưu ý: chỉ dùng app cho truyện tự vẽ hoặc truyện em có quyền chỉnh sửa.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if ans != QMessageBox.Yes:
            self.lbl.setText("Chưa có mô hình. Bấm \"Xóa chữ\" khi muốn tải.")
            return False
        self.dl_dialog = QProgressDialog("Đang chuẩn bị tải…", "Hủy", 0, 100, self)
        self.dl_dialog.setWindowTitle("Đang tải mô hình")
        self.dl_dialog.setWindowModality(Qt.WindowModal)
        self.dl_dialog.setMinimumDuration(0)
        self.dl_dialog.setAutoClose(False)
        self.dl_dialog.setAutoReset(False)
        self.dl_dialog.setMinimumWidth(420)
        self.dl_worker = DownloadWorker()
        self.dl_dialog.canceled.connect(self.dl_worker.cancel)

        def on_progress(got, total, name):
            self.dl_dialog.setMaximum(max(total, 1))
            self.dl_dialog.setValue(min(got, total))
            if got >= total:
                self.dl_dialog.setLabelText("Đang chuẩn bị mô hình… (vài giây)")
            else:
                self.dl_dialog.setLabelText(f"Đang tải {name}: {got} / {total} MB")

        def on_done():
            self.dl_dialog.close()
            self.lbl.setText("Đã có mô hình. Sẵn sàng xóa chữ.")
            if then:
                then()

        def on_failed(msg):
            self.dl_dialog.close()
            if msg:
                QMessageBox.warning(self, "Tải không được",
                                    f"Chưa tải được mô hình:\n{msg}\n\nKiểm tra mạng rồi bấm \"Xóa chữ\" để thử lại.")
            self.lbl.setText("Chưa có mô hình. Bấm \"Xóa chữ\" để tải lại.")

        self.dl_worker.progress.connect(on_progress)
        self.dl_worker.done.connect(on_done)
        self.dl_worker.failed.connect(on_failed)
        self.dl_dialog.show()
        self.dl_worker.start()
        return False

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        paths = []
        for u in e.mimeData().urls():
            p = Path(u.toLocalFile())
            if p.is_dir():
                paths += sorted((q for q in p.iterdir() if q.suffix.lower() in EXTS), key=natural_key)
            elif p.suffix.lower() in EXTS:
                paths.append(p)
        self.add_files(paths)

    def open_images(self):
        names, _ = QFileDialog.getOpenFileNames(self, "Chọn ảnh", self._start_dir(),
                                                "Ảnh (*.png *.jpg *.jpeg *.webp *.bmp)")
        self.add_files([Path(n) for n in names])

    def open_folder(self):
        d = QFileDialog.getExistingDirectory(self, "Chọn thư mục ảnh", self._start_dir())
        if d:
            self.add_files(sorted((q for q in Path(d).iterdir() if q.suffix.lower() in EXTS), key=natural_key))

    def choose_out(self):
        d = QFileDialog.getExistingDirectory(self, "Chọn thư mục lưu kết quả", str(self.out_dir))
        if d:
            self.out_dir = Path(d)
            self.statusBar().showMessage(f"Lưu kết quả vào: {self.out_dir}")

    def open_out_dir(self):
        self.out_dir.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.out_dir)))

    def save_copy(self):
        row = self.listw.currentRow()
        res = self.results.get(row)
        if res is None or not Path(res).exists():
            self._warn("Ảnh này chưa có kết quả để lưu. Bấm Xóa chữ trước.")
            return
        dst, _ = QFileDialog.getSaveFileName(self, "Lưu bản sao kết quả", str(Path(res).name),
                                             "PNG (*.png);;JPEG (*.jpg)")
        if not dst:
            return
        try:
            Image.open(res).convert("RGB").save(dst)
        except Exception as e:  # noqa: BLE001
            self._warn(f"Không lưu được: {e}")
            return
        self.lbl.setText(f"Đã lưu bản sao: {dst}")

    def _remove_rows(self, rows):
        if self._busy():
            self._warn("Đang xử lý, đợi xong rồi hãy gỡ ảnh khỏi danh sách.")
            return
        rows = sorted(set(rows), reverse=True)
        if not rows:
            return
        keep = [i for i in range(len(self.files)) if i not in rows]
        remap = {old: new for new, old in enumerate(keep)}
        self.files = [self.files[i] for i in keep]
        self.results = {remap[i]: p for i, p in self.results.items() if i in remap}
        self.undo = {remap[i]: v for i, v in self.undo.items() if i in remap}
        self.edit_arr, self.edit_row = None, -1
        self.listw.blockSignals(True)
        for r in rows:
            self.listw.takeItem(r)
        self.listw.blockSignals(False)
        if self.files:
            self.listw.setCurrentRow(min(rows[-1], len(self.files) - 1))
            self.show_row(self.listw.currentRow())
        else:
            self.view_a.set_empty("Mở ảnh hoặc kéo thả ảnh vào cửa sổ")
            self.view_b.set_empty("Kết quả hiện ở đây sau khi bấm Xóa chữ")
        self.lbl.setText(f"Đã gỡ khỏi danh sách (không xóa file). Còn {len(self.files)} ảnh.")

    def remove_selected(self):
        self._remove_rows([self.listw.row(i) for i in self.listw.selectedItems()])

    def remove_done(self):
        self._remove_rows(list(self.results.keys()))

    def add_files(self, paths):
        known = set(self.files)
        added = 0
        for p in paths:
            if p in known or p.stem.endswith("_clean"):
                continue
            self.files.append(p)
            self.listw.addItem(QListWidgetItem(f"{p.name}  —  Chờ"))
            added += 1
        if added and self.listw.currentRow() < 0:
            self.listw.setCurrentRow(0)
        self.lbl.setText(f"{len(self.files)} ảnh trong danh sách.")

    def set_item(self, idx, text):
        self.listw.item(idx).setText(f"{self.files[idx].name}  —  {text}")

    # ---------------- xem truoc
    def show_row(self, row):
        if not (0 <= row < len(self.files)):
            return
        img = read_image(self.files[row])
        if img.isNull():
            self.view_a.set_empty("Không đọc được ảnh này")
        else:
            self.view_a.set_image(img)
        res = self.results.get(row)
        if res and Path(res).exists():
            self.view_b.set_image(read_image(res))
        else:
            self.view_b.set_empty("Chưa xử lý ảnh này")

    def on_zoom(self):
        mode = self.zoom.currentData()
        self.view_a.set_mode(mode)
        self.view_b.set_mode(mode)

    # ---------------- khoanh vung
    def on_sel_toggled(self, *_):
        on = self.act_sel.isChecked()
        for v in (self.view_a, self.view_b):
            v.label.shape = self.cb_shape.currentData()
            v.label.set_active(on)
        self.lbl_sel.setText("  ● ĐANG BẬT KHOANH: kéo chuột trên ảnh để khoanh  " if on else "")
        self.statusBar().showMessage(
            "Kéo chuột trên ảnh để khoanh vùng." if on else f"Lưu kết quả vào: {self.out_dir}")

    def _warn(self, text):
        """Báo lỗi nổi bật (hộp thoại) để không bị lỡ khi cửa sổ bị cắt mất thanh dưới."""
        self.lbl.setText(text)
        QMessageBox.information(self, "Khoanh vùng", text)

    def _busy(self):
        return bool((self.worker and self.worker.isRunning()) or
                    (self.edit_worker and self.edit_worker.isRunning()))

    def _set_edit_busy(self, busy):
        for w in (self.act_sel, self.act_undo, self.btn_run):
            w.setEnabled(not busy)
        self.lbl.setText("Đang xử lý vùng khoanh…" if busy else self.lbl.text())

    def _load_arr(self, row):
        path = self.results[row]
        if self.edit_row != row or self.edit_arr is None:
            self.edit_arr = np.array(Image.open(path).convert("RGB"))
            self.edit_row = row
        return path, self.edit_arr

    def _show_arr(self, arr):
        h, w = arr.shape[:2]
        img = QImage(arr.data, w, h, 3 * w, QImage.Format_RGB888).copy()
        self.view_b.set_image(img)

    def on_lasso(self, pts, view=None):
        view = view or self.view_b
        row = self.listw.currentRow()
        if self._busy():
            self._warn("Đang bận, đợi xong rồi khoanh tiếp.")
            return
        if row not in self.results or self.view_b.image is None:
            self._warn("Hãy bấm Xóa chữ cho ảnh này trước, rồi mới khoanh vùng.")
            return
        if self.cb_mode.currentData() != "restore" and not self.ensure_models():
            return
        pm = view.label.pixmap()
        if pm is None or pm.isNull() or view.image is None:
            self._warn("Chưa có ảnh để khoanh.")
            return
        scale = pm.width() / view.image.width()
        poly = [(x / scale, y / scale) for x, y in pts]
        mode = self.cb_mode.currentData()
        params = self.params()

        def job_clean():
            path, arr = self._load_arr(row)
            sess, lama = m0_clean.load_models(MODEL_DET, MODEL_LAMA)
            r = m0_clean.clean_region(arr, poly, mode, sess, lama, dilate=params.dilate)
            if r is None:
                return None
            hh, ww = r["new"].shape[:2]
            arr[r["y0"]:r["y0"] + hh, r["x0"]:r["x0"] + ww] = r["new"]
            Image.fromarray(arr).save(path)
            return {"row": row, **r}

        def job_restore():
            """Tra vung khoanh ve dung nhu anh goc (khong dung mo hinh)."""
            path, arr = self._load_arr(row)
            H, W = arr.shape[:2]
            x0, y0 = max(0, int(min(p[0] for p in poly))), max(0, int(min(p[1] for p in poly)))
            x1, y1 = min(W, int(max(p[0] for p in poly)) + 1), min(H, int(max(p[1] for p in poly)) + 1)
            if x1 - x0 < 2 or y1 - y0 < 2:
                return None
            orig = np.array(Image.open(self.files[row]).convert("RGB").crop((x0, y0, x1, y1)))
            if orig.shape[:2] != (y1 - y0, x1 - x0):
                raise ValueError("Ảnh gốc khác kích thước ảnh kết quả")
            pm = np.zeros((y1 - y0, x1 - x0), np.uint8)
            m0_clean.cv2.fillPoly(pm, [np.array([[p[0] - x0, p[1] - y0] for p in poly], np.int32)], 1)
            old = arr[y0:y1, x0:x1].copy()
            new = old.copy()
            new[pm > 0] = orig[pm > 0]
            arr[y0:y1, x0:x1] = new
            Image.fromarray(arr).save(path)
            return {"row": row, "x0": x0, "y0": y0, "old": old, "new": new, "kind": "restore",
                    "stats": {"flat": 0, "lama": 0, "lama_scaled": 0}}

        self._start_edit(job_restore if mode == "restore" else job_clean, self._on_region_done)

    def _start_edit(self, job, on_done):
        self._set_edit_busy(True)
        self.edit_worker = EditWorker(job)
        self.edit_worker.done.connect(on_done)
        self.edit_worker.failed.connect(self._on_edit_failed)
        self.edit_worker.finished.connect(lambda: self._set_edit_busy(False))
        self.edit_worker.start()

    def _on_edit_failed(self, msg):
        self._warn(f"Lỗi khi xử lý vùng khoanh: {msg[:200]}")

    def _on_region_done(self, r):
        if r is None:
            self.lbl.setText("Không có gì để đổi trong vùng khoanh. Với chế độ 'Tự tìm chữ', thử 'Xóa hết vùng khoanh' "
                             "(khoanh sát quanh chữ).")
            return
        stack = self.undo.setdefault(r["row"], [])
        stack.append((r["x0"], r["y0"], r["old"]))
        del stack[:-15]  # giu toi da 15 buoc hoan tac
        if self.listw.currentRow() == r["row"]:
            self._show_arr(self.edit_arr)
        st = r["stats"]
        if r.get("kind") == "restore":
            self.lbl.setText("Đã khôi phục bản gốc trong vùng khoanh. Ctrl+Z để hoàn tác.")
            return
        self.lbl.setText(f"Đã xử lý vùng khoanh ({st['flat'] + st['lama'] + st['lama_scaled']} chỗ). Ctrl+Z để hoàn tác.")

    def undo_edit(self):
        row = self.listw.currentRow()
        stack = self.undo.get(row)
        if self._busy() or not stack:
            self.lbl.setText("Không có gì để hoàn tác.")
            return
        x0, y0, old = stack.pop()

        def job():
            path, arr = self._load_arr(row)
            hh, ww = old.shape[:2]
            arr[y0:y0 + hh, x0:x0 + ww] = old
            Image.fromarray(arr).save(path)
            return {"row": row}

        def done(r):
            if self.listw.currentRow() == r["row"]:
                self._show_arr(self.edit_arr)
            self.lbl.setText("Đã hoàn tác một bước.")

        self._start_edit(job, done)

    def _sync(self, other, value):
        if self._syncing:
            return
        self._syncing = True
        other.verticalScrollBar().setValue(value)
        self._syncing = False

    # ---------------- chay
    def params(self):
        return Namespace(thresh=self.sp_thresh.value(), det_scale=self.sp_scale.value(),
                         dilate=self.sp_dilate.value(), max_tile=1000, flat_std=8.0, save_mask=False)

    def run_all(self):
        if not self.files:
            QMessageBox.information(self, "Chưa có ảnh", "Hãy mở ảnh hoặc kéo thả ảnh vào cửa sổ trước.")
            return
        if not self.ensure_models(then=self.run_all):
            return
        jobs = [(i, p) for i, p in enumerate(self.files) if i not in self.results]
        if not jobs:
            self.lbl.setText("Tất cả ảnh đã xử lý.")
            return
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self._total_jobs, self._done_jobs, self._t0 = len(jobs), 0, time.time()
        for i, _ in jobs:
            self.set_item(i, "Chờ")
        self.worker = Worker(jobs, self.out_dir, self.params())
        self.worker.status.connect(self.lbl.setText)
        self.worker.started_file.connect(self.on_started)
        self.worker.progress.connect(self.on_progress)
        self.worker.file_done.connect(self.on_done)
        self.worker.file_failed.connect(self.on_failed)
        self.worker.finished.connect(self.on_finished)
        self.btn_run.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.worker.start()

    def stop(self):
        if self.worker:
            self.worker.cancel()
            self.lbl.setText("Đang dừng… (xong đoạn hiện tại sẽ dừng)")

    def on_started(self, idx):
        self.set_item(idx, "Đang xử lý…")
        self.bar.setRange(0, 1)
        self.bar.setValue(0)
        self.lbl.setText(f"Đang xử lý {self.files[idx].name} (ảnh {self._done_jobs + 1}/{self._total_jobs})")

    def on_progress(self, idx, done, total):
        self.bar.setRange(0, total)
        self.bar.setValue(done)
        self.set_item(idx, f"Đang xử lý {done}/{total} đoạn")

    def on_done(self, idx, res):
        self._done_jobs += 1
        self.results[idx] = self.out_dir / res["output"]
        self.undo.pop(idx, None)
        if idx == self.edit_row:
            self.edit_arr = None  # ket qua moi ghi de file, bo ban sua cu
        self.set_item(idx, f"Xong ({res['sec_total']:.0f} s)")
        self.listw.item(idx).setToolTip(f"Đã lưu: {self.results[idx]}")
        if self.listw.currentRow() == idx:
            self.show_row(idx)

    def on_failed(self, idx, msg):
        self._done_jobs += 1
        self.set_item(idx, f"Lỗi: {msg[:60]}")

    def on_finished(self):
        self.btn_run.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.bar.setRange(0, 1)
        self.bar.setValue(1 if len(self.results) == len(self.files) else 0)
        self.lbl.setText(f"Xong. Đã xử lý {len(self.results)}/{len(self.files)} ảnh trong {time.time() - self._t0:.0f} giây. "
                         f"Đã tự lưu ở: {self.out_dir}  (bấm 'Mở nơi lưu' để xem)")

    def closeEvent(self, e):
        if self.dl_worker and self.dl_worker.isRunning():
            self.dl_worker.cancel()
            self.dl_worker.wait(10000)
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.worker.wait(30000)
        super().closeEvent(e)


def ghi_loi(exc_type, exc, tb):
    """Loi khong luong truoc: ghi vao nhat-ky-loi.txt va bao bang hop thoai (ban dong goi khong co cua so den)."""
    text = "".join(traceback.format_exception(exc_type, exc, tb))
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n===== {time.strftime('%Y-%m-%d %H:%M:%S')}  phiên bản {__version__}\n{text}")
    except OSError:
        pass
    sys.__excepthook__(exc_type, exc, tb)
    if QApplication.instance():
        QMessageBox.critical(None, "Có lỗi",
                             f"App gặp lỗi:\n{exc}\n\nChi tiết đã ghi vào:\n{LOG_FILE}\n"
                             "Gửi file này kèm ảnh chụp màn hình cho người làm app nhé.")


def tu_kiem_tra():
    """Dung khi dong goi (GitHub): kiem tra ban dong goi nap du thu vien va mo duoc cua so. Ma thoat 0 = dat."""
    import onnx
    import onnxruntime as ort
    import torch
    from onnx import TensorProto, helper

    g = helper.make_graph([helper.make_node("Relu", ["x"], ["y"])], "t",
                          [helper.make_tensor_value_info("x", TensorProto.FLOAT, [1, 3])],
                          [helper.make_tensor_value_info("y", TensorProto.FLOAT, [1, 3])])
    m = helper.make_model(g, opset_imports=[helper.make_opsetid("", 13)])
    m.ir_version = 8
    out = ort.InferenceSession(m.SerializeToString(), providers=["CPUExecutionProvider"]).run(
        None, {"x": np.array([[-1, 0, 2]], np.float32)})[0]
    assert out.tolist() == [[0, 0, 2]], out
    assert float(torch.nn.functional.relu(torch.tensor([-1.0, 2.0])).sum()) == 2.0
    import cv2
    assert cv2.dilate(np.ones((5, 5), np.uint8), None).shape == (5, 5)
    if "--day-du" in sys.argv:
        # Tai mo hinh that va xoa chu tren mot trang gia (kiem tra torch/onnx trong ban dong goi).
        tai_mo_hinh.tai_tat_ca(MODELS_DIR)
        sess, lama = m0_clean.load_models(MODEL_DET, MODEL_LAMA)
        img = np.full((1500, 600, 3), 255, np.uint8)
        cv2.ellipse(img, (300, 400), (220, 140), 0, 0, 360, (0, 0, 0), 3)
        cv2.putText(img, "HELLO THERE", (150, 400), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 0), 3)
        yy, xx = np.mgrid[800:1500, 0:600]
        img[800:] = (128 + 60 * np.sin(xx / 7.0) * np.cos(yy / 9.0))[..., None].astype(np.uint8)  # nen hoa van -> LaMa
        cv2.putText(img, "BOOM", (180, 1200), cv2.FONT_HERSHEY_TRIPLEX, 3, (255, 255, 255), 6)
        tmp = LOG_FILE.parent / "tu-kiem-tra"
        tmp.mkdir(parents=True, exist_ok=True)
        Image.fromarray(img).save(tmp / "trang.png")
        args = Namespace(thresh=0.3, det_scale=0.75, dilate=11, max_tile=1000, flat_std=8.0, save_mask=False)
        r = m0_clean.process(tmp / "trang.png", tmp, sess, lama, args)
        out = np.array(Image.open(tmp / r["output"]))
        chu_con_lai = int((out[350:420, 140:470] < 128).sum())
        print("XU LY", r, "diem den con lai trong bong bong:", chu_con_lai)
        assert r["boxes"]["flat"] >= 1 and r["boxes"]["lama"] + r["boxes"]["lama_scaled"] >= 1, r
        assert chu_con_lai < 200, chu_con_lai
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    QTimer.singleShot(500, app.quit)
    app.exec()
    print("TU KIEM TRA DAT", __version__)


def main():
    if "--tu-kiem-tra" in sys.argv:
        try:
            tu_kiem_tra()
        except Exception:  # noqa: BLE001
            traceback.print_exc()
            LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
            LOG_FILE.write_text("TU KIEM TRA LOI\n" + traceback.format_exc(), encoding="utf-8")
            sys.exit(1)
        sys.exit(0)
    sys.excepthook = ghi_loi
    app = QApplication(sys.argv)
    app.setApplicationName("XoaChuTruyenTranh")
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE)
    w = MainWindow()
    w.show()
    if not w.models_ready():
        QTimer.singleShot(300, w.ensure_models)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
