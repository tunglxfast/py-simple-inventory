from datetime import date
from enum import StrEnum

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class StockDocumentType(StrEnum):
    IN = "IN"
    OUT = "OUT"
    ADJUST_IN = "ADJUST-IN"
    ADJUST_OUT = "ADJUST-OUT"


class StockDocument(TimestampMixin, Base):
    __tablename__ = "stock_documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    date: Mapped[date | None] = mapped_column(Date, nullable=True)
    area_id: Mapped[int | None] = mapped_column(ForeignKey("areas.id"), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    proposed_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    area = relationship("Area")
    lines = relationship("StockDocumentLine", back_populates="document", cascade="all, delete-orphan")


class StockDocumentLine(TimestampMixin, Base):
    __tablename__ = "stock_document_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("stock_documents.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    document = relationship("StockDocument", back_populates="lines")
    product = relationship("Product")
