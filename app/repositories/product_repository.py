from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.product import Product


def list_products(db: Session, include_inactive: bool = False, search: str | None = None) -> list[Product]:
    stmt = select(Product).order_by(Product.code)
    if not include_inactive:
        stmt = stmt.where(Product.is_active.is_(True))
    if search:
        pattern = f"%{search.strip()}%"
        stmt = stmt.where(or_(Product.code.ilike(pattern), Product.name.ilike(pattern)))
    return list(db.scalars(stmt))


def get_product(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)


def get_by_code(db: Session, code: str) -> Product | None:
    return db.scalar(select(Product).where(Product.code == code))


def create_product(db: Session, code: str, name: str, unit: str, note: str | None = None) -> Product:
    product = Product(code=code.strip(), name=name.strip(), unit=unit.strip(), note=note or None)
    db.add(product)
    db.flush()
    return product


def update_product(
    db: Session,
    product: Product,
    code: str,
    name: str,
    unit: str,
    note: str | None,
    is_active: bool | None = None,
) -> Product:
    product.code = code.strip()
    product.name = name.strip()
    product.unit = unit.strip()
    product.note = note or None
    if is_active is not None:
        product.is_active = is_active
    db.flush()
    return product


def deactivate_product(db: Session, product: Product) -> Product:
    product.is_active = False
    db.flush()
    return product

