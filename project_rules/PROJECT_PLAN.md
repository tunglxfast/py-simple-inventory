# Kế Hoạch Dự Án

## Vai Trò Tài Liệu

Tài liệu này là source of truth cho phạm vi sản phẩm, roadmap triển khai, danh sách page dự kiến, và các quyết định chức năng đã chốt. Chi tiết kỹ thuật nằm trong `project_rules/ARCHITECTURE.md`; quy tắc viết code nằm trong `project_rules/CODING_STANDARDS.md`; quy định chi tiết cho các trang UI nằm trong `project_rules/UI_PAGES.md`.

## Mục Tiêu Sản Phẩm

Xây dựng ứng dụng quản lý kho đơn giản, chạy offline trên Windows. Người dùng cuối chỉ cần mở file `.exe` trong thư mục portable, không cần cài đặt Python hay dependency riêng.

Các chức năng chính của v1:

- Nhập kho.
- Xuất kho.
- Quản lý sản phẩm.
- Quản lý khu vực.
- Báo cáo xuất - nhập - tồn.
- Xuất báo cáo Excel.
- Đăng nhập admin local.
- Điều chỉnh tồn kho ban đầu cho sản phẩm.

UI dùng tiếng Việt, ưu tiên phong cách desktop app quản lý kho: bảng dữ liệu lớn, sidebar điều hướng, tìm kiếm/lọc rõ ràng, tông trắng và xanh lá nhạt.

## Tech Stack Đã Chốt

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Alembic
- Jinja2
- HTML/CSS thuần
- Bootstrap
- PyWebView
- PyInstaller
- Pydantic
- uvicorn
- bcrypt
- httpx
- logging
- pandas
- openpyxl
- python-dotenv optional

## Roadmap V1

### 1. Tạo kiến trúc project

- Tạo cấu trúc thư mục nền cho app.
- Cấu hình FastAPI, Jinja2, static files, logging, database session.
- Tạo entrypoint chạy dev và entrypoint desktop bằng PyWebView.
- Chuẩn bị nền đóng gói Windows portable.

### 2. Tạo database và models

- Tạo SQLAlchemy models.
- Tạo Alembic migration đầu tiên.
- Tạo luồng kiểm tra database khi app mở.
- Tạo seed data phục vụ test thủ công và test tự động.

### 3. Danh mục sản phẩm và khu vực

- Sản phẩm:
  - Danh sách sản phẩm.
  - Tìm kiếm theo mã hàng và tên hàng.
  - Thêm/sửa/xoá sản phẩm.
  - Xoá sản phẩm là chuyển sang inactive, không hard delete.
  - Có checkbox xem inactive để hiển thị cả sản phẩm đã xoá/inactive.
- Khu vực:
  - Danh sách khu vực.
  - Thêm/sửa khu vực.
  - Ẩn/hiện khu vực.

### 4. Nhập kho và xuất kho

- Tạo phiếu nhập nhiều dòng hàng.
- Tạo phiếu xuất nhiều dòng hàng.
- Chặn xuất kho nếu làm tồn kho bị âm.
- Có lịch sử phiếu và trang chi tiết phiếu.

### 5. Báo cáo xuất - nhập - tồn

- Lọc báo cáo theo khoảng ngày.
- Lọc theo khu vực và sản phẩm.
- Hiển thị đầu kỳ, nhập, xuất, tồn cuối.
- Xuất file `.xlsx` theo bộ lọc hiện tại.

### 6. Điều chỉnh tồn kho

- Có page riêng hiển thị tất cả sản phẩm với ô số lượng mặc định bằng tồn hiện tại.
- Người dùng nhập số lượng tồn mong muốn cho từng sản phẩm; số lượng không được âm.
- Khi xác nhận, app tạo phiếu điều chỉnh nhập/xuất nếu cần để tồn kho sau cùng bằng đúng số lượng người dùng đã nhập.
- Chức năng này là chức năng phụ, triển khai sau khi các chức năng kho chính đã ổn định.

### 7. Login/Auth

- Đăng nhập admin local.
- Lưu password bằng bcrypt hash.
- Bảo vệ các page chính.
- Hỗ trợ logout.

### 8. Đóng gói Windows

- Build bằng PyInstaller.
- Bàn giao app dạng thư mục portable.
- Kiểm tra người dùng mở app, tạo database nếu chưa có, nhập dữ liệu, đóng app, mở lại và dữ liệu vẫn còn.

## Danh Sách Page Dự Kiến

Quy định chi tiết về layout, thành phần, hành vi, text, màu sắc và trải nghiệm của từng trang UI sẽ được quản lý trong `project_rules/UI_PAGES.md`.

- Login: đăng nhập admin local.
- Database Setup: thông báo chưa có database và nút tạo database mới.
- Dashboard: tổng quan nhanh tồn kho, số sản phẩm, số phiếu gần đây.
- Sản phẩm: danh sách, tìm kiếm, thêm/sửa/xoá, checkbox xem inactive.
- Khu vực: danh sách, thêm/sửa, ẩn/hiện.
- Nhập kho: tạo phiếu nhập nhiều dòng.
- Xuất kho: tạo phiếu xuất nhiều dòng và kiểm tra tồn.
- Lịch sử phiếu kho: xem, tìm kiếm, lọc phiếu nhập/xuất.
- Chi tiết phiếu kho: xem thông tin phiếu và các dòng hàng.
- Báo cáo xuất - nhập - tồn: xem báo cáo và xuất Excel.
- Điều chỉnh tồn kho: nhập số lượng tồn mong muốn cho tất cả sản phẩm.

## Quyết Định Chức Năng Đã Chốt

- Database/table/field dùng tiếng Anh; UI label, message, form text dùng tiếng Việt.
- Mọi cột text trong database phải hỗ trợ tiếng Việt Unicode.
- Mã hàng và tên hàng có thể là tiếng Việt.
- `Khu Vực` là danh mục riêng.
- Tồn kho được tính từ giao dịch, không dùng `current_stock` làm nguồn sự thật.
- Phiếu kho dùng mô hình header + nhiều dòng hàng.
- Không cho xuất âm kho.
- Điều chỉnh tồn kho tạo giao dịch điều chỉnh `ADJUST-IN` hoặc `ADJUST-OUT` theo chênh lệch giữa tồn hiện tại và số lượng người dùng nhập.
- Product v1 gồm tối thiểu: mã hàng, tên hàng hóa, đơn vị tính, ghi chú, trạng thái active.
- Xoá sản phẩm trong UI là chuyển sản phẩm sang inactive.
- Báo cáo v1 có xuất Excel.
- Database portable nằm trong thư mục dữ liệu cùng level với `.exe`.
- Thứ tự module ưu tiên: Danh mục -> Kho -> Báo cáo -> Auth, sau khi đã có kiến trúc project và database.

## Tiêu Chí Hoàn Thành Mỗi Module

- Có đủ backend, UI, validation, và test cho workflow chính.
- UI render được và thao tác được trên MacBook trong quá trình dev.
- Người dùng kiểm tra manual xong mới chuyển sang module tiếp theo.
