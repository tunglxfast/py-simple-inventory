from datetime import date
from typing import Iterable

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session, selectinload

from app.models.product import Product
from app.models.stock import StockDocument, StockDocumentLine, StockDocumentType
from app.schemas.dto import StockLineData

IN_TYPES = (StockDocumentType.IN.value, StockDocumentType.ADJUST_IN.value)
OUT_TYPES = (StockDocumentType.OUT.value, StockDocumentType.ADJUST_OUT.value)


def create_document(
    db: Session,
    document_type: str,
    lines: Iterable[StockLineData],
    document_date: date | None = None,
    area_id: int | None = None,
    description: str | None = None,
    proposed_by: str | None = None,
    note: str | None = None,
) -> StockDocument:
    document = StockDocument(
        type=document_type,
        date=document_date,
        area_id=area_id,
        description=description or None,
        proposed_by=proposed_by or None,
        note=note or None,
    )
    for line in lines:
        document.lines.append(
            StockDocumentLine(
                product_id=line.product_id,
                quantity=line.quantity,
                note=line.note or None,
            )
        )
    db.add(document)
    db.flush()
    return document


def list_documents(db: Session) -> list[StockDocument]:
    stmt = (
        select(StockDocument)
        .options(selectinload(StockDocument.lines), selectinload(StockDocument.area))
        .order_by(StockDocument.created_at.desc(), StockDocument.id.desc())
    )
    return list(db.scalars(stmt))


def get_document(db: Session, document_id: int) -> StockDocument | None:
    stmt = (
        select(StockDocument)
        .where(StockDocument.id == document_id)
        .options(selectinload(StockDocument.lines).selectinload(StockDocumentLine.product))
    )
    return db.scalar(stmt)


def get_stock_by_product_ids(db: Session, product_ids: Iterable[int]) -> dict[int, int]:
    ids = list(product_ids)
    if not ids:
        return {}
    signed_quantity = case(
        (StockDocument.type.in_(IN_TYPES), StockDocumentLine.quantity),
        (StockDocument.type.in_(OUT_TYPES), -StockDocumentLine.quantity),
        else_=0,
    )
    stmt = (
        select(StockDocumentLine.product_id, func.coalesce(func.sum(signed_quantity), 0))
        .join(StockDocument, StockDocument.id == StockDocumentLine.document_id)
        .where(StockDocumentLine.product_id.in_(ids))
        .group_by(StockDocumentLine.product_id)
    )
    values = {product_id: int(quantity or 0) for product_id, quantity in db.execute(stmt)}
    return {product_id: values.get(product_id, 0) for product_id in ids}


def get_all_stock(db: Session, include_inactive: bool = False) -> list[dict]:
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
    return [
        {
            "product_id": row.id,
            "code": row.code,
            "name": row.name,
            "unit": row.unit,
            "is_active": row.is_active,
            "stock": int(row.stock or 0),
        }
        for row in db.execute(stmt)
    ]


def get_inventory_report(db: Session) -> list[dict]:
    signed_in = case((StockDocument.type.in_(IN_TYPES), StockDocumentLine.quantity), else_=0)
    signed_out = case((StockDocument.type.in_(OUT_TYPES), StockDocumentLine.quantity), else_=0)
    stmt = (
        select(
            Product.code,
            Product.name,
            Product.unit,
            func.coalesce(func.sum(signed_in), 0).label("stock_in"),
            func.coalesce(func.sum(signed_out), 0).label("stock_out"),
        )
        .outerjoin(StockDocumentLine, StockDocumentLine.product_id == Product.id)
        .outerjoin(StockDocument, StockDocument.id == StockDocumentLine.document_id)
        .where(Product.is_active.is_(True))
        .group_by(Product.id)
        .order_by(Product.code)
    )
    report = []
    for row in db.execute(stmt):
        stock_in = int(row.stock_in or 0)
        stock_out = int(row.stock_out or 0)
        report.append(
            {
                "code": row.code,
                "name": row.name,
                "unit": row.unit,
                "opening": 0,
                "stock_in": stock_in,
                "stock_out": stock_out,
                "closing": stock_in - stock_out,
            }
        )
    return report
