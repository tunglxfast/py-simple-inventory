# Login

## Trạng Thái

Đã tạo kế hoạch chi tiết cho màn hình đăng nhập.

## Mục Tiêu

Trang Login dùng để xác thực người dùng local trước khi vào ứng dụng quản lý kho. Màn hình cần tối giản, tập trung vào form đăng nhập, hiển thị lỗi rõ ràng và hỗ trợ thao tác nhanh bằng phím Enter.

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

## Quy Tắc Triển Khai

- Form dùng `method="post"` và submit về `/login`.
- Field tài khoản dùng name tương ứng với route xử lý đăng nhập.
- Field mật khẩu dùng input type `password`.
- Alert lỗi chỉ hiển thị khi route truyền biến lỗi về template.
- Sau khi đăng nhập thành công, người dùng được đưa tới trang chính của ứng dụng.
- Cookie xác thực do route đăng nhập chịu trách nhiệm tạo.

## Kiểm Tra Thủ Công

- Mở `/login`.
- Đăng nhập sai để kiểm tra alert lỗi.
- Đăng nhập đúng để kiểm tra redirect.
- Kiểm tra có thể submit bằng phím Enter.
