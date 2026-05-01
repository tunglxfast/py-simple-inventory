"""Simple bilingual dictionary for UI labels."""

from __future__ import annotations

TRANSLATIONS = {
    "vi": {
        "app_title": "Warehouse Management",
        "language": "Ngôn ngữ",
        "products": "Sản phẩm",
        "import": "Nhập kho",
        "export": "Xuất kho",
        "hold": "Giữ hàng",
        "hold_manage": "Quản lý giữ hàng",
        "sales": "Bán hàng",
        "reports": "Báo cáo",
        "setup": "Thiết lập",
        "sku": "Mã hàng",
        "name": "Tên hàng",
        "unit": "ĐVT",
        "quantity": "Số lượng",
        "note": "Ghi chú",
        "save": "Lưu",
        "refresh": "Làm mới",
        "search": "Tìm",
        "code": "Mã",
        "status": "Trạng thái",
        "created_at": "Tạo lúc",
        "return_qty": "SL trả",
        "finalize": "Chốt giữ hàng",
        "from_date": "Từ ngày",
        "to_date": "Đến ngày",
        "load_report": "Xem báo cáo",
        "file": "Tệp",
        "preview": "Xem trước",
        "import_initial": "Nhập tồn đầu",
        "reset_db": "Reset DB",
        "confirm_reset": "Nhập RESET để xác nhận",
        "backup": "Sao lưu",
        "restore": "Phục hồi",
        "destination": "Thư mục đích",
    },
    "en": {
        "app_title": "Warehouse Management",
        "language": "Language",
        "products": "Products",
        "import": "Import",
        "export": "Export",
        "hold": "Hold",
        "hold_manage": "Hold Management",
        "sales": "Sales",
        "reports": "Reports",
        "setup": "Setup",
        "sku": "SKU",
        "name": "Name",
        "unit": "Unit",
        "quantity": "Quantity",
        "note": "Note",
        "save": "Save",
        "refresh": "Refresh",
        "search": "Search",
        "code": "Code",
        "status": "Status",
        "created_at": "Created At",
        "return_qty": "Return Qty",
        "finalize": "Finalize Hold",
        "from_date": "From Date",
        "to_date": "To Date",
        "load_report": "Load Report",
        "file": "File",
        "preview": "Preview",
        "import_initial": "Import Initial Stock",
        "reset_db": "Reset DB",
        "confirm_reset": "Type RESET to confirm",
        "backup": "Backup",
        "restore": "Restore",
        "destination": "Destination",
    },
}


class Translator:
    def __init__(self) -> None:
        self.language = "vi"

    def set_language(self, language: str) -> None:
        if language in TRANSLATIONS:
            self.language = language

    def t(self, key: str) -> str:
        return TRANSLATIONS[self.language].get(key, key)
