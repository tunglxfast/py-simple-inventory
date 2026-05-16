# Lịch sử phiếu kho

## Trạng Thái

Đã tạo kế hoạch chi tiết cho trang Lịch sử phiếu kho và Chi tiết phiếu kho.

## Mục Tiêu

Trang Lịch sử phiếu kho dùng để xem danh sách phiếu nhập/xuất đã tạo. Người dùng bấm vào một phiếu để mở Chi tiết phiếu kho. UI mới cần dễ đọc, có đường quay lại danh sách rõ ràng và phù hợp với luồng kiểm tra chứng từ.

## Route Và Template Dự Kiến

- Danh sách phiếu: `GET /documents`
- Chi tiết phiếu: `GET /documents/{document_id}`
- Template danh sách: `app/templates/documents.html`
- Template chi tiết: `app/templates/document_detail.html`
- Legacy tham chiếu:
  - `app/templates/legacy/documents.html`
  - `app/templates/legacy/document_detail.html`

## Layout Trang Danh Sách

### Header Trang

- Tiêu đề: `Lịch sử phiếu kho`.
- Có thể bố trí vùng filter/tìm kiếm dự phòng trong thiết kế nếu cần mở rộng sau.

### Bảng Danh Sách Phiếu

Bảng là vùng chính.

Cột đề xuất:

- `ID`
- `Loại phiếu`
- `Ngày`
- `Khu vực`
- `Diễn giải`
- `Tạo lúc`
- Cột thao tác hoặc click row để xem chi tiết

### Trạng Thái Rỗng

- Nếu chưa có phiếu kho, hiển thị empty state tiếng Việt: `Chưa có phiếu kho`.

## Hành Vi Trang Danh Sách

- Hiển thị danh sách phiếu từ mới đến cũ theo dữ liệu service trả về.
- Người dùng bấm vào một phiếu hoặc nút `Xem` để mở chi tiết phiếu.
- Trang danh sách dùng route `GET /documents`.

## Layout Trang Chi Tiết Phiếu

### Header Trang

- Tiêu đề: `Chi tiết phiếu #ID`.
- Có nút `Quay lại lịch sử phiếu`.

### Vùng Thông Tin Phiếu

Hiển thị thông tin chính:

- `Loại`
- `Ngày`
- `Khu vực`
- `Nhân viên`
- `Diễn giải`
- `Ghi chú`

### Vùng Dòng Hàng

Bảng dòng hàng gồm:

- `Mã hàng`
- `Tên hàng hóa`
- `Đơn vị`
- `Số lượng`
- `Ghi chú`

## Hành Vi Trang Chi Tiết

- Mở từ danh sách phiếu kho.
- Người dùng có thể quay lại danh sách bằng nút `Quay lại lịch sử phiếu`.
- Trang chi tiết chỉ phục vụ xem thông tin phiếu.

## Quy Tắc Nghiệp Vụ

- Route `/documents` gọi service liệt kê phiếu kho.
- Route `/documents/{document_id}` gọi service lấy chi tiết phiếu kho.
- Danh sách phiếu chỉ hiển thị dữ liệu đã ghi nhận từ phiếu nhập/xuất.
- Chi tiết phiếu hiển thị metadata phiếu và toàn bộ dòng hàng của phiếu.
- Trang này không cung cấp thao tác thêm, sửa hoặc xoá phiếu.

## Kiểm Tra Thủ Công

- Tạo phiếu nhập/xuất.
- Mở `/documents`.
- Kiểm tra phiếu mới xuất hiện trong danh sách.
- Bấm vào phiếu để xem chi tiết.
- Kiểm tra thông tin header phiếu và dòng hàng.
- Bấm `Quay lại lịch sử phiếu` để quay lại danh sách.
- Kiểm tra empty state khi chưa có phiếu.

## Việc Cần Làm Khi Triển Khai

- Thiết kế lại `documents.html` theo template mới.
- Thiết kế lại `document_detail.html` theo template mới.
- Quyết định click row hay nút `Xem`; nếu dùng cả hai thì phải rõ ràng.
- Bổ sung route/template smoke test sau khi UI mới ổn định.
