# Database Setup

## Trạng Thái

Đã tạo kế hoạch chi tiết cho màn hình khởi tạo database.

## Mục Tiêu

Trang Database Setup dùng để bootstrap ứng dụng khi chưa có file database. Màn hình cần giải thích ngắn gọn tình trạng thiếu database, cung cấp một hành động rõ ràng để tạo database và đưa người dùng về luồng đăng nhập sau khi hoàn tất.

## Route Và Template

- Route GET: `/setup`
- Route POST: `/setup/create`
- Template: `app/templates/setup.html`

## Thành Phần UI

- Panel setup nằm giữa màn hình.
- Tiêu đề: `Chưa có database`.
- Nội dung giải thích ứng dụng chưa tìm thấy database trong thư mục dữ liệu.
- Nút chính: `Tạo database mới`.

## Hành Vi

- Nếu chưa có database, middleware redirect người dùng về `/setup`.
- Người dùng bấm `Tạo database mới`.
- App chạy Alembic migration để tạo database.
- App tạo tài khoản admin mặc định.
- Sau khi setup xong, redirect về `/login`.
- Nếu database đã tồn tại, GET `/setup` redirect về `/`.

## Quy Tắc Triển Khai

- Form tạo database dùng `method="post"` và submit về `/setup/create`.
- GET `/setup` chỉ hiển thị màn hình setup khi database chưa sẵn sàng.
- Khi database đã sẵn sàng, GET `/setup` đưa người dùng về trang chính.
- Quá trình tạo database chạy qua luồng khởi tạo database của ứng dụng.
- Sau khi tạo database và tài khoản admin mặc định, người dùng được đưa về `/login`.

## Kiểm Tra Thủ Công

- Xoá/đổi database dev và mở app.
- Kiểm tra app tự chuyển về `/setup`.
- Bấm `Tạo database mới`.
- Kiểm tra redirect về `/login`.
- Kiểm tra database được tạo bằng Alembic và có tài khoản admin mặc định.
