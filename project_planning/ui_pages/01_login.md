# Login

## Trạng Thái

Giữ nguyên. Không thay đổi trong đợt thay template mới.

## Mục Tiêu

Giữ trang đăng nhập hiện tại vì chức năng và giao diện đã đủ cho giai đoạn này.

## Route Và Template

- Route GET: `/login`
- Route POST: `/login`
- Template: `app/templates/login.html`

## Thành Phần UI

- Panel đăng nhập nằm giữa màn hình.
- Tiêu đề: `Đăng nhập`.
- Alert lỗi nếu đăng nhập thất bại.
- Input `Tài khoản`.
- Input `Mật khẩu`.
- Nút chính `Đăng nhập`.
- Dòng ghi chú tài khoản mặc định lần đầu: `Mặc định lần đầu: admin / admin`.

## Hành Vi

- Người dùng nhập tài khoản và mật khẩu.
- Submit form bằng nút `Đăng nhập` hoặc phím Enter.
- Nếu hợp lệ, route tạo cookie `auth_token` và redirect về `/`.
- Nếu không hợp lệ, render lại trang với lỗi tiếng Việt.

## Không Thay Đổi

- Không đổi layout.
- Không đổi field name.
- Không đổi route/action.
- Không áp dụng template mới cho trang này trong đợt hiện tại.

## Kiểm Tra Thủ Công

- Mở `/login`.
- Đăng nhập sai để kiểm tra alert lỗi.
- Đăng nhập đúng để kiểm tra redirect.
- Kiểm tra có thể submit bằng phím Enter.
