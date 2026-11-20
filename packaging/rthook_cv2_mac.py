# Runtime hook PyInstaller (chay truoc app.py trong ban dong goi).
# Ban Mac (.app do PyInstaller BUNDLE xep): goi cv2 bi tach data/binary giua Contents/Resources va
# Contents/Frameworks, bootstrap cua cv2/__init__.py nap lai chinh no -> "recursion is detected" (2026-11-20).
# Cach sua: nap thang phan loi C++ (cv2.abi3.so) lam module 'cv2', bo qua bootstrap. App chi dung cac ham loi
# (dilate, resize, connectedComponentsWithStats, fillPoly, ...), co du trong phan loi.
# Bien moi truong XOA_CV2_NAP_THANG=1 bat cach nap nay tren he dieu hanh khac (de thu tren Linux/Windows).
import glob
import os
import sys

if getattr(sys, "frozen", False) and (sys.platform == "darwin" or os.environ.get("XOA_CV2_NAP_THANG")):
    import importlib.machinery
    import importlib.util

    _found = sorted(glob.glob(os.path.join(sys._MEIPASS, "cv2", "cv2*.so")) +
                    glob.glob(os.path.join(sys._MEIPASS, "cv2", "cv2*.pyd")))
    if _found:
        _so = os.path.realpath(_found[0])
        _loader = importlib.machinery.ExtensionFileLoader("cv2", _so)
        _spec = importlib.util.spec_from_file_location("cv2", _so, loader=_loader)
        _mod = importlib.util.module_from_spec(_spec)
        sys.modules["cv2"] = _mod
        _loader.exec_module(_mod)
