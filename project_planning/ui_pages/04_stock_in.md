# Nhập kho

## Trạng Thái

Đã tạo kế hoạch chi tiết cho trang Nhập kho.

## Mục Tiêu

Trang Nhập kho dùng để tạo phiếu nhập nhiều dòng sản phẩm vào một khu vực kho. UI mới cần trình bày thông tin phiếu rõ ràng, cho phép thêm/xoá dòng hàng thuận tiện, kiểm tra trước khi lưu và hiển thị lỗi nghiệp vụ bằng tiếng Việt.

## Route Và Template Dự Kiến

- Route GET: `/stock/IN`
- Route POST: `/stock/IN`
- Template triển khai: `app/templates/stock_form.html`
- Legacy tham chiếu: `app/templates/legacy/stock_form.html`

## Layout Đề Xuất

### Header Trang

- Tiêu đề: `Nhập kho`.
- Có mô tả ngắn hoặc subtitle nếu cần: tạo phiếu nhập hàng vào kho.

### Vùng Thông Tin Phiếu

Hiển thị phía trên danh sách dòng hàng, gồm:

- `Ngày`
- `Khu vực`
- `Diễn giải`
- `Nhân viên đề xuất`
- `Ghi chú`

Cách thể hiện nên là form gọn, chia cột rõ ràng, không chiếm quá nhiều chiều cao.

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

### Vùng Hành Động

- Nút chính: `Lưu phiếu`.
- Có confirm dialog trước khi lưu:
  - Nội dung: `Bạn có chắc muốn lưu phiếu này?`
  - Có `OK` và `Cancel`.

## Hành Vi

- Người dùng chọn ngày, khu vực và nhập thông tin phiếu.
- Người dùng bấm `Thêm sản phẩm` để thêm dòng hàng.
- Mỗi dòng chọn sản phẩm, nhập số lượng và ghi chú dòng.
- Có thể xoá dòng hàng trước khi lưu.
- Submit phiếu gửi về `POST /stock/IN`.
- Service tiếp tục validate:
  - Loại phiếu hợp lệ.
  - Có ít nhất một dòng hàng.
  - Khu vực active.
  - Sản phẩm tồn tại và active.
  - Số lượng lớn hơn 0.
- Nếu lỗi nghiệp vụ, render lại trang với alert lỗi tiếng Việt.
- Nếu thành công, redirect về lịch sử phiếu kho.

## Quy Tắc Nghiệp Vụ

- Route xử lý tạo phiếu gọi service `create_stock_document`.
- Dữ liệu dòng hàng được map vào DTO `StockLineData`.
- Loại phiếu gửi vào service là `IN`.
- Các dòng trống hoặc số lượng không hợp lệ được service trả lỗi nghiệp vụ.
- Phiếu hợp lệ làm tăng tồn kho tại khu vực được chọn.

## Kiểm Tra Thủ Công

- Mở `/stock/IN`.
- Kiểm tra ban đầu chưa có dòng sản phẩm.
- Bấm `Thêm sản phẩm`, dòng mới xuất hiện.
- Thêm nhiều dòng, xoá một dòng.
- Lưu khi chưa có dòng và kiểm tra lỗi.
- Lưu phiếu nhập hợp lệ và kiểm tra redirect về lịch sử phiếu.
- Kiểm tra tồn kho/báo cáo tăng đúng sau nhập.

## Việc Cần Làm Khi Triển Khai

- Thiết kế lại `stock_form.html` cho document type `IN`.
- Có thể dùng chung template với Xuất kho nếu title, action, document type và wording được truyền rõ theo loại phiếu.
- Kiểm tra lại `app/static/js/app.js` cho thêm/xoá dòng.
- Bổ sung route/template smoke test sau khi UI mới ổn định.
