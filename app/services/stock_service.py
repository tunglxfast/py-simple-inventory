from datetime import date

from sqlalchemy.orm import Session

from app.models.stock import StockDocumentType
from app.repositories import area_repository, product_repository, stock_repository
from app.services.exceptions import BusinessError


def list_documents(db: Session):
    return stock_repository.list_documents(db)


def get_document(db: Session, document_id: int):
    document = stock_repository.get_document(db, document_id)
    if not document:
        raise BusinessError("Không tìm thấy phiếu kho.")
    return document


def create_stock_document(
    db: Session,
    document_type: str,
    lines: list[dict],
    document_date: date,
    area_id: int,
    description: str | None,
    proposed_by: str | None,
    note: str | None,
):
    if document_type not in {StockDocumentType.IN.value, StockDocumentType.OUT.value}:
        raise BusinessError("Loại phiếu không hợp lệ.")
    if not lines:
        raise BusinessError("Phiếu kho phải có ít nhất một dòng hàng.")
    area = area_repository.get_area(db, area_id)
    if not area:
        raise BusinessError("Khu vực không hợp lệ.")
    if not area.is_active:
        raise BusinessError("Khu vực đã bị ngưng hoạt động.")
    normalized = normalize_lines(lines)
    ensure_active_products(db, normalized)
    if document_type == StockDocumentType.OUT.value:
        ensure_enough_stock(db, normalized)
    document = stock_repository.create_document(
        db,
        document_type,
        normalized,
        document_date=document_date,
        area_id=area_id,
        description=description,
        proposed_by=proposed_by,
        note=note,
    )
    db.commit()
    return document


def reset_inventory(db: Session, desired_quantities: dict[int, int]) -> tuple[int, int]:
    if not desired_quantities:
        return (0, 0)
    for quantity in desired_quantities.values():
        if quantity < 0:
            raise BusinessError("Số lượng tồn mong muốn không được âm.")

    product_ids = list(desired_quantities)
    for product_id in product_ids:
        product = product_repository.get_product(db, product_id)
        if not product:
            raise BusinessError(f"Không tìm thấy sản phẩm ID {product_id}.")
        if not product.is_active:
            raise BusinessError(f"Sản phẩm {format_product(product.id, product.name)} đã bị ngưng hoạt động.")

    current = stock_repository.get_stock_by_product_ids(db, product_ids)
    adjust_in_lines = []
    adjust_out_lines = []
    for product_id, desired in desired_quantities.items():
        delta = desired - current.get(product_id, 0)
        if delta > 0:
            adjust_in_lines.append({"product_id": product_id, "quantity": delta})
        elif delta < 0:
            adjust_out_lines.append({"product_id": product_id, "quantity": abs(delta)})

    if adjust_in_lines:
        stock_repository.create_document(db, StockDocumentType.ADJUST_IN.value, adjust_in_lines)
    if adjust_out_lines:
        stock_repository.create_document(db, StockDocumentType.ADJUST_OUT.value, adjust_out_lines)
    db.commit()
    return (len(adjust_in_lines), len(adjust_out_lines))


def get_stock_table(db: Session):
    return stock_repository.get_all_stock(db)


def get_inventory_report(db: Session):
    return stock_repository.get_inventory_report(db)


def normalize_lines(lines: list[dict]) -> list[dict]:
    merged: dict[int, dict] = {}
    for line in lines:
        product_id = int(line.get("product_id") or 0)
        quantity = int(line.get("quantity") or 0)
        if product_id <= 0:
            raise BusinessError("Dòng hàng có sản phẩm không hợp lệ.")
        if quantity <= 0:
            raise BusinessError("Số lượng phải lớn hơn 0.")
        if product_id not in merged:
            merged[product_id] = {"product_id": product_id, "quantity": 0, "note": line.get("note")}
        merged[product_id]["quantity"] += quantity
    return list(merged.values())


def ensure_enough_stock(db: Session, lines: list[dict]) -> None:
    stock = stock_repository.get_stock_by_product_ids(db, [line["product_id"] for line in lines])
    for line in lines:
        product = product_repository.get_product(db, line["product_id"])
        if not product:
            raise BusinessError(f"Không tìm thấy sản phẩm ID {line['product_id']}.")
        available = stock.get(line["product_id"], 0)
        if line["quantity"] > available:
            raise BusinessError(f"Sản phẩm {format_product(product.id, product.name)} không đủ tồn kho.")


def ensure_active_products(db: Session, lines: list[dict]) -> None:
    for line in lines:
        product = product_repository.get_product(db, line["product_id"])
        if not product:
            raise BusinessError(f"Không tìm thấy sản phẩm ID {line['product_id']}.")
        if not product.is_active:
            raise BusinessError(f"Sản phẩm {format_product(product.id, product.name)} đã bị ngưng hoạt động.")


def format_product(product_id: int, product_name: str) -> str:
    return f"{product_name} (ID {product_id})"
