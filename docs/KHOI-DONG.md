# Khởi động dự án — 2026-11-09

## Đề bài
App desktop xóa chữ thoại và SFX truyện tranh mượt mà, giao diện đẹp, dễ dùng, đủ công cụ (cọ vá, chỉnh mask, so sánh trước/sau, xử lý hàng loạt). Dùng cho truyện tự vẽ hoặc có quyền chỉnh sửa. Chữ gốc: Nhật, Hàn, Trung, Anh. Giai đoạn sau: thay thoại bằng tiếng Việt có dấu.

## Khảo sát nhanh
Các công cụ có sẵn ghép 3 khâu: nhận diện chữ → tạo mask → vá nền (inpainting).

| Công cụ | Nhận xét |
|---|---|
| BallonsTranslator (github.com/dmMaze/BallonsTranslator) | App desktop: nhận diện, OCR, vá nền, cọ chỉnh mask, sửa chữ. Rất gần mục tiêu. |
| manga-image-translator (github.com/zyddnys/manga-image-translator) | Pipeline xóa chữ + dịch + dàn chữ; dùng mô hình vá kiểu LaMa. License chưa rõ trong README. |
| PanelCleaner (VoxelCubes) | App desktop chuyên xóa chữ, dùng Comic Text Detector + LaMa. Nguồn tra cứu là blog bên thứ ba, cần kiểm lại ở repo gốc. |
| LaMa | Mô hình vá vùng lớn, Apache-2.0 (theo trang manga-cleaner). |

Đề xuất: tự viết app và giao diện, dùng lại mô hình nhận diện + LaMa.

## Rủi ro và cách kiểm chứng sớm
| Rủi ro | Kiểm chứng |
|---|---|
| SFX đè tranh vá không sạch | Thử 10 trang nhiều kiểu SFX trước khi làm giao diện |
| Chạy chậm / hết bộ nhớ | Đo 1 trang ở CPU và GPU ngay ở M0 |
| Nhận diện sai (sót chữ, xóa nhầm nét vẽ) | Luôn cho xem mask trước khi vá, có cọ chỉnh tay |

## Mốc
| Mốc | Nội dung | Tiêu chí xong |
|---|---|---|
| M0 | Dòng lệnh: 1 ảnh vào, 1 ảnh đã xóa chữ ra | ≥ 7/10 trang mẫu sạch bằng mắt thường |
| M1 | Giao diện cơ bản: mở ảnh, xem trước/sau, xuất ảnh | Mở và lưu 1 trang không cần dòng lệnh |
| M2 | Cọ vẽ/xóa mask, vá lại vùng chọn, hoàn tác | Sửa 1 vùng vá hỏng chỉ bằng chuột |
| M3 | Xử lý cả thư mục, tiến độ, lưu cài đặt | Chạy hết 1 chương không treo |
| M4 | Thay thoại: bấm bong bóng, gõ chữ Việt, font tự do | Chữ có dấu hiển thị đúng, vừa bong bóng |

Chưa làm: dịch tự động, thay SFX bằng chữ Việt, bản Android, huấn luyện mô hình mới, phát hành cho người khác.

## Nguồn
- https://www.GitHub.com/dmMaze/BallonsTranslator/blob/dev/README_EN.md
- https://github.com/zyddnys/manga-image-translator
- https://converter.brightcoding.dev/blog/panelcleaner-the-secret-tool-manga-translators-are-hiding
- https://huggingface.co/kzome/manga-cleaner
