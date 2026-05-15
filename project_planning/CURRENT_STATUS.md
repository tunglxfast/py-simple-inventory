# Hiện Trạng App Để Kiểm Tra

## Cách Chạy

Khuyến nghị chạy app web local:

```bash
uv run python -m app.main
```

Sau đó mở:

```text
http://127.0.0.1:8000
```

Cũng có thể chạy PyWebView desktop:

```bash
uv run python -m app.webview_app
```

Lưu ý: chạy bằng `python -m ...` là cách chuẩn vì app dùng import theo package `app.*`.

## Database Setup

Hiện app có luồng kiểm tra database:

- Nếu chưa có database, truy cập `/` sẽ chuyển sang `/setup`.
- Page `/setup` có nút tạo database mới.
- Database được tạo tại:

```text
data/inventory.db
```

Sau khi tạo database, app tạo tài khoản admin mặc định:

```text
username: admin
password: admin
```

## Vendor Assets

App không dùng trực tiếp thư mục `vendors/`.

Các file vendor đã được copy vào:

```text
app/static/vendor/
```

Đang có:

- `bootstrap.min.css`
- `bootstrap.bundle.min.js`
- `htmx.min.js`
- `alpine.min.js`
- `apexcharts.min.js`

Templates đang dùng asset qua `/static/vendor/...`.

## Các Page Đã Có

- `/setup`: tạo database lần đầu.
- `/login`: đăng nhập admin local.
- `/`: Dashboard.
- `/products`: quản lý sản phẩm.
- `/areas`: quản lý khu vực.
- `/stock/IN`: nhập kho.
- `/stock/OUT`: xuất kho.
- `/documents`: lịch sử phiếu kho.
- `/documents/{id}`: chi tiết phiếu kho.
- `/reports/inventory`: báo cáo xuất - nhập - tồn.
- `/reports/inventory.xlsx`: xuất Excel báo cáo.
- `/inventory/reset`: reset/nhập lại tồn kho mong muốn.

## Chức Năng Đã Có

### Sản phẩm

- Thêm sản phẩm.
- Sửa sản phẩm.
- Xoá sản phẩm bằng cách chuyển `is_active = false`.
- Checkbox `Xem inactive` để xem cả sản phẩm inactive.
- Tìm kiếm theo mã hàng hoặc tên hàng.
- Mã hàng unique.
- Mã hàng, tên hàng, đơn vị tính, ghi chú hỗ trợ tiếng Việt Unicode.

### Khu vực

- Thêm khu vực.
- Sửa khu vực.
- Ẩn/hiện khu vực bằng `is_active`.
- Tên khu vực unique.

### Nhập kho

- Tạo phiếu nhập `IN`.
- Một phiếu có nhiều dòng hàng.
- Có ngày, khu vực, diễn giải, nhân viên đề xuất, ghi chú.
- Nhập kho làm tăng tồn.

### Xuất kho

- Tạo phiếu xuất `OUT`.
- Một phiếu có nhiều dòng hàng.
- Chặn xuất nếu số lượng xuất làm tồn kho bị âm.
- Xuất kho làm giảm tồn.

### Lịch sử và chi tiết phiếu

- Xem danh sách phiếu kho.
- Xem chi tiết phiếu và các dòng hàng.
- Phiếu điều chỉnh `ADJUST-IN` / `ADJUST-OUT` cũng nằm trong lịch sử.

### Báo cáo

- Báo cáo xuất - nhập - tồn hiển thị:
  - Mã hàng.
  - Tên hàng hóa.
  - Đơn vị tính.
  - Đầu kỳ.
  - Nhập.
  - Xuất.
  - Tồn cuối.
- Xuất Excel `.xlsx`.
- Báo cáo tính cả:
  - `IN` và `ADJUST-IN` như nhập.
  - `OUT` và `ADJUST-OUT` như xuất.

### Reset tồn kho

- Page `/inventory/reset` hiển thị tất cả sản phẩm active.
- Ô số lượng mong muốn mặc định là `0`.
- Không cho nhập số âm.
- Khi xác nhận:
  - Nếu tồn mong muốn lớn hơn tồn hiện tại, tạo `ADJUST-IN`.
  - Nếu tồn mong muốn nhỏ hơn tồn hiện tại, tạo `ADJUST-OUT`.
  - Nếu bằng tồn hiện tại, không tạo dòng điều chỉnh.

## Kiến Trúc Đã Theo Source Of Truth

- Có `models`.
- Có `repositories`.
- Có `services`.
- Có `routes`.
- Có `templates`.
- Có `static`.
- Tất cả query SQLAlchemy nằm trong `app/repositories/`.
- Services gọi repositories.
- Routes gọi services.

## Tests Hiện Có

Đã có test cho:

- Xoá sản phẩm bằng inactive.
- Nhập kho làm tăng tồn.
- Xuất kho làm giảm tồn.
- Chặn xuất âm.
- Reset tồn kho tạo `ADJUST-IN`.
- Reset tồn kho tạo `ADJUST-OUT`.
- Reset tồn kho từ chối số âm.
- Smoke test route setup/dashboard.

Lệnh kiểm tra:

```bash
uv run pytest
```

Kết quả gần nhất:

```text
7 passed
```

## Những Điểm Còn Chưa Hoàn Thiện

- Auth chưa được bật chặn toàn bộ page chính; login page và cookie auth đã có, nhưng middleware bảo vệ route sẽ cần làm chặt hơn ở module Auth.
- Dashboard mới ở mức tổng quan cơ bản.
- Báo cáo hiện chưa có filter theo ngày/khu vực/sản phẩm.
- Lịch sử phiếu hiện chưa có filter.
- UI mới là bản chức năng đầu tiên, chưa polish kỹ theo screenshot mẫu.
- Chưa có build PyInstaller Windows.
- Chưa có Alembic command workflow đầy đủ; hiện có migration file và app có thể tạo schema bằng SQLAlchemy metadata.

## Source Of Truth

Mọi bước phát triển đều phải bám theo 3 tài liệu chính:

- `project_rules/PROJECT_PLAN.md`: phạm vi sản phẩm, roadmap, page dự kiến, quyết định chức năng.
- `project_rules/ARCHITECTURE.md`: kiến trúc kỹ thuật, data flow, database, repositories, đóng gói.
- `project_rules/CODING_STANDARDS.md`: quy ước code, UI, repositories, validation, testing.

Nếu có quyết định mới, cập nhật tài liệu liên quan trước hoặc cùng lúc với code.
