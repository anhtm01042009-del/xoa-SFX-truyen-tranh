# Hướng dẫn dùng app Xóa chữ truyện tranh

App chạy trên **Windows 10/11** và **Mac chip Apple (M1, M2, M3, M4…)**. App xóa chữ thoại trong bong bóng (và một phần SFX) trên trang truyện, tự vá lại nền. Trang dài kiểu truyện cuộn dọc cũng được.

> Chỉ dùng cho truyện tự vẽ hoặc truyện bạn có quyền chỉnh sửa.
> Đây là bản thử nghiệm: SFX cách điệu và chữ rất nhỏ có thể còn sót, sửa bằng công cụ Khoanh vùng.

Tải ở trang **Releases**: https://github.com/anhtm01042009-del/xoa-SFX-truyen-tranh/releases/latest — chọn đúng file cho máy mình:

| Máy | File |
|---|---|
| Windows | `XoaChuTruyenTranh-windows.zip` |
| Mac chip Apple | `XoaChuTruyenTranh-mac.zip` |

Mac chip Intel chưa dùng được. Xem chip: quả táo → **Giới thiệu về máy Mac này** → dòng **Chip**.

## 1a. Cài trên Windows
1. Tải `XoaChuTruyenTranh-windows.zip`.
2. Chuột phải vào file zip → **Extract All** (Giải nén tất cả). Để thư mục ở chỗ dễ tìm, ví dụ `Documents`.
3. Mở thư mục vừa giải nén, bấm đúp **`XoaChuTruyenTranh.exe`**.
   - Nếu hiện "Windows protected your PC": bấm **More info → Run anyway** (app chưa có chữ ký số).
   - Giữ nguyên cả thư mục; đừng chép riêng file exe đi chỗ khác.
4. Lần đầu mở, app hỏi **tải mô hình AI** (khoảng 290 MB, chỉ tải một lần). Bấm **Yes** và đợi thanh tiến độ chạy hết. Cần có mạng.

Muốn có biểu tượng ngoài màn hình chính: chuột phải `XoaChuTruyenTranh.exe` → **Send to → Desktop (create shortcut)**.

## 1b. Cài trên Mac (chip Apple)
1. Tải `XoaChuTruyenTranh-mac.zip`, bấm đúp để giải nén (thường nằm trong **Tải về**).
2. Kéo **`XoaChuTruyenTranh.app`** vào thư mục **Ứng dụng (Applications)**.
3. Bấm đúp app. Lần đầu Mac sẽ chặn vì app chưa có chữ ký của Apple:
   - Bấm **Xong / OK** ở thông báo.
   - Mở **Cài đặt hệ thống → Quyền riêng tư & Bảo mật**, kéo xuống dưới cùng, bấm **Vẫn mở (Open Anyway)** cạnh dòng nói về XoaChuTruyenTranh, nhập mật khẩu máy, rồi bấm **Mở**. Chỉ phải làm một lần.
   - Máy macOS cũ (13 trở về trước) có thể làm nhanh hơn: chuột phải vào app → **Mở** → **Mở**.
4. Nếu Mac báo app **"bị hỏng và không thể mở"** (damaged): mở **Terminal** (Launchpad → gõ Terminal), dán dòng sau rồi Enter, sau đó mở lại app:
   ```
   xattr -cr /Applications/XoaChuTruyenTranh.app
   ```
5. Lần đầu mở, app hỏi **tải mô hình AI** (khoảng 290 MB, chỉ tải một lần). Bấm **Yes**. Mac có thể hỏi quyền truy cập thư mục Tải về/Màn hình nền khi mở ảnh ở đó: bấm **Cho phép**.

Phím tắt trên Mac dùng **Cmd** thay cho Ctrl (vd Cmd+Z để hoàn tác).

## 2. Xóa chữ
1. Bấm **Mở ảnh…** (hoặc **Mở thư mục…**, hoặc kéo thả ảnh vào cửa sổ). Nhận PNG, JPG, WEBP, BMP.
2. Bấm **Xóa chữ**. Trang dài mất vài phút trên máy yếu; có thể bấm **Dừng**.
3. Bên trái là ảnh gốc, bên phải là kết quả. Kết quả **tự lưu** vào thư mục **Pictures (Hình ảnh)/XoaChuTruyenTranh**, tên có đuôi `_clean.png`. App **không bao giờ ghi đè ảnh gốc**.
4. **Mở nơi lưu** để xem ảnh kết quả; **Lưu bản sao…** để lưu thêm một bản ra chỗ khác; **Thư mục lưu…** để đổi chỗ tự lưu.

## 3. Sửa chỗ còn sót hoặc xóa nhầm
Bật **Khoanh vùng**, chọn kiểu khoanh (chữ nhật hoặc vẽ tự do), rồi chọn việc cần làm:
- **Tự tìm chữ trong vùng**: app tìm kỹ hơn và xóa chữ trong vùng khoanh.
- **Xóa hết vùng khoanh**: xóa toàn bộ vùng, dùng cho SFX cách điệu app không nhận ra.
- **Khôi phục bản gốc trong vùng**: trả vùng về như ảnh gốc (giữ lại số chương, chữ cần giữ).

**Hoàn tác** lùi lại tối đa 15 bước. Lưu ý: bấm **Xóa chữ** lại cho cùng ảnh sẽ làm lại từ đầu, mất các chỗ đã sửa tay.

## 4. Gặp lỗi
Chụp màn hình lỗi và gửi kèm file nhật ký cho người làm app (hoặc tạo mục mới ở trang **Issues** của repo). File nằm ở:
- **Windows:** `%LOCALAPPDATA%\XoaChuTruyenTranh\nhat-ky-loi.txt` (dán vào ô địa chỉ của File Explorer rồi Enter).
- **Mac:** `~/Library/Application Support/XoaChuTruyenTranh/nhat-ky-loi.txt` (Finder → menu **Đi → Đi tới thư mục…**, dán đường dẫn).

## 5. Gỡ app
- **Windows:** xóa thư mục đã giải nén, và thư mục `%LOCALAPPDATA%\XoaChuTruyenTranh` (chứa mô hình đã tải).
- **Mac:** kéo app trong Ứng dụng vào Thùng rác, và xóa thư mục `~/Library/Application Support/XoaChuTruyenTranh`.

## 6. Cập nhật bản mới
Tải zip bản mới, giải nén đè (Windows) hoặc kéo app mới vào Ứng dụng thay app cũ (Mac). Mô hình đã tải được giữ lại, không phải tải lại.
