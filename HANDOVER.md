# HANDOVER

## Tóm tắt (cho em Minh Anh)
Bạn dùng Mac M1 đã mở được app (v0.1.1) nhưng không tải được mô hình (lỗi chứng chỉ bảo mật). Đã sửa ở **bản 0.1.2**: app mang theo bộ chứng chỉ riêng. Cần em: gửi bạn link `releases/latest` để tải lại **mac.zip** bản 0.1.2, kéo app mới vào Ứng dụng thay app cũ (có thể phải bấm Vẫn mở lần nữa); bấm đúp `Noi Git.bat` khi rảnh.

## Cập nhật
- 2026-11-20. Bản 0.1.2 (`src/phien_ban.py` = 0.1.2): thêm certifi cho bước tải mô hình. v0.1.1 đã phát hành (2 zip); bạn Mac M1 mở được app, Gatekeeper qua được, lỗi tải mô hình do chứng chỉ.
- Trước đó: bản 0.1.1 Git `main` tại commit thêm runtime hook cv2. Run Actions 44705818137: windows xanh (zip 253 MB), mac xanh (zip 263 MB, giải nén 845 MB, Signature=adhoc, tự kiểm tra đầy đủ đạt).
- v0.1.0 (2026-11-19, chỉ Windows) đã phát hành; em thử trên máy em chạy ổn. Bạn đầu tiên dùng Mac M1 → mới có bản Mac.
- Thư mục trên máy em vẫn **chưa có `.git`**: agent đẩy từ clone ở container, chép file về bằng `device_commit_files` (không ghi được `.github/`).

## Đã làm phiên này
- `src/duong_dan.py`: Mac dùng `~/Library/Application Support/XoaChuTruyenTranh`.
- `packaging/XoaChuTruyenTranh.spec`: thêm BUNDLE (.app) khi build trên Mac + runtime hook `packaging/rthook_cv2_mac.py`.
- Workflow: job `windows` + job `mac` (macos-latest), mỗi job tự đính kèm zip của mình vào release; mô tả release ở `packaging/MO-TA-BAN-PHAT-HANH.md`; Mac nén bằng `ditto` (giữ symlink trong .app).
- `packaging/requirements-dong-goi.txt`: khóa OpenCV < 5.
- Hướng dẫn Mac: `HUONG-DAN.md` mục 1b, `packaging/DOC-TRUOC-MAC.txt`, README.

## Đang làm dở
- Bản Mac chưa được mở bằng tay trên Mac thật (chờ bạn của em thử); chưa biết cách Gatekeeper trên máy bạn hiển thị (Open Anyway hay báo "damaged").
- Ảnh tiếng Trung vẫn chưa chạy trên máy em (việc cũ).

## Việc kế tiếp (tối đa 3)
1. Em tạo release `v0.1.1`; kiểm tra trang release có đủ 2 file zip.
2. Ghi phản hồi của bạn dùng Mac M1 (mở được không, bước Gatekeeper nào, thời gian chạy) vào `validation\`; nếu Gatekeeper chặn khó, cân nhắc hướng dẫn `xattr -cr` lên trước.
3. Theo phản hồi; cân nhắc bỏ torch (LaMa ONNX) nếu zip quá nặng.

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
- Mac: KHÔNG tự dựng .app và KHÔNG chép `_internal` nguyên khối vào `Contents/Frameworks` (đã thử 2026-11-20: bootloader cần Frameworks, codesign từ chối thư mục `*.dist-info`/file dữ liệu ở đó). Dùng BUNDLE + runtime hook cv2. Biến `XOA_CV2_NAP_THANG=1` bật hook trên Linux/Windows để thử.
- GitHub không còn máy `macos-14`; dùng `macos-latest`.
- Tải mô hình phải dùng `tai_mo_hinh.ssl_context()` (kho máy + certifi); Python đóng gói trên Mac không thấy chứng chỉ của macOS. Máy GitHub có sẵn chứng chỉ nên tự kiểm tra đặt `SSL_CERT_FILE`/`SSL_CERT_DIR` giả để giả lập.
- Torch PyPI trên Linux kèm CUDA (gói thử trên máy Claude 5,2 GB); Windows dùng index CPU: zip 261 MB, giải nén 752 MB (run 44558433135, 2026-11-19). Actions chạy ~5 phút.
- Số "2" (số chương, Hàn) bị xóa dở khi chạy tự động: giữ bằng khoanh + Khôi phục. Khôi phục dùng ảnh gốc theo đường dẫn: gỡ/đổi tên ảnh gốc làm hỏng khôi phục.

## File cần đọc trước
`RULES.md`, `src/duong_dan.py`, `src/tai_mo_hinh.py`, `src/app.py` (`ensure_models`, `tu_kiem_tra`), `.github/workflows/dong-goi.yml`, `packaging/XoaChuTruyenTranh.spec`, `packaging/rthook_cv2_mac.py`
