# Chuẩn Code

## Vai Trò Tài Liệu

Tài liệu này là source of truth cho quy ước viết code, naming, phân lớp, UI convention, testing, và frontend framework policy. Phạm vi sản phẩm nằm trong `project_rules/PROJECT_PLAN.md`; kiến trúc kỹ thuật nằm trong `project_rules/ARCHITECTURE.md`.

## Ngôn Ngữ Và Naming

- Code, database, model, schema, route, service, repository, function, và variable dùng tiếng Anh.
- UI label, button, message, form text, và validation text dùng tiếng Việt có dấu.
- Tên bảng dùng số nhiều, snake_case: `products`, `stock_documents`.
- Tên cột dùng snake_case: `created_at`, `is_active`, `password_hash`.
- Tên Python module dùng snake_case.
- Tên class dùng PascalCase.
- Tên function và variable dùng snake_case.

## Python Và Layering

- Dùng type hints cho service, repository, schema, và helper quan trọng.
- Route handler chỉ điều phối request/response, validate input mức route, và gọi service.
- Business logic nằm trong `app/services/`.
- Tất cả query SQLAlchemy nằm trong `app/repositories/`.
- Route, service, template helper, và module khác không query SQLAlchemy trực tiếp.
- Database access đi qua SQLAlchemy session.
- Không viết SQL thô nếu SQLAlchemy có thể diễn đạt rõ ràng và dễ bảo trì.
- Dùng `logging` chuẩn của Python, không dùng `print` cho app logic.
- Lỗi nghiệp vụ nên có exception rõ ràng để route hiển thị thông báo tiếng Việt phù hợp.
- Không trộn logic tính tồn kho vào template.

## FastAPI, Templates Và Frontend

- UI page routes render Jinja2 templates trong v1.
- Form submit routes nên redirect sau khi xử lý thành công để tránh submit lại khi refresh.
- Template nên kế thừa layout chung.
- Sidebar, flash messages, table controls, và form controls nên được tách thành partial nếu bị lặp lại nhiều.
- Message hiển thị cho người dùng phải ngắn gọn, rõ ràng, bằng tiếng Việt có dấu.
- Mặc định dùng Jinja2, HTML/CSS thuần, Bootstrap, và JavaScript nhỏ.
- Có thể sử dụng frontend framework nếu nó làm cấu trúc tổng thể đơn giản hơn rõ rệt, nhưng phải có sự đồng ý của chủ dự án trước khi thêm vào stack.

## Database Và Migrations

- Mọi thay đổi schema phải có Alembic migration.
- Không sửa schema trực tiếp trong database local rồi bỏ qua migration.
- Tất cả cột dạng text phải hỗ trợ Unicode tiếng Việt.
- Không hard delete dữ liệu nghiệp vụ trong UI nếu chức năng đã được định nghĩa là inactive.
- Quantity trong phiếu nhập/xuất/điều chỉnh phải validate lớn hơn 0 ở schema/service.
- Input số lượng tồn mong muốn trong chức năng điều chỉnh tồn kho được phép bằng 0 nhưng không được âm.
- Constraint quan trọng phải được thể hiện ở model/migration, không chỉ validate ở UI.
- Transaction tạo phiếu kho phải đảm bảo header và lines được lưu cùng nhau hoặc rollback cùng nhau.

## UI Standards

- Dùng Bootstrap và CSS thuần theo mặc định.
- Không thêm frontend framework khác nếu chưa được chủ dự án đồng ý.
- Layout desktop-first, nhưng không được vỡ trên màn hình nhỏ.
- Màu chủ đạo: trắng, xanh lá nhạt, xám nhạt cho border/background phụ.
- Bảng dữ liệu phải dễ đọc, có header rõ, căn lề hợp lý, và trạng thái rỗng nếu chưa có dữ liệu.
- Form nhập/xuất kho phải có validation rõ ràng.
- Form điều chỉnh tồn kho phải hiển thị tất cả sản phẩm với số lượng mặc định bằng tồn hiện tại và chặn số âm trước khi submit.
- Nút hành động chính cần nổi bật, nhưng không làm UI quá nặng.
- Search/filter nên nằm gần bảng dữ liệu liên quan.
- Các page danh sách cần có trạng thái loading/rỗng/lỗi phù hợp với server-rendered UI.
- UI không hiển thị text kỹ thuật nội bộ như tên model, exception raw, stack trace.

## Testing

- Mỗi service nghiệp vụ chính cần có unit test.
- Repository có query phức tạp hoặc dùng cho báo cáo cần có test riêng.
- Route/page quan trọng cần có smoke test render thành công.
- Test cần bao phủ:
  - Tạo/sửa/xoá sản phẩm bằng inactive.
  - Tạo/sửa/ẩn khu vực.
  - Nhập kho làm tăng tồn.
  - Xuất kho hợp lệ làm giảm tồn.
  - Xuất kho vượt tồn bị chặn.
  - Báo cáo xuất - nhập - tồn tính đúng.
  - Xuất Excel tạo file hợp lệ.
  - Điều chỉnh tồn kho tạo `ADJUST-IN` khi số lượng mong muốn lớn hơn tồn hiện tại.
  - Điều chỉnh tồn kho tạo `ADJUST-OUT` khi số lượng mong muốn nhỏ hơn tồn hiện tại.
  - Điều chỉnh tồn kho không tạo dòng điều chỉnh khi số lượng mong muốn bằng tồn hiện tại.
  - Điều chỉnh tồn kho với input 0, tồn sản phẩm kiểm tra đã về 0.
  - Điều chỉnh tồn kho từ chối số lượng âm.
  - Luồng kiểm tra database khi mở app: đã có DB thì kết nối, chưa có DB thì hiện setup và tạo DB.
- Sau mỗi module UI, chạy test trên MacBook và để người dùng manual check trước khi sang module tiếp theo.

## Documentation

- Khi có quyết định mới làm thay đổi phạm vi sản phẩm, cập nhật `project_rules/PROJECT_PLAN.md`.
- Khi có quyết định mới làm thay đổi kiến trúc, data flow, database, repositories, hoặc đóng gói, cập nhật `project_rules/ARCHITECTURE.md`.
- Khi có quyết định mới làm thay đổi coding convention, UI convention, test policy, hoặc frontend framework policy, cập nhật `project_rules/CODING_STANDARDS.md`.
