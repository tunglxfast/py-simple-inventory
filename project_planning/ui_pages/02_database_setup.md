# Database Setup

## Trạng Thái

Giữ nguyên. Không thay đổi trong đợt thay template mới.

## Mục Tiêu

Giữ trang setup database hiện tại vì đây là màn hình bootstrap đơn giản, chỉ xuất hiện khi chưa có database.

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

## Không Thay Đổi

- Không đổi layout.
- Không đổi route/action.
- Không đổi nội dung chính.
- Không áp dụng template mới cho trang này trong đợt hiện tại.

## Kiểm Tra Thủ Công

- Xoá/đổi database dev và mở app.
- Kiểm tra app tự chuyển về `/setup`.
- Bấm `Tạo database mới`.
- Kiểm tra redirect về `/login`.
- Kiểm tra database được tạo bằng Alembic và có tài khoản admin mặc định.
