# CHANGELOG

Chỉ thêm mục mới ở đầu danh sách, không sửa mục cũ.

## 2026-11-20 — Bản 0.1.1: thêm bản Mac
- Có thêm bản cho **Mac chip Apple (M1 trở lên)**: file `XoaChuTruyenTranh-mac.zip`, bên trong là `XoaChuTruyenTranh.app`. Mac chip Intel chưa hỗ trợ.
- Trên Mac, mô hình và nhật ký lỗi lưu ở `~/Library/Application Support/XoaChuTruyenTranh`, kết quả ở thư mục Hình ảnh (Pictures)/XoaChuTruyenTranh.
- Hướng dẫn sử dụng có thêm phần cài và mở app lần đầu trên Mac (app chưa có chữ ký của Apple nên phải cho phép trong Quyền riêng tư & Bảo mật).
- Trang phát hành ghi rõ file nào dành cho máy nào.
- Bản đóng gói dùng OpenCV 4 (bản 5 mới ra chưa đóng gói được trên Mac). Bản Windows: zip khoảng 253 MB; bản Mac: zip khoảng 263 MB, giải nén khoảng 845 MB; cộng khoảng 290 MB mô hình tải lần đầu.
- Cả hai bản đã tự kiểm tra trên máy của GitHub (không có màn hình); bản Mac chưa được mở thử bằng tay trên máy Mac thật.

## 2026-11-19 — Chuẩn bị bản 0.1.0 để chia sẻ
- App có số phiên bản (0.1.0) trên thanh tiêu đề và biểu tượng riêng.
- Lần đầu mở, nếu chưa có mô hình AI, app hỏi rồi tự tải (khoảng 290 MB, có thanh tiến độ, bấm Hủy được, kiểm đúng kích thước file). Không còn phải chạy `cai_dat.bat` mới có mô hình.
- Bản đóng gói lưu kết quả vào `Pictures\XoaChuTruyenTranh` và mô hình vào thư mục dữ liệu của người dùng; bản chạy từ mã nguồn giữ nguyên chỗ cũ (`outputs\`, `models\`).
- Lỗi bất ngờ được ghi vào file `nhat-ky-loi.txt` và báo bằng hộp thoại, để người dùng gửi lại.
- GitHub tự đóng gói app thành `XoaChuTruyenTranh-windows.zip` (giải nén là chạy, không cần cài Python); khi tạo bản phát hành, file zip được đính kèm.
- Thêm hướng dẫn sử dụng cho người dùng, giấy phép GPL-3.0 và danh sách nguồn, giấy phép các mô hình và thư viện.
- Lần đóng gói đầu tiên: file zip khoảng 261 MB, giải nén khoảng 752 MB, cộng khoảng 290 MB mô hình tải lần đầu. Đã tự kiểm tra trên máy Windows của GitHub (không có màn hình); chưa mở thử bằng tay trên máy Windows thật.

## 2026-11-11 (danh sách và lưu)
- Khoanh vùng dùng được cả trên ảnh gốc lẫn ảnh kết quả; nút "Khoanh vùng" đổi màu và có dòng báo khi đang bật; lỗi hiện thành hộp thoại.
- Danh sách ảnh có "Gỡ ảnh đã chọn" (phím Delete) và "Gỡ ảnh đã xong": chỉ gỡ khỏi danh sách, không xóa file.
- Thêm "Mở nơi lưu" và "Lưu bản sao…"; trạng thái ghi rõ nơi kết quả được tự lưu.
- Thêm `tao_loi_tat.bat` và biểu tượng để tạo lối tắt ngoài màn hình chính (chưa thử trên Windows).

## 2026-11-11 (khôi phục vùng)
- Thêm chế độ "Khôi phục bản gốc trong vùng" cho công cụ Khoanh vùng: giữ lại chữ/số bị xóa nhầm (ví dụ số chương). Chưa thử trên máy chạy thật.

## 2026-11-11 (khoanh vùng)
- Thêm công cụ "Khoanh vùng" và "Hoàn tác": em khoanh (chữ nhật hoặc vẽ tự do) chỗ còn sót chữ trên ảnh kết quả, phần mềm tự tìm và xóa chữ trong vùng đó. Có chế độ "Xóa hết vùng khoanh" cho chữ cách điệu mà máy không nhận ra. Mới thử tự động trên một số ca, chưa thử trên máy chạy thật; chữ số trang trí rất lớn và dãy chấm nhỏ còn khó xử lý.

## 2026-11-11 (bản giao diện)
- Giao diện đầu tiên (M1): mở ảnh hoặc thư mục (cũng kéo thả được), bấm "Xóa chữ", xem ảnh gốc và ảnh đã xóa cạnh nhau, có nút Dừng, thanh tiến độ, thu phóng và vài cài đặt nâng cao. Kết quả lưu thành file mới, không ghi đè ảnh gốc. Mới thử trên một ảnh; chưa thử trên máy chạy thật.

## 2026-11-11
- Bản thử đầu tiên (M0, chạy bằng dòng lệnh): xóa chữ trên trang truyện dài, tự chia đoạn và ghép lại. Thử trên 3 trang (Anh, Trung, Hàn): chữ thoại trong bong bóng xóa khá sạch; SFX cách điệu và chữ nhỏ trong bong bóng nền chuyển sắc còn sót hoặc vá chưa tốt. Kết quả chi tiết trong thư mục kiểm chứng.

## 2026-11-09
- Khởi động dự án "Xóa thoại & SFX truyện tranh": dựng khung thư mục, quy tắc làm việc, bản khảo sát và kế hoạch các mốc M0–M4. Chưa có chức năng phần mềm.
