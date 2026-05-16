from sqlalchemy import case, func, or_, select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.stock import StockDocument, StockDocumentLine, StockDocumentType

IN_TYPES = (StockDocumentType.IN.value, StockDocumentType.ADJUST_IN.value)
OUT_TYPES = (StockDocumentType.OUT.value, StockDocumentType.ADJUST_OUT.value)


def list_products(db: Session, include_inactive: bool = False, search: str | None = None) -> list[Product]:
    stmt = select(Product).order_by(Product.code)
    if not include_inactive:
        stmt = stmt.where(Product.is_active.is_(True))
    if search:
        pattern = f"%{search.strip()}%"
        stmt = stmt.where(or_(Product.code.ilike(pattern), Product.name.ilike(pattern)))
    return list(db.scalars(stmt))


def list_products_with_stock(db: Session, include_inactive: bool = False, search: str | None = None) -> list[dict]:
    signed_quantity = case(
        (StockDocument.type.in_(IN_TYPES), StockDocumentLine.quantity),
        (StockDocument.type.in_(OUT_TYPES), -StockDocumentLine.quantity),
        else_=0,
    )
    stmt = (
        select(
            Product.id,
            Product.code,
            Product.name,
            Product.unit,
            Product.note,
            Product.is_active,
            func.coalesce(func.sum(signed_quantity), 0).label("stock"),
        )
        .outerjoin(StockDocumentLine, StockDocumentLine.product_id == Product.id)
        .outerjoin(StockDocument, StockDocument.id == StockDocumentLine.document_id)
        .group_by(Product.id)
        .order_by(Product.code)
    )
    if not include_inactive:
        stmt = stmt.where(Product.is_active.is_(True))
    if search:
        pattern = f"%{search.strip()}%"
        stmt = stmt.where(or_(Product.code.ilike(pattern), Product.name.ilike(pattern)))
    return [
        {
            "id": row.id,
            "code": row.code,
            "name": row.name,
            "unit": row.unit,
            "note": row.note,
            "is_active": row.is_active,
            "stock": int(row.stock or 0),
        }
        for row in db.execute(stmt)
    ]


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
