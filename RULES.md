# RULES — Quy tắc làm việc

Chỉ thêm dòng mới ở cuối. Mâu thuẫn với dòng cũ thì hỏi em Minh Anh, không tự sửa.

## Quy tắc cứng ban đầu
- 2026-11-09 — Chỉ xử lý truyện tự vẽ hoặc truyện em có quyền chỉnh sửa.
- 2026-11-09 — Không ghi đè ảnh gốc; kết quả luôn lưu ra thư mục riêng (`outputs\`).
- 2026-11-09 — Không xóa file khi chưa hỏi em.
- 2026-11-09 — Không ghi số liệu hoặc kết quả thử nghiệm mà em chưa tự đo.
- 2026-11-09 — Mô hình nhận diện/vá nền dùng lại bản có sẵn; chưa huấn luyện mô hình mới ở giai đoạn đầu.
- 2026-11-09 — Trước khi phát hành app cho người khác phải kiểm lại license của mô hình và code đã dùng lại (một số thành phần là AGPL/GPL).

## Chốt phiên
- 2026-11-09 — Đầu phiên chạy `tiep-quan` (đọc `HANDOVER.md` trước).
- 2026-11-09 — Trong phiên, quyết định lâu dài của em ghi dần vào `RULES.md`; thay đổi ở sản phẩm ghi vào `CHANGELOG.md`.
- 2026-11-09 — Cuối phiên chạy `ban-giao`: ghi đè `HANDOVER.md`, thêm dòng vào `CHANGELOG.md` và `docs\QA.md`.

## Đã chốt từ trao đổi trước
- 2026-11-09 — Ứng dụng desktop, không làm web.
- 2026-11-09 — Chữ gốc có thể là Nhật, Hàn, Trung hoặc Anh.
- 2026-11-09 — Ngôn ngữ app phải xử lý: Trung, Nhật, Hàn, Anh (chữ gốc) và Việt (chữ thay vào).
- 2026-11-09 — Ngôn ngữ lập trình: Python + PySide6 (em Minh Anh đã đồng ý).
- 2026-11-09 — Máy chạy không có card NVIDIA, chưa rõ dòng máy: app phải chạy được trên CPU, không phụ thuộc CUDA.
- 2026-11-09 — Máy mục tiêu (theo ảnh Task Manager em gửi): Intel Core i5-4300U 1.90GHz (2 nhân, 4 luồng), RAM 7.7GB (lúc chụp đã dùng khoảng 5.2GB), Intel HD Graphics (128MB riêng, 2GB chia sẻ), ổ SSD. App phải tiết kiệm RAM: xử lý từng trang, giải phóng bộ nhớ sau mỗi trang.
- 2026-11-11 — App phải xử lý được một trang truyện dài (dải dọc, ví dụ ảnh ghép từ nhiều lần chụp) trong một lần chạy, để em tiết kiệm thời gian. Lõi xử lý chia trang dài thành các đoạn nhỏ có phần chồng lên nhau, xử lý lần lượt từng đoạn, rồi ghép lại; không nạp cả trang vào mô hình cùng lúc.
- 2026-11-11 — Phạm vi giai đoạn đầu: truyện "cơ bản" (thoại trong bong bóng, khung chữ). SFX cách điệu và chữ nhỏ khó nhận diện được chấp nhận sót ở tự động, sửa bằng công cụ chỉnh tay.
- 2026-11-11 — Chỉnh chỗ sót/xóa nhầm theo kiểu "em khoanh vùng, máy tự xử lý chỗ đó"; không làm công cụ tô vẽ thủ công.
- 2026-11-11 — Chữ/số cần giữ (ví dụ số chương) em giữ bằng cách khoanh rồi "Khôi phục bản gốc trong vùng"; chưa làm tự động bảo vệ.
- 2026-11-11 — Gỡ ảnh khỏi danh sách trong app chỉ gỡ khỏi danh sách, không xóa file trên máy; kết quả tự lưu thành `_clean.png` trong thư mục lưu.
- 2026-11-09 — Tính năng thay thoại: bấm chọn bong bóng, gõ hoặc dán chữ đã dịch; đích là tiếng Việt có dấu; bong bóng làm trước, SFX làm sau; font dùng loại license tự do.

## Chia sẻ cho người khác dùng (2026-11-19)
- 2026-11-19 — Chia sẻ app theo cách của Chụp Nét: repo GitHub công khai `anhtm01042009-del/xoa-SFX-truyen-tranh`, GitHub tự đóng gói, em tạo bản phát hành trên web. Gửi cho bạn file `XoaChuTruyenTranh-windows.zip` (đóng gói kiểu thư mục, không phải 1 file exe vì có torch).
- 2026-11-19 — Mô hình AI không nằm trong zip; ban đóng gói tự tải lần đầu mở vào `%LOCALAPPDATA%\XoaChuTruyenTranh\models`, kiểm đúng kích thước file trước khi dùng.
- 2026-11-19 — Repo và gói phát hành không chứa `samples\`, `outputs\`, ảnh truyện của người khác (kể cả ảnh trong `validation\`), mô hình, hay đường dẫn trên máy em.
- 2026-11-19 — Mã nguồn phát hành theo GPL-3.0; `THIRD-PARTY.md` ghi nguồn và license từng mô hình, thư viện; cập nhật khi thêm thành phần mới.
- 2026-11-19 — Hướng dẫn và hộp thoại đầu tiên của app nhắc: chỉ dùng cho truyện tự vẽ hoặc có quyền chỉnh sửa.
- 2026-11-19 — Mỗi bản phát hành: đổi `src\phien_ban.py`, thêm dòng `CHANGELOG.md`, tag `vX.Y.Z` trùng số phiên bản, trỏ vào commit đã đóng gói xanh; em tải zip thử trên một máy chưa cài Python trước khi gửi rộng.
- 2026-11-19 — Lõi `src\m0_clean.py` chỉ sửa khi có ca kiểm chứng; sửa xong chạy lại các ca trong `validation\`.
- 2026-11-19 — Đã dùng git: cuối phiên `ban-giao` có thêm bước commit và push lên `main`.
- 2026-11-20 — Phát hành cho Windows và Mac chip Apple (M1 trở lên); không hỗ trợ Mac chip Intel (torch không còn bản cho Mac Intel).
- 2026-11-20 — Bản Mac đóng gói bằng BUNDLE của PyInstaller kèm `packaging/rthook_cv2_mac.py` (nạp thẳng lõi cv2); không tự dựng .app hay chép thư viện nguyên khối vào Frameworks (codesign từ chối). Khóa `opencv-python-headless<5` cho bản đóng gói cho tới khi thử lại được OpenCV 5.
