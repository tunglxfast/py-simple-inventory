from sqlalchemy.orm import Session

from app.repositories import product_repository
from app.services.exceptions import BusinessError


def list_products(db: Session, include_inactive: bool = False, search: str | None = None):
    return product_repository.list_products(db, include_inactive=include_inactive, search=search)


def list_products_with_stock(db: Session, include_inactive: bool = False, search: str | None = None):
    return product_repository.list_products_with_stock(db, include_inactive=include_inactive, search=search)


def create_product(db: Session, code: str, name: str, unit: str, note: str | None = None):
    validate_product_input(code, name, unit)
    existing = product_repository.get_by_code(db, code.strip())
    if existing:
        raise_duplicate_product_code(existing.is_active)
    product = product_repository.create_product(db, code, name, unit, note)
    db.commit()
    return product


def update_product(
    db: Session,
    product_id: int,
    code: str,
    name: str,
    unit: str,
    note: str | None,
    is_active: bool | None = None,
):
    # Product update currently allows changing code, name, unit, note, and active status.
    # Code/name/unit remain required; code must stay unique across active and inactive products.
    validate_product_input(code, name, unit)
    product = product_repository.get_product(db, product_id)
    if not product:
        raise BusinessError("Không tìm thấy sản phẩm.")
    existing = product_repository.get_by_code(db, code.strip())
    if existing and existing.id != product_id:
        raise_duplicate_product_code(existing.is_active)
    product_repository.update_product(db, product, code, name, unit, note, is_active)
    db.commit()
    return product


def delete_product(db: Session, product_id: int):
    product = product_repository.get_product(db, product_id)
    if not product:
        raise BusinessError("Không tìm thấy sản phẩm.")
    product_repository.deactivate_product(db, product)
    db.commit()
    return product


def validate_product_input(code: str, name: str, unit: str) -> None:
    if not code.strip():
        raise BusinessError("Mã hàng không được để trống.")
    if not name.strip():
        raise BusinessError("Tên hàng không được để trống.")
    if not unit.strip():
        raise BusinessError("Đơn vị tính không được để trống.")


def raise_duplicate_product_code(is_active: bool) -> None:
    if is_active:
        raise BusinessError("Mã hàng đã tồn tại.")
    raise BusinessError("Mã hàng đã bị ngưng hoạt động. Bật Xem inactive để cập nhật lại sản phẩm.")
