# Quy Định Trang UI

Tài liệu này sẽ là source of truth cho quy định chi tiết của từng trang UI.

## Phạm Vi

Các trang UI của ứng dụng được rút gọn còn các màn hình chính bên dưới. Những route phụ hoặc trạng thái chi tiết phải phục vụ trực tiếp cho các màn hình này, không tách thành module UI độc lập nếu chưa có quyết định mới.

## Quy Định Chung

- UI dùng tiếng Việt có dấu.
- Ưu tiên giao diện desktop quản lý kho: bảng dữ liệu lớn, thao tác rõ, mật độ thông tin cao.
- Các quyết định chi tiết về layout, màu sắc, nút, bảng, dialog và hành vi từng trang sẽ được bổ sung vào tài liệu này.

## Hình Ảnh Tham Chiếu

- `project_planning/Inventory Storage Manager Pro.jpg` là hình ảnh mẫu cho giao diện trang Sản phẩm.
- Giao diện mẫu có cấu trúc chính:
  - Thanh tiêu đề/top bar màu xanh.
  - Sidebar trái cho điều hướng và quick actions.
  - Khu vực tìm kiếm/lọc sản phẩm ở phía trên nội dung.
  - Nhóm nút thao tác sản phẩm nằm gần bảng.
  - Bảng sản phẩm là vùng nội dung chính.

## Danh Sách Trang

1. Login
2. Database Setup
3. Sản phẩm
   - Thêm sản phẩm.
   - Sửa sản phẩm.
   - Xoá sản phẩm.
   - Tìm sản phẩm.
4. Nhập kho
5. Xuất kho
6. Lịch sử phiếu kho
   - Bấm vào một phiếu sẽ mở Chi tiết phiếu kho.
7. Báo cáo xuất - nhập - tồn
8. Điều chỉnh
   - Điều chỉnh tồn kho.
   - Điều chỉnh khu vực.
