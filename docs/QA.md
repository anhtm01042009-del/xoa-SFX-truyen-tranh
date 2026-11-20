# Hỏi & Đáp

Chỉ thêm. Độ chắc chắn: Đã kiểm chứng / Tra cứu / Giả định.

## 2026-11-09
- **Hỏi:** Nên dùng lại hay tự viết phần nhận diện chữ và vá nền?
  **Đáp:** Dùng lại mô hình có sẵn (nhận diện chữ + LaMa), tự viết giao diện và công cụ chỉnh. **Nguồn:** `docs\KHOI-DONG.md`. **Độ chắc chắn:** Giả định, kiểm chứng ở M0.
- **Hỏi:** LaMa có vá tốt nền phức tạp không?
  **Đáp:** Một bình luận Reddit cho rằng chỉ tốt với nền đơn sắc; chưa kiểm chứng trên trang của em. **Độ chắc chắn:** Tra cứu (ý kiến cá nhân).
- **Hỏi:** Trên máy của em (i5-4300U) một trang dài mất bao lâu?
  **Đáp:** Ảnh 804 × 9633 px mất 82.3 s, RAM đỉnh 1044 MB. Ảnh 645 × 22857 px mất 229.6 s, RAM đỉnh 1050 MB (mỗi ảnh đo 1 lần). Chưa đo ảnh Trung 16103 px. **Nguồn:** em Minh Anh chạy `chay_thu.bat` ngày 2026-11-11, báo cáo `outputs\may-em\m0_report.json`. **Độ chắc chắn:** Đã kiểm chứng (1 ảnh).
- **Hỏi:** Nhận diện chữ có chạy nổi trên CPU không?
  **Đáp:** Mô hình gốc ~56 s cho đoạn 1024×1024 (2 nhân CPU, máy của Claude). Sau khi bỏ nhánh thừa và chạy ở 0.75 kích thước, trang dài 9.6k–22.9k px mất 143–271 s. Chưa đo trên máy của em. **Nguồn:** `validation\M0-2026-11-11.md`. **Độ chắc chắn:** Đã kiểm chứng (trên máy Claude), Giả định (với máy em).
- **Hỏi:** Vá nền bằng LaMa trên CPU chậm không?
  **Đáp:** Không đáng kể khi chỉ vá vùng nhỏ quanh chữ: 1–2 s cho vùng 256–400 px, tổng 1–10 s mỗi trang dài (máy Claude). Vùng nền đơn sắc tô màu viền, không cần LaMa. **Độ chắc chắn:** Đã kiểm chứng (trên máy Claude).
- **Hỏi:** Máy của em chạy mô hình AI được đến đâu?
  **Đáp:** Máy là i5-4300U (2 nhân), RAM 7.7GB, Intel HD Graphics, không có card NVIDIA, nên chạy CPU. Tốc độ thật chưa biết, đo ở M0. **Nguồn:** ảnh Task Manager em Minh Anh gửi ngày 2026-11-09. **Độ chắc chắn:** Đã kiểm chứng (thông số), Giả định (khả năng chạy).
- **Hỏi:** License có cản trở không?
  **Đáp:** Theo trang manga-cleaner trên Hugging Face, mô hình nhận diện đến từ manga-image-translator (AGPL-3.0), code detector GPL-3.0, LaMa Apache-2.0. Chỉ ảnh hưởng khi phát hành cho người khác. **Độ chắc chắn:** Tra cứu.

## 2026-11-19
- **Hỏi:** Có đóng gói thành một file exe như Chụp Nét được không?
  **Đáp:** Được nhưng không nên: app dùng torch nên gói rất nặng, kiểu một file phải giải nén mỗi lần mở nên khởi động chậm. Chọn kiểu thư mục rồi nén zip; mô hình tải lần đầu mở. **Nguồn:** diễn đàn PyTorch và PyInstaller (người dùng báo torch đóng gói vài GB). **Độ chắc chắn:** Tra cứu; dung lượng thật của gói chưa đo.
- **Hỏi:** License có buộc phải công khai mã nguồn không?
  **Đáp:** Mô hình comic-text-detector và repo manga-image-translator (nơi tải mô hình) ghi GPL-3.0; gửi app cho người khác là phát hành nên kèm mã nguồn theo GPL-3.0. Repo công khai là cách đơn giản nhất. (Ghi chú 2026-11-09 nói AGPL-3.0 theo trang manga-cleaner; repo gốc hiện ghi GPL-3.0.) **Nguồn:** trang GitHub/ecosyste.ms của hai repo. **Độ chắc chắn:** Tra cứu (không phải tư vấn pháp lý).

## 2026-11-20
- **Hỏi:** Bạn dùng Mac mở file .exe không được?
  **Đáp:** .exe chỉ chạy trên Windows. Đã thêm bản Mac (chip Apple) đóng gói trên máy macOS của GitHub. Mac chip Intel không làm được vì torch đã ngừng phát hành bản cho Mac Intel. **Nguồn:** thử đóng gói trên GitHub Actions (macos-latest); torch trên PyPI chỉ có bản macosx arm64. **Độ chắc chắn:** Đã kiểm chứng (tự kiểm tra đạt), chưa mở tay trên Mac thật.
- **Hỏi:** Vì sao bản Mac lỗi "recursion is detected during loading of cv2"?
  **Đáp:** Khi PyInstaller xếp thành .app, gói cv2 bị tách phần dữ liệu (Contents/Resources) và phần nhị phân (Contents/Frameworks); bootstrap của cv2 nạp lại chính nó. Bản thư mục (không .app) chạy bình thường. Sửa bằng runtime hook nạp thẳng `cv2.abi3.so`. Hai cách khác thất bại: tự dựng .app (bootloader tìm thư viện ở Contents/Frameworks) và chép nguyên khối vào Frameworks (codesign từ chối thư mục `*.dist-info` và file dữ liệu). **Nguồn:** log GitHub Actions 2026-11-20. **Độ chắc chắn:** Đã kiểm chứng.
- **Hỏi:** Máy macos-14 của GitHub còn dùng được không?
  **Đáp:** Không: GitHub báo cấu hình macos-14 không còn hỗ trợ; dùng `macos-latest` (chip Apple). **Nguồn:** log Actions. **Độ chắc chắn:** Đã kiểm chứng.
- **Hỏi:** Bạn dùng Mac M1 mở được app nhưng báo "CERTIFICATE_VERIFY_FAILED … unable to get local issuer certificate" khi tải mô hình?
  **Đáp:** Python đóng gói (bản python.org, macOS) không dùng kho chứng chỉ của macOS; máy GitHub đã cài chứng chỉ nên tự kiểm tra không thấy lỗi. Sửa: `tai_mo_hinh.ssl_context()` = kho của máy + certifi; tự kiểm tra trên GitHub đặt `SSL_CERT_FILE`/`SSL_CERT_DIR` trỏ chỗ không có để giả lập. **Nguồn:** ảnh chụp lỗi từ máy bạn (2026-11-20), tái hiện trên máy Claude với kho chứng chỉ trống. **Độ chắc chắn:** Đã kiểm chứng (tái hiện + kiểm số chứng chỉ nạp được: 0 → 118).
