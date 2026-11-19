# HANDOVER

## Tóm tắt (cho em Minh Anh)
Dự án đã lên GitHub (repo công khai) và GitHub tự đóng gói app thành `XoaChuTruyenTranh-windows.zip`, giống cách Chụp Nét đang làm. App giờ tự tải mô hình lần đầu mở, nên các bạn chỉ cần giải nén rồi bấm đúp exe. Lần đóng gói đầu trên Windows đã xanh: zip 261 MB, giải nén 752 MB (mô hình 286 MB tải riêng lần đầu). Em đã phát hành `v0.1.0` (2026-11-19) và thử bản zip trên máy em: em báo chạy ổn. Cần em: (1) gửi cho một bạn trước làm bản thử, ổn rồi mới gửi cả nhóm (link `releases/latest`); (2) bấm đúp `Noi Git.bat` một lần để nối thư mục trên máy với GitHub.

## Cập nhật
- 2026-11-19. Bản 0.1.0 đã phát hành (release `v0.1.0`, commit `a0962fb`, zip 261 MB). Em thử zip trên máy em (máy đã cài Python): chạy ổn; chưa thử trên máy sạch. Git: https://github.com/anhtm01042009-del/xoa-SFX-truyen-tranh (public), nhánh `main`. Thư mục trên máy em **chưa có `.git`**: agent đẩy code từ bản clone ở container rồi chép file sửa về máy em bằng `device_commit_files`.
- GitHub Actions (windows-latest) lần đầu: xanh, gồm tự kiểm tra đầy đủ của bản đóng gói. Trên máy Claude (Linux): `packaging/kiem_tra_nap.py` đạt; app chạy từ mã nguồn tự tải mô hình rồi xóa chữ ảnh giả đạt; bản PyInstaller `--tu-kiem-tra --day-du` đạt (tải mô hình, tạo ctd_seg trong bản đóng gói, nhánh tô màu + LaMa đều chạy).

## Đã làm phiên này
- `src/duong_dan.py`: chạy từ mã nguồn giữ `models\`, `outputs\` như cũ; bản đóng gói dùng `%LOCALAPPDATA%\XoaChuTruyenTranh\models` và `Pictures\XoaChuTruyenTranh`.
- `src/tai_mo_hinh.py`: hàm `tai_tat_ca` (file `.part`, kiểm đúng kích thước, hủy được), `da_du`; `make_seg_model.tao_seg` gọi trực tiếp (không mở tiến trình mới, vì trong bản đóng gói `sys.executable` là app).
- `src/app.py`: hộp thoại tải mô hình lần đầu (có lời nhắc bản quyền), số phiên bản ở tiêu đề, biểu tượng, ghi lỗi vào `nhat-ky-loi.txt`, chế độ `--tu-kiem-tra [--day-du]` cho GitHub.
- Đóng gói: `packaging/XoaChuTruyenTranh.spec` (onedir), `.github/workflows/dong-goi.yml` (windows-latest, torch CPU, chạy tự kiểm tra đầy đủ, nén 7z, đính kèm khi có tag `v*`).
- Khung chia sẻ: `LICENSE` (GPL-3.0), `THIRD-PARTY.md`, `HUONG-DAN.md`, `packaging/DOC-TRUOC.txt`, `Noi Git.bat`, `Day len GitHub.bat`, `.gitignore` chặn ảnh truyện và mô hình, `.gitattributes`.

## Đang làm dở
- Bản đóng gói chưa được mở bằng tay trên Windows thật có màn hình (Actions chỉ chạy tự kiểm tra không cửa sổ).
- Ảnh tiếng Trung vẫn chưa chạy trên máy em (việc cũ).

## Việc kế tiếp (tối đa 3)
1. Nếu Actions đỏ ở lần sau, đọc log bước "Chay thu ban dong goi" (in nội dung `nhat-ky-loi.txt`).
2. Ghi phản hồi của bạn đầu tiên (máy sạch): cài được không, thời gian chạy, lỗi (nếu có) vào `validation\`.
3. Theo phản hồi của các bạn; cân nhắc bỏ torch (LaMa ONNX) nếu zip quá nặng.

## Đang chờ em quyết
- Có dùng Notion cho dự án này không (chưa có trang).
- `outputs\Thư mục mới\` (bản sao ảnh cũ) — em tự quyết xóa/giữ.

## Lưu ý và bẫy
- **Phát hành:** agent không đẩy tag hay tạo release được (giống Chụp Nét): em tạo release trên web, tag `vX.Y.Z` trùng `src/phien_ban.py`, trỏ vào commit có Actions xanh.
- `device_commit_files` không ghi được vào `.github/` trên máy em; file workflow chỉ có trên GitHub cho tới khi em chạy `Noi Git.bat`.
- Nạp `m0_clean` (numpy, cv2, onnxruntime, torch) TRƯỚC PySide6, nếu không nạp chậm hàng chục lần. `ImageView`: thanh cuộn dọc luôn hiện + bỏ qua vẽ lại khi kích thước không đổi. Kiểm thử headless dùng `app.exec()`, không dùng `QTest.qWait`.
- Bản đóng gói `console=False`: `print` không hiện; lỗi tự kiểm tra ghi vào `nhat-ky-loi.txt`. Hộp thoại lỗi không được bật trong chế độ tự kiểm tra (offscreen sẽ treo).
- `ctd_seg.onnx` yêu cầu đầu vào chia hết cho 64; tạo ra phải đúng 65 568 531 byte (khớp bản trên máy em).
- Kích thước mô hình dùng để kiểm: comictextdetector 94 669 756 byte, big-lama 205 669 692 byte. Nếu nguồn tải đổi file, app sẽ báo "tải không đủ".
- Torch PyPI trên Linux kèm CUDA (gói thử trên máy Claude 5,2 GB); Windows dùng index CPU: zip 261 MB, giải nén 752 MB (run 44558433135, 2026-11-19). Actions chạy ~5 phút.
- Số "2" (số chương, Hàn) bị xóa dở khi chạy tự động: giữ bằng khoanh + Khôi phục. Khôi phục dùng ảnh gốc theo đường dẫn: gỡ/đổi tên ảnh gốc làm hỏng khôi phục.

## File cần đọc trước
`RULES.md`, `src/duong_dan.py`, `src/tai_mo_hinh.py`, `src/app.py` (`ensure_models`, `tu_kiem_tra`), `.github/workflows/dong-goi.yml`
