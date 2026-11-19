# Hướng dẫn dùng app Xóa chữ truyện tranh

App chạy trên **Windows 10/11**, xóa chữ thoại trong bong bóng (và một phần SFX) trên trang truyện, tự vá lại nền. Trang dài kiểu truyện cuộn dọc cũng được.

> Chỉ dùng cho truyện tự vẽ hoặc truyện bạn có quyền chỉnh sửa.
> Đây là bản thử nghiệm: SFX cách điệu và chữ rất nhỏ có thể còn sót, sửa bằng công cụ Khoanh vùng.

## 1. Cài đặt
1. Vào trang **Releases** của repo: https://github.com/anhtm01042009-del/xoa-SFX-truyen-tranh/releases
2. Tải file `XoaChuTruyenTranh-windows.zip` của bản mới nhất.
3. Chuột phải vào file zip → **Extract All** (Giải nén tất cả). Để thư mục ở chỗ dễ tìm, ví dụ `Documents`.
4. Mở thư mục vừa giải nén, bấm đúp **`XoaChuTruyenTranh.exe`**.
   - Nếu hiện "Windows protected your PC": bấm **More info → Run anyway** (app chưa có chữ ký số).
   - Giữ nguyên cả thư mục; đừng chép riêng file exe đi chỗ khác.
5. Lần đầu mở, app hỏi **tải mô hình AI** (khoảng 290 MB, chỉ tải một lần). Bấm **Yes** và đợi thanh tiến độ chạy hết. Cần có mạng.

Muốn có biểu tượng ngoài màn hình chính: chuột phải `XoaChuTruyenTranh.exe` → **Send to → Desktop (create shortcut)**.

## 2. Xóa chữ
1. Bấm **Mở ảnh…** (hoặc **Mở thư mục…**, hoặc kéo thả ảnh vào cửa sổ). Nhận PNG, JPG, WEBP, BMP.
2. Bấm **Xóa chữ**. Trang dài mất vài phút trên máy yếu; có thể bấm **Dừng**.
3. Bên trái là ảnh gốc, bên phải là kết quả. Kết quả **tự lưu** vào `Pictures\XoaChuTruyenTranh`, tên có đuôi `_clean.png`. App **không bao giờ ghi đè ảnh gốc**.
4. **Mở nơi lưu** để xem ảnh kết quả; **Lưu bản sao…** để lưu thêm một bản ra chỗ khác; **Thư mục lưu…** để đổi chỗ tự lưu.

## 3. Sửa chỗ còn sót hoặc xóa nhầm
Bật **Khoanh vùng**, chọn kiểu khoanh (chữ nhật hoặc vẽ tự do), rồi chọn việc cần làm:
- **Tự tìm chữ trong vùng**: app tìm kỹ hơn và xóa chữ trong vùng khoanh.
- **Xóa hết vùng khoanh**: xóa toàn bộ vùng, dùng cho SFX cách điệu app không nhận ra.
- **Khôi phục bản gốc trong vùng**: trả vùng về như ảnh gốc (giữ lại số chương, chữ cần giữ).

**Hoàn tác** lùi lại tối đa 15 bước. Lưu ý: bấm **Xóa chữ** lại cho cùng ảnh sẽ làm lại từ đầu, mất các chỗ đã sửa tay.

## 4. Gặp lỗi
Chụp màn hình lỗi và gửi kèm file nhật ký cho người làm app. File nằm ở:
```
%LOCALAPPDATA%\XoaChuTruyenTranh\nhat-ky-loi.txt
```
(Dán dòng trên vào ô địa chỉ của File Explorer rồi Enter để mở.) Hoặc tạo mục mới ở trang **Issues** của repo.

## 5. Gỡ app
Xóa thư mục đã giải nén, và thư mục `%LOCALAPPDATA%\XoaChuTruyenTranh` (chứa mô hình đã tải).

## 6. Cập nhật bản mới
Tải zip bản mới, giải nén đè hoặc ra thư mục mới. Mô hình đã tải được giữ lại, không phải tải lại.
