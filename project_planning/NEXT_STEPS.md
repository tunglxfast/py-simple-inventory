# Tóm Tắt Tiến Độ Và Bước Tiếp Theo

## Source Of Truth

Mọi bước tiếp theo phải tiếp tục bám theo 3 tài liệu chính:

- `project_rules/PROJECT_PLAN.md`: phạm vi sản phẩm, roadmap, page dự kiến, quyết định chức năng.
- `project_rules/ARCHITECTURE.md`: kiến trúc kỹ thuật, data flow, database, repositories, đóng gói.
- `project_rules/CODING_STANDARDS.md`: quy ước code, UI, repositories, validation, testing.

Nếu có quyết định mới, cập nhật tài liệu liên quan trước hoặc cùng lúc với code.

## Đã Xong

- Dựng cấu trúc project theo architecture: `app/`, `models/`, `repositories/`, `services/`, `routes/`, `templates/`, `static/`, `alembic/`, `tests/`, `scripts/`.
- Thêm cấu hình dependency trong `pyproject.toml`.
- Thêm database models cho `users`, `products`, `areas`, `stock_documents`, `stock_document_lines`.
- Thêm repositories; tất cả query SQLAlchemy đi qua `app/repositories/`.
- Thêm services cho sản phẩm, khu vực, kho, báo cáo, auth.
- Thêm UI Jinja2/Bootstrap cho các page chính.
- Copy vendor FE assets vào `app/static/vendor/`; app không dùng trực tiếp thư mục `vendors/`.
- Có luồng Database Setup tạo `data/inventory.db`.
- Có reset tồn kho bằng `ADJUST-IN` / `ADJUST-OUT`.
- Có export Excel cho báo cáo.
- Có tests nền; kết quả gần nhất: `7 passed`.
- Có `project_planning/CURRENT_STATUS.md` để checklist kiểm tra thủ công.

## Chưa Xong

- Auth chưa được bật chặn toàn bộ page chính.
- Dashboard mới ở mức cơ bản.
- Báo cáo chưa có filter theo ngày/khu vực/sản phẩm.
- Lịch sử phiếu kho chưa có filter.
- UI chưa polish kỹ theo screenshot mẫu.
- Chưa có workflow Alembic hoàn chỉnh khi tạo database lần đầu.
- Chưa có build PyInstaller Windows.
- Chưa test thủ công đầy đủ trên MacBook theo từng module.

## Dự Tính Bước Tiếp Theo

1. Hoàn thiện luồng Database Setup:
   - Tạo database bằng Alembic migration hoặc cơ chế migration rõ ràng.
   - Seed admin mặc định sau khi tạo database.

2. Hoàn thiện Auth:
   - Bật middleware bảo vệ các page chính.
   - Cho phép `/setup`, `/login`, `/static` truy cập không cần auth.
   - Kiểm tra login/logout end-to-end.

3. Kiểm tra và polish module Danh mục:
   - Sản phẩm: thêm/sửa/xoá inactive, checkbox xem inactive, search.
   - Khu vực: thêm/sửa/ẩn hiện.
   - Bổ sung tests route/service nếu cần.

4. Kiểm tra và polish module Kho:
   - Nhập kho nhiều dòng.
   - Xuất kho nhiều dòng.
   - Chặn xuất âm.
   - Lịch sử và chi tiết phiếu.

5. Hoàn thiện Báo cáo:
   - Thêm filter theo khoảng ngày, khu vực, sản phẩm.
   - Đảm bảo Excel xuất đúng bộ lọc.

6. Hoàn thiện Reset tồn kho:
   - Kiểm tra UI với nhiều sản phẩm.
   - Đảm bảo `ADJUST-IN` / `ADJUST-OUT` hiển thị hợp lý trong lịch sử và báo cáo.

7. Chuẩn bị đóng gói:
   - Tạo cấu hình PyInstaller.
   - Kiểm tra đường dẫn database portable cạnh `.exe`.
   - Build/test trên Windows sau khi chức năng chính ổn định.
