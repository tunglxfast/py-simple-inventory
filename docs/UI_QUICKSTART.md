# UI Quickstart

Tài liệu này mô tả cách dùng nhanh giao diện ứng dụng kho cho người dùng nghiệp vụ.

## 1. Mở ứng dụng

- Tkinter (ổn định hiện tại):

```bash
python3 app.py
```

- PySide6 (giao diện mới):

```bash
uv pip install -e ".[gui]"
uv run python app_qt.py
```

## 2. Luồng thao tác cơ bản

1. `Sản phẩm (Products)`
- Tạo mã hàng, tên hàng, đơn vị.
- Kiểm tra danh sách tồn kho ở bảng bên dưới.

2. `Nhập kho (Import)`
- Nhập `Mã hàng`, `Số lượng`, `Ghi chú` (nếu có).
- Bấm `Lưu` để cộng tồn.

3. `Xuất kho (Export)`
- Nhập `Mã hàng`, `Số lượng`, `Ghi chú`.
- Bấm `Lưu` để trừ tồn, hệ thống trả về mã bán hàng.

4. `Giữ hàng (Hold)`
- Thêm các dòng `Mã hàng + Số lượng`.
- Bấm `Lưu` để tạo phiên giữ hàng.

5. `Quản lý giữ hàng (Hold Management)`
- Chọn phiên giữ hàng.
- Nhập số lượng trả lại cho từng dòng (nếu có).
- Bấm `Chốt giữ hàng` để hoàn tất.

6. `Bán hàng (Sales)`
- Xem danh sách mã bán hàng và chi tiết item đã xuất.

7. `Báo cáo (Reports)`
- Chọn ngày bắt đầu/kết thúc.
- Bấm `Xem báo cáo` để tải số liệu nhập/xuất/tồn.

8. `Thiết lập (Setup)`
- `Xem trước`/`Nhập tồn đầu` từ file Excel/CSV.
- `Reset DB` (cần token `RESET`).
- `Sao lưu` và `Phục hồi` DB (phục hồi có hộp thoại xác nhận).

## 3. Lưu ý an toàn

- `Reset DB` và `Restore DB` là thao tác ảnh hưởng dữ liệu; hãy sao lưu trước.
- Sau khi `Restore DB`, nên khởi động lại ứng dụng.
- File import cần đúng header cột theo định dạng hệ thống.
