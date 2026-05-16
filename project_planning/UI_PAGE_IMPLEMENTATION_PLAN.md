# Kế Hoạch Triển Khai Trang UI

## Mục Đích

Tài liệu này là trang tổng hợp kế hoạch triển khai UI. Chi tiết từng trang được tách ra các file riêng trong `project_planning/ui_pages/`.

Source of truth về danh sách trang, quy định giao diện và hình ảnh tham chiếu vẫn là `project_rules/UI_PAGES.md`. File này chỉ dùng để theo dõi trạng thái tổng quan và trỏ đến kế hoạch chi tiết của từng trang.

## Trạng Thái Tổng Quan

| Trang | Trạng thái | File kế hoạch | Ghi chú |
|---|---|---|---|
| Login | Giữ nguyên | `project_planning/ui_pages/01_login.md` | Không thay đổi trong đợt thay template mới |
| Database Setup | Giữ nguyên | `project_planning/ui_pages/02_database_setup.md` | Không thay đổi trong đợt thay template mới |
| Sản phẩm | Chờ yêu cầu chi tiết | `project_planning/ui_pages/03_products.md` | Bám ảnh mẫu `Inventory Storage Manager Pro.jpg` |
| Nhập kho | Chờ yêu cầu chi tiết | `project_planning/ui_pages/04_stock_in.md` | Thiết kế theo template mới |
| Xuất kho | Chờ yêu cầu chi tiết | `project_planning/ui_pages/05_stock_out.md` | Thiết kế theo template mới |
| Lịch sử phiếu kho | Chờ yêu cầu chi tiết | `project_planning/ui_pages/06_documents.md` | Bao gồm luồng mở Chi tiết phiếu kho |
| Báo cáo xuất - nhập - tồn | Chờ yêu cầu chi tiết | `project_planning/ui_pages/07_inventory_report.md` | Thiết kế theo template mới |
| Điều chỉnh | Chờ yêu cầu chi tiết | `project_planning/ui_pages/08_adjustments.md` | Bao gồm điều chỉnh tồn kho và khu vực |

## Thứ Tự Triển Khai Đề Xuất

1. Sản phẩm
2. Nhập kho
3. Xuất kho
4. Lịch sử phiếu kho
5. Báo cáo xuất - nhập - tồn
6. Điều chỉnh

## Ghi Chú

- Login và Database Setup giữ nguyên.
- Khi một trang được chốt yêu cầu UI, cập nhật file riêng của trang đó trước khi chỉnh code.
- Sau khi thay template từng trang, cần kiểm tra lại form action, field name, confirm flow, empty state, error state và route smoke tests.
