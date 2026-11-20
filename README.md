# Xóa thoại & SFX truyện tranh

Ứng dụng desktop (Windows và Mac chip Apple) xóa chữ thoại trong bong bóng và SFX trên trang truyện tranh (kể cả trang dài cuộn dọc), tự dựng lại nền. Giai đoạn sau: gõ chữ Việt có dấu thay vào bong bóng.

> Chỉ dùng cho truyện tự vẽ hoặc truyện bạn có quyền chỉnh sửa.

## Cho người dùng
Tải bản mới nhất ở mục **[Releases](https://github.com/anhtm01042009-del/xoa-SFX-truyen-tranh/releases)** — Windows: `XoaChuTruyenTranh-windows.zip`, giải nén, bấm đúp `XoaChuTruyenTranh.exe`; Mac chip Apple: `XoaChuTruyenTranh-mac.zip`, kéo app vào Ứng dụng (lần đầu mở phải cho phép trong Quyền riêng tư & Bảo mật). Không cần cài Python. Lần đầu mở app tự tải mô hình AI (khoảng 290 MB).

Hướng dẫn đầy đủ: [HUONG-DAN.md](HUONG-DAN.md). Bản thử nghiệm, gặp lỗi xin báo ở mục Issues.

## Cho người phát triển
- Python 3.12 + PySide6; nhận diện chữ bằng comic-text-detector (ONNX), vá nền bằng LaMa (TorchScript), chạy CPU.
- Chạy từ mã nguồn: `cai_dat.bat` (một lần), rồi `chay_app.bat`.
- Đóng gói: GitHub Actions (`.github/workflows/dong-goi.yml`) dùng PyInstaller theo `packaging/XoaChuTruyenTranh.spec`, đóng gói song song trên Windows và macOS (arm64), nén thành hai file zip. Tạo bản phát hành có tag `vX.Y.Z` thì zip được đính kèm. Số phiên bản ở `src/phien_ban.py`.

| Thư mục / file | Nội dung |
|---|---|
| `src\` | Code ứng dụng (`app.py` giao diện, `m0_clean.py` lõi xử lý, `tai_mo_hinh.py` tải mô hình) |
| `packaging\` | Cấu hình đóng gói, kiểm tra nạp, file `DOC-TRUOC.txt` kèm zip |
| `models\` | Mô hình tải về (không đưa lên git) |
| `samples\`, `outputs\` | Ảnh thử và kết quả (không đưa lên git) |
| `validation\` | Kết quả chấm (ảnh không đưa lên git) |
| `docs\` | Hỏi đáp (`QA.md`), quyết định (`decisions\`), bản khởi động (`KHOI-DONG.md`) |
| `HANDOVER.md` / `CHANGELOG.md` / `RULES.md` | Bàn giao giữa các phiên / thay đổi theo mốc / quy tắc làm việc |

## Giấy phép
GPL-3.0 (xem [LICENSE](LICENSE)). Nguồn và giấy phép các mô hình, thư viện: [THIRD-PARTY.md](THIRD-PARTY.md).
