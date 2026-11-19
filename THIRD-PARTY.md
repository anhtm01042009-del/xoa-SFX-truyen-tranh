# Thành phần bên thứ ba

App này (mã nguồn trong repo) phát hành theo giấy phép **GPL-3.0** (xem `LICENSE`), vì có dùng mô hình nhận diện chữ theo GPL-3.0.

## Mô hình AI (app tự tải về lần đầu, không nằm trong repo hay file zip)
| Thành phần | Dùng để | Nguồn tải | Giấy phép |
|---|---|---|---|
| comic-text-detector (`comictextdetector.pt.onnx`) | Nhận diện vùng chữ | https://github.com/zyddnys/manga-image-translator (bản phát hành beta-0.2.1); mô hình gốc: https://github.com/dmMaze/comic-text-detector | GPL-3.0 |
| `ctd_seg.onnx` | Bản rút gọn của mô hình trên (chỉ giữ nhánh phân đoạn chữ), app tự tạo trên máy | — | GPL-3.0 (theo mô hình gốc) |
| Big LaMa (`big-lama.pt`) | Vá lại nền sau khi xóa chữ | https://github.com/Sanster/models (bản add_big_lama); gốc: https://github.com/advimman/lama | Apache-2.0 |

LaMa được huấn luyện trên bộ ảnh Places; điều khoản của bộ dữ liệu do nhóm tác giả Places quy định.

## Thư viện đóng gói kèm bản Windows
| Thư viện | Giấy phép |
|---|---|
| PySide6 (Qt for Python) | LGPL-3.0 |
| PyTorch | BSD-3-Clause |
| ONNX, ONNX Runtime | Apache-2.0 / MIT |
| OpenCV (opencv-python-headless) | Apache-2.0 (OpenCV), MIT (gói Python) |
| NumPy | BSD-3-Clause |
| Pillow | MIT-CMU (HPND) |
| psutil | BSD-3-Clause |
| PyInstaller (dùng để đóng gói) | GPL-2.0 kèm ngoại lệ cho phép phát hành app đóng gói |

Giấy phép ghi theo trang chính thức của từng dự án tại thời điểm viết (11/2026); nếu có khác biệt thì theo trang gốc.
