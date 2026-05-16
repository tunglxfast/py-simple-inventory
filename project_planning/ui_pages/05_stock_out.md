# Xuất kho

## Trạng Thái

Đã tạo kế hoạch chi tiết cho trang Xuất kho.

## Mục Tiêu

Trang Xuất kho dùng để tạo phiếu xuất nhiều dòng sản phẩm khỏi một khu vực kho. UI mới cần giúp người dùng nhập phiếu nhanh, nhìn rõ các dòng sản phẩm, xác nhận trước khi lưu và nhận lỗi rõ ràng khi số lượng xuất vượt tồn.

## Route Và Template Dự Kiến

- Route GET: `/stock/OUT`
- Route POST: `/stock/OUT`
- Template triển khai: `app/templates/stock_form.html`
- Legacy tham chiếu: `app/templates/legacy/stock_form.html`

## Layout Đề Xuất

### Header Trang

- Tiêu đề: `Xuất kho`.
- Có mô tả ngắn hoặc subtitle nếu cần: tạo phiếu xuất hàng khỏi kho.

### Vùng Thông Tin Phiếu

Hiển thị phía trên danh sách dòng hàng, gồm:

- `Ngày`
- `Khu vực`
- `Diễn giải`
- `Nhân viên đề xuất`
- `Ghi chú`

### Vùng Dòng Hàng

- Bảng dòng hàng là vùng chính.
- Không render sẵn dòng sản phẩm khi mới mở trang.
- Có nút `Thêm sản phẩm`.
- Khi bấm `Thêm sản phẩm`, thêm một dòng hàng mới.
- Nút `Thêm sản phẩm` nằm dưới các dòng hàng đã thêm.

Cột bảng:

- `Mã hàng / Sản phẩm`
- `Số lượng`
- `Ghi chú`
- Cột thao tác xoá dòng

Ghi chú cho template mới:

- Nếu có đủ dữ liệu tồn kho ở frontend, có thể hiển thị số tồn đang có bên cạnh sản phẩm hoặc trong cột phụ.
- Nếu chưa có dữ liệu tồn ở frontend, service vẫn là nơi kiểm tra xuất vượt tồn.

### Vùng Hành Động

- Nút chính: `Lưu phiếu`.
- Có confirm dialog trước khi lưu:
  - Nội dung: `Bạn có chắc muốn lưu phiếu này?`
  - Có `OK` và `Cancel`.

## Hành Vi

- Người dùng chọn ngày, khu vực và nhập thông tin phiếu.
- Người dùng thêm một hoặc nhiều dòng sản phẩm.
- Có thể xoá dòng hàng trước khi lưu.
- Submit phiếu gửi về `POST /stock/OUT`.
- Service tiếp tục validate:
  - Loại phiếu hợp lệ.
  - Có ít nhất một dòng hàng.
  - Khu vực active.
  - Sản phẩm tồn tại và active.
  - Số lượng lớn hơn 0.
  - Không xuất vượt tồn kho.
- Nếu lỗi nghiệp vụ, render lại trang với alert lỗi tiếng Việt.
- Nếu thành công, redirect về lịch sử phiếu kho.

## Quy Tắc Nghiệp Vụ

- Route xử lý tạo phiếu gọi service `create_stock_document`.
- Dữ liệu dòng hàng được map vào DTO `StockLineData`.
- Loại phiếu gửi vào service là `OUT`.
- Service kiểm tra khu vực active, sản phẩm active, số lượng lớn hơn 0 và tồn kho đủ để xuất.
- Phiếu hợp lệ làm giảm tồn kho tại khu vực được chọn.

## Kiểm Tra Thủ Công

- Mở `/stock/OUT`.
- Kiểm tra ban đầu chưa có dòng sản phẩm.
- Bấm `Thêm sản phẩm`, dòng mới xuất hiện.
- Thử xuất số lượng hợp lệ.
- Thử xuất vượt tồn và kiểm tra alert lỗi.
- Thử xuất sản phẩm inactive nếu có dữ liệu test phù hợp.
- Lưu phiếu xuất hợp lệ và kiểm tra redirect về lịch sử phiếu.
- Kiểm tra tồn kho/báo cáo giảm đúng sau xuất.

## Việc Cần Làm Khi Triển Khai

- Thiết kế lại `stock_form.html` cho document type `OUT`.
- Có thể dùng chung template với Nhập kho nếu title, action, document type và wording được truyền rõ theo loại phiếu.
- Cân nhắc hiển thị số tồn đang có khi chọn sản phẩm.
- Bổ sung route/template smoke test sau khi UI mới ổn định.
