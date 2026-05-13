# Kiến Trúc

## Vai Trò Tài Liệu

Tài liệu này là source of truth cho kiến trúc kỹ thuật, cấu trúc thư mục, data flow, database schema, repositories, và cách app chạy offline/portable. Phạm vi sản phẩm nằm trong `PROJECT_PLAN.md`; quy tắc code nằm trong `CODING_STANDARDS.md`.

## Tổng Quan Kỹ Thuật

Ứng dụng là desktop app offline cho Windows. FastAPI phục vụ backend, Jinja2 render HTML, SQLite lưu dữ liệu local, và PyWebView mở UI như một desktop window. PyInstaller đóng gói app thành thư mục portable có file `.exe`.

Trong môi trường phát triển, app có thể chạy bằng uvicorn trên macOS để test nhanh trong browser hoặc PyWebView.

## Luồng Khởi Động App

1. Người dùng mở file `.exe`.
2. App xác định thư mục dữ liệu cùng level với file `.exe`.
3. App kiểm tra trong thư mục dữ liệu đã có SQLite database chưa.
4. Nếu đã có database, app kết nối tới database đó.
5. Nếu chưa có database, app hiển thị Database Setup để người dùng xác nhận tạo database mới.
6. Sau khi database sẵn sàng, FastAPI server local được khởi động ở background.
7. PyWebView mở cửa sổ desktop trỏ đến địa chỉ local của FastAPI.
8. Người dùng thao tác trên UI.
9. Route gọi service layer.
10. Service layer gọi repositories.
11. Repositories đọc/ghi SQLite thông qua SQLAlchemy session.

## Cấu Trúc Thư Mục Dự Kiến

```text
app/
  main.py
  webview_app.py
  core/
    config.py
    database.py
    logging.py
    security.py
  models/
  schemas/
  repositories/
  services/
  routes/
  templates/
  static/
    css/
    js/
alembic/
tests/
scripts/
```

## Vai Trò Các Thành Phần

- `app/main.py`: tạo FastAPI app, include routes, cấu hình templates và static files.
- `app/webview_app.py`: kiểm tra database, khởi động FastAPI local và mở PyWebView window.
- `app/core/config.py`: quản lý settings, đường dẫn database, và biến môi trường optional.
- `app/core/database.py`: engine, session factory, dependency lấy database session.
- `app/core/security.py`: hash password, verify password, auth helpers.
- `app/models/`: SQLAlchemy models.
- `app/schemas/`: Pydantic schemas cho validation và data transfer.
- `app/repositories/`: cổng truy cập dữ liệu duy nhất; chứa toàn bộ query SQLAlchemy của ứng dụng.
- `app/services/`: business logic và orchestration nghiệp vụ.
- `app/routes/`: FastAPI route handlers cho UI và form actions.
- `app/templates/`: Jinja2 templates tiếng Việt.
- `app/static/`: CSS/JS thuần và Bootstrap assets nếu cần bundle local.
- `alembic/`: database migrations.
- `tests/`: unit tests và route/template smoke tests.
- `scripts/`: seed data, maintenance scripts, build helpers.

## Data Access Flow

```text
routes -> services -> repositories -> SQLAlchemy session -> SQLite
```

Routes và services không query SQLAlchemy trực tiếp. Mọi truy cập database đi qua repositories để tránh query rải rác, dễ test, và dễ thay đổi sau này.

## Database V1

Tất cả cột dạng text trong database phải hỗ trợ Unicode tiếng Việt.

### `users`

- `id`
- `username`
- `password_hash`
- `is_active`
- `created_at`
- `updated_at`

### `products`

- `id`
- `code`
- `name`
- `unit`
- `note`
- `is_active`
- `created_at`
- `updated_at`

`products.code` là unique.

### `areas`

- `id`
- `name`
- `description`
- `is_active`
- `created_at`
- `updated_at`

### `stock_documents`

- `id`
- `type`: `IN`, `OUT`, `ADJUST-IN`, hoặc `ADJUST-OUT`
- `date`
- `area_id`
- `description`
- `proposed_by`
- `note`
- `created_at`
- `updated_at`

### `stock_document_lines`

- `id`
- `document_id`
- `product_id`
- `quantity`
- `note`
- `created_at`
- `updated_at`

## Luồng Dữ Liệu Nghiệp Vụ Chính

- Nhập kho: route nhận form -> service validate -> repository tạo phiếu và dòng phiếu -> báo cáo đọc lại từ giao dịch.
- Xuất kho: route nhận form -> service kiểm tra tồn -> repository tạo phiếu và dòng phiếu nếu hợp lệ.
- Báo cáo: route nhận bộ lọc -> service chuẩn hóa filter -> repository aggregate giao dịch -> route render bảng hoặc export Excel.
- Xoá sản phẩm: route nhận action -> service kiểm tra nghiệp vụ nếu cần -> repository set `is_active = false`.
- Reset tồn kho: route nhận số lượng tồn mong muốn cho từng sản phẩm -> service so sánh với tồn hiện tại -> repository tạo dòng điều chỉnh `ADJUST-IN` hoặc `ADJUST-OUT` theo phần chênh lệch.

## Adjustment Documents

Phiếu điều chỉnh tồn kho phục vụ chức năng reset/nhập lại tồn kho ban đầu.

- Nếu số lượng sản phẩm mà người dùng nhập lớn hơn tồn hiện tại, tạo điều chỉnh `ADJUST-IN` với số lượng bằng phần chênh lệch.
- Nếu số lượng sản phẩm mà người dùng nhập nhỏ hơn tồn hiện tại, tạo điều chỉnh `ADJUST-OUT` với số lượng bằng phần chênh lệch.
- Nếu số lượng sản phẩm mà người dùng nhập bằng tồn hiện tại, không tạo dòng điều chỉnh cho sản phẩm đó.
- Phiếu điều chỉnh không cần đầy đủ thông tin nghiệp vụ như phiếu nhập/xuất thường; chỉ bắt buộc `id`, `type`, `created_at`, và các dòng hàng liên quan.
- Các cột metadata của `stock_documents` như `date`, `area_id`, `description`, `proposed_by`, `note` cần cho phép nullable hoặc có chiến lược default phù hợp để hỗ trợ phiếu điều chỉnh.
- Báo cáo tồn kho phải tính cả `ADJUST-IN` như nhập và `ADJUST-OUT` như xuất.

## UI Architecture

- Server-rendered HTML bằng Jinja2.
- Bootstrap dùng cho layout, table, form, modal, button.
- CSS riêng tạo tone trắng và xanh lá nhạt.
- JavaScript chỉ dùng cho tương tác nhỏ như thêm/xóa dòng phiếu, tính tổng tạm thời, và validate form cơ bản.
- Layout chính gồm sidebar điều hướng và content area cho từng module.

Frontend framework khác chỉ được đưa vào nếu đã được chủ dự án đồng ý. Quy tắc này được định nghĩa trong `CODING_STANDARDS.md`.

## Đóng Gói Và Đường Dẫn Dữ Liệu

- Dev trên macOS:
  - Chạy FastAPI bằng uvicorn để test nhanh.
  - Có thể mở UI trong browser hoặc PyWebView.
- Release Windows:
  - Build bằng PyInstaller.
  - App được bàn giao dạng folder portable.
  - File `.exe` nằm trong folder release.
  - SQLite database nằm trong một thư mục cùng level với file `.exe`, ví dụ `data/inventory.db` hoặc tên thư mục tương tự được chốt khi implement.
  - Nếu database đã tồn tại thì app dùng database đó.
  - Nếu database chưa tồn tại thì app hiển thị Database Setup để người dùng xác nhận tạo database mới.
