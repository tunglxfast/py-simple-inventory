# Sản phẩm

## Trạng Thái

Đã có yêu cầu UI chi tiết. Chờ triển khai template mới.

## Mục Tiêu

Trang Sản phẩm là màn hình quản lý danh sách sản phẩm, cho phép tìm kiếm, thêm, điều chỉnh và xoá sản phẩm. Giao diện bám tinh thần ảnh mẫu `project_planning/Inventory Storage Manager Pro.jpg`: thao tác rõ, bảng sản phẩm là vùng chính, các nút hành động nằm gần danh sách.

## Route Và Template Dự Kiến

- Trang danh sách: `GET /products`
- Tìm kiếm: `GET /products?search=...&include_inactive=...`
- Thêm sản phẩm:
  - Có thể dùng route hiện tại `POST /products`.
  - Cần thêm UI form riêng cho trạng thái thêm sản phẩm.
- Điều chỉnh sản phẩm:
  - Có thể dùng route hiện tại `POST /products/{product_id}/update`.
  - Cần thêm UI form riêng cho trạng thái điều chỉnh sản phẩm.
- Xoá sản phẩm: `POST /products/{product_id}/delete`

Ghi chú: hiện route/template đang gom thêm/sửa/xoá trong một trang. Template mới sẽ tổ chức lại trải nghiệm theo các trạng thái màn hình rõ hơn.

## Layout Trang Danh Sách

### Vùng Tìm Kiếm

- Nằm ở phía trên, căn giữa theo chiều ngang.
- Có ô nhập tìm kiếm.
- Có nút `Tìm kiếm` màu xanh dương.
- Có nút `Reset` màu xanh dương.
- Bên dưới thanh tìm kiếm có checkbox:
  - Label: `Bao gồm sản phẩm inactive`.
  - Khi check, danh sách bao gồm cả sản phẩm inactive.

### Vùng Nút Hành Động

Nằm phía dưới vùng tìm kiếm, gồm các nút:

- `Thêm sản phẩm`
- `Điều chỉnh sản phẩm`
- `Xoá sản phẩm`

Các nút hành động áp dụng trên sản phẩm đang được đánh dấu trong danh sách, trừ `Thêm sản phẩm`.

### Vùng Danh Sách Sản Phẩm

Nằm phía dưới vùng nút hành động.

Bảng sản phẩm có các cột:

- `Mã sản phẩm`
- `Tên sản phẩm`
- `Số lượng`
- `Đơn vị tính`

Danh sách phải có một sản phẩm đang được đánh dấu/selected.

## Hành Vi

### Tìm Kiếm

- Người dùng có thể tìm bằng tên sản phẩm hoặc mã sản phẩm.
- Bấm `Tìm kiếm` sẽ lọc danh sách sản phẩm.
- Nhấn Enter trong ô tìm kiếm cũng nên thực hiện tìm kiếm.
- Bấm `Reset` sẽ xoá nội dung tìm kiếm, bỏ filter liên quan và quay về danh sách mặc định.
- Checkbox `Bao gồm sản phẩm inactive` quyết định có hiển thị sản phẩm inactive hay không.

### Chọn Sản Phẩm Trong Danh Sách

- Mặc định đánh dấu sản phẩm đầu tiên trong danh sách.
- Người dùng có thể chọn một dòng sản phẩm khác.
- Thay đổi vị trí con trỏ sang các field khác (ví dụ: Tìm kiếm) trong trang này không thay đổi vị đánh dấu sản phẩm hiện tại.
- Dòng đang chọn phải có trạng thái visual rõ ràng.
- Nếu danh sách rỗng, các nút `Điều chỉnh sản phẩm` và `Xoá sản phẩm` nên ở trạng thái disabled.

### Thêm Sản Phẩm

- Bấm `Thêm sản phẩm` sẽ hiện trang/trạng thái thêm sản phẩm.
- Form thêm sản phẩm dùng các thông tin cần thiết cho sản phẩm.
- Có nút `Cancel` ở dưới để quay lại danh sách sản phẩm.
- Không thêm số lượng ở trang này, sản phẩm mới thêm mặc định số lượng là 0.
- Khi thêm thành công, quay lại danh sách và hiển thị sản phẩm mới theo danh sách mặc định.

### Điều Chỉnh Sản Phẩm

- Bấm `Điều chỉnh sản phẩm` sẽ hiện trang/trạng thái form sản phẩm.
- Form được điền sẵn thông tin của sản phẩm đang được đánh dấu trong danh sách phía dưới.
- Danh sách sản phẩm luôn có chọn 1 sản phẩm. Trường hợp không có sản phẩm nào thì khi gọi tới trang này trả lại về Trang danh sách sản phẩm.
- Có nút `Cancel` ở dưới để quay lại danh sách sản phẩm.
- Khi lưu thành công, quay lại danh sách.

### Xoá Sản Phẩm

- Bấm `Xoá sản phẩm` sẽ hiện dialog xác nhận:
  - Nội dung: `Bạn có chắc muốn xoá sản phẩm này không?`
  - Có lựa chọn `OK` và `Cancel`.
- Chọn `OK` thì gửi request xoá sản phẩm.
- Chọn `Cancel` thì đóng dialog và không thay đổi dữ liệu.
- Xoá sản phẩm vẫn là chuyển sang inactive, không hard delete.

## Dữ Liệu Cần Hiển Thị

Mỗi dòng sản phẩm cần tối thiểu:

- `code` -> `Mã sản phẩm`
- `name` -> `Tên sản phẩm`
- `stock` hoặc tồn tính từ giao dịch -> `Số lượng`
- `unit` -> `Đơn vị tính`

Ghi chú: route hiện tại `product_service.list_products()` chưa trả tồn kho. Khi triển khai template mới, cần lấy thêm tồn kho từ service phù hợp hoặc tạo view model cho trang sản phẩm.

## Kiểm Tra Thủ Công

- Mở trang Sản phẩm.
- Kiểm tra ô tìm kiếm nằm top center.
- Tìm theo mã sản phẩm.
- Tìm theo tên sản phẩm.
- Reset filter.
- Bật/tắt `Bao gồm sản phẩm inactive`.
- Kiểm tra mặc định chọn dòng sản phẩm đầu tiên.
- Chọn dòng khác và bấm `Điều chỉnh sản phẩm`.
- Bấm `Cancel` từ form thêm/điều chỉnh để quay lại danh sách.
- Xoá sản phẩm và kiểm tra dialog OK/Cancel.
- Sau xoá, bật include inactive để kiểm tra sản phẩm vẫn còn nhưng inactive.

## Việc Cần Làm Khi Triển Khai

- Thiết kế lại `products.html` theo layout mới.
- Quyết định route/view cho trạng thái thêm và điều chỉnh sản phẩm.
- Bổ sung dữ liệu tồn kho vào danh sách sản phẩm.
- Bổ sung JavaScript chọn dòng sản phẩm nếu cần.
- Bổ sung/điều chỉnh route tests cho trang sản phẩm sau khi template mới ổn định.
