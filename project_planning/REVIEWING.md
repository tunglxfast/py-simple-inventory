# Review Code Hiện Tại

## Mốc Review

Review này áp dụng cho code sau mốc `41a9866 implement basic` và các thay đổi phát sinh trong quá trình review.

Source of truth cần bám theo khi review:

- `project_rules/PROJECT_PLAN.md`
- `project_rules/ARCHITECTURE.md`
- `project_rules/CODING_STANDARDS.md`

## Đã Review Xong

### 1. Models

Đã review các model:

- `app/models/base.py`
- `app/models/user.py`
- `app/models/product.py`
- `app/models/area.py`
- `app/models/stock.py`

Ghi nhận:

- Cấu trúc bảng hiện khớp với source of truth v1.
- Có `is_active` cho `users`, `products`, `areas`.
- `stock_documents.type` hỗ trợ `IN`, `OUT`, `ADJUST-IN`, `ADJUST-OUT`.
- Các cột text dùng SQLAlchemy `String`/`Text`, phù hợp yêu cầu hỗ trợ Unicode tiếng Việt với SQLite.

### 2. Repositories

Đã review các repository:

- `app/repositories/product_repository.py`
- `app/repositories/area_repository.py`
- `app/repositories/user_repository.py`
- `app/repositories/stock_repository.py`

Ghi nhận:

- Query SQLAlchemy tập trung trong repositories, đúng `CODING_STANDARDS.md`.
- `stock_repository` tính tồn kho bằng giao dịch: `IN`/`ADJUST-IN` là cộng, `OUT`/`ADJUST-OUT` là trừ.
- Sau review services, `stock_repository.create_document()` đã chuyển từ nhận `dict` sang DTO `StockLineData` để tránh hard-code key string.

### 3. Services

Đã review các service:

- `app/services/exceptions.py`
- `app/services/product_service.py`
- `app/services/area_service.py`
- `app/services/stock_service.py`
- `app/services/auth_service.py`

Các thay đổi sau review:

- `product_service`:
  - Làm rõ `update_product()` cho phép sửa `code`, `name`, `unit`, `note`, `is_active`.
  - Khi trùng mã hàng, phân biệt sản phẩm đang active và sản phẩm đã inactive.
  - Xoá sản phẩm vẫn là set inactive, không hard delete.

- `area_service`:
  - Khi trùng tên khu vực, phân biệt khu vực đang active và khu vực đã inactive.

- `stock_service`:
  - Chặn tạo phiếu kho với khu vực inactive.
  - Chặn tạo phiếu kho với sản phẩm không tồn tại hoặc inactive.
  - Error message khi không tìm thấy sản phẩm có kèm ID.
  - Error message khi sản phẩm inactive hoặc không đủ tồn có kèm tên và ID.
  - Bỏ kiểu truyền line bằng `dict` và hard-code key như `"product_id"`, `"quantity"`.
  - Dùng DTO `StockLineData` cho line data giữa routes, services, repositories.
  - `normalize_lines()` được refactor gọn hơn bằng if/else khi merge dòng trùng sản phẩm.

- `auth_service`:
  - Đánh dấu `ensure_default_admin()` là bootstrap helper tạm thời.
  - Ghi chú cần xoá hoặc thay thế sau khi hoàn thiện luồng auth/admin setup thật.

Lý do thay đổi:

- Message lỗi rõ hơn để người dùng/dev biết chính xác record nào có vấn đề.
- Tôn trọng `is_active` đúng hơn ở service layer.
- Giảm rủi ro runtime do truyền dict tự do.
- Giữ đúng nguyên tắc routes -> services -> repositories.

Tests sau review services:

```text
uv run pytest
14 passed
```

### 4. Routes

Đã review `app/routes/`.

Ghi nhận:

- Routes đi đúng luồng `routes -> services -> repositories`.
- Không thấy route query repository trực tiếp.
- POST thành công dùng `RedirectResponse(..., status_code=303)`.
- Các lỗi nghiệp vụ quan trọng đã bắt `BusinessError` và render lại template với `status_code=400`.

Các thay đổi sau review:

- `products.py`:
  - `create_product`, `update_product`, `delete_product` xử lý `BusinessError`.
  - Tách helper render trang sản phẩm để tránh lặp `TemplateResponse`.

- `areas.py`:
  - `update_area` xử lý `BusinessError`.

- `stock.py`:
  - Bỏ điều kiện lọc `if pid and qty` khi tạo `StockLineData`, để service validate `quantity = 0`.
  - Đổi chức năng `/inventory/reset` thành `/inventory/adjust`.

- `reports.py`:
  - Tách mapping label cột export Excel khỏi đoạn hard-code rename trực tiếp.

### 5. Templates

Đã review `app/templates/`.

Ghi nhận:

- Static/vendor assets dùng đúng `/static/vendor/...`.
- Form fields nhìn chung khớp routes/services.
- UI text đang dùng tiếng Việt có dấu.
- Các page chính hiện có đủ theo phạm vi v1.

Các thay đổi sau review:

- Sửa `products.html` và `areas.html` để tránh đặt `<form>` trực tiếp trong `<tr>`.
- Thêm confirm dialog OK/Cancel cho các action thêm/sửa/xoá, lưu phiếu, điều chỉnh tồn kho.
- `stock_form.html` không còn render sẵn một dòng sản phẩm; người dùng bấm `Thêm sản phẩm` để thêm dòng.
- `document_detail.html` có nút quay lại lịch sử phiếu.
- `inventory_reset.html` được thay bằng `inventory_adjust.html`; tồn mong muốn mặc định bằng tồn hiện tại.

Quyết định sau review:

- Template hiện tại chỉ là bản chức năng v1.
- Khi polish UI, sẽ dùng template/UI mới thay thế thay vì tiếp tục chỉnh sâu bộ template hiện tại.

### 6. Core

Đã review `app/core/`.

Các thay đổi sau review:

- `security.py`:
  - Token đăng nhập có expiry.
  - `issued_at` trong token được dùng để kiểm tra TTL.

- `config.py`:
  - Thêm `AUTH_TOKEN_TTL_SECONDS`, mặc định 8 giờ.

- `database.py`:
  - `initialize_database()` chuyển sang chạy Alembic `upgrade head`, không dùng `Base.metadata.create_all()`.
  - Tạo thư mục theo `settings.database_path.parent` để hỗ trợ cả `DATABASE_PATH` override.

Ghi nhận còn lại:

- Middleware hiện mới kiểm tra database tồn tại, chưa bảo vệ các route chính bằng login.
- `SECRET_KEY` vẫn là config quan trọng để ký token, cần giữ ổn định cho app đã phát hành.

### 7. Scripts

Đã review `scripts/seed.py`.

Ghi nhận:

- Dùng cho dev/demo/manual testing.
- Gọi service layer, không query repository trực tiếp.
- Không xoá/drop/truncate dữ liệu.
- Có thể chạy lại nhiều lần vì bỏ qua lỗi trùng dữ liệu bằng `BusinessError`.
- Không thuộc runtime chính khi đóng gói PyInstaller, trừ khi cấu hình include/call rõ ràng.

### 8. Alembic

Đã review `alembic/`.

Ghi nhận:

- `env.py` lấy database URL từ `get_settings().database_url`.
- Migration đầu tiên tạo đủ bảng chính: `users`, `products`, `areas`, `stock_documents`, `stock_document_lines`.
- `initialize_database()` đã chuyển sang dùng Alembic.
- `alembic.ini` đã thêm `path_separator = os`.

### 9. Tests

Đã review `tests/`.

Ghi nhận:

- Service tests cover các workflow chính: danh mục, nhập/xuất kho, điều chỉnh tồn kho, inactive/missing records.
- Có test token expiry.
- Có test database init bằng Alembic.
- Route tests hiện vẫn là smoke tests nhẹ; có thể bổ sung sau khi thay template/UI mới.

### 10. Packaging/PyWebView

Đã review `app/webview_app.py`.

Các thay đổi sau review:

- Tìm port rảnh thay vì hard-code `8765`.
- Chờ server sẵn sàng bằng socket với timeout thay vì `time.sleep(1)`.
- Chạy bằng `uvicorn.Server` để shutdown sạch hơn.
- Thêm single-instance lock bằng file lock trong `data/app.lock`.

## Kết Luận Review

Review hiện tại đã đóng.

Phạm vi đã review:

- `app/models/`
- `app/repositories/`
- `app/services/`
- `app/routes/`
- `app/templates/`
- `app/core/`
- `scripts/`
- `alembic/`
- `tests/`
- `app/webview_app.py`

Trạng thái test cuối review:

```text
uv run pytest
17 passed
```

Ghi chú cho giai đoạn tiếp theo:

- Khi thay template/UI mới, cần review lại toàn bộ form action, field name, confirm flow, empty/error state và route smoke tests.
- Sau khi bật auth middleware thật, cần bổ sung test route bảo vệ login.
- Trước PyInstaller release, cần tạo spec/build workflow và kiểm tra static/templates/alembic trong bản đóng gói.
