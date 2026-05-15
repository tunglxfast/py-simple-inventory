from datetime import date
from dataclasses import dataclass

from pydantic import BaseModel, Field


@dataclass(slots=True)
class StockLineData:
    """DTO for passing stock line data between routes, services, and repositories."""

    product_id: int
    quantity: int
    note: str | None = None


class StockLineInput(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    note: str | None = None


class StockDocumentInput(BaseModel):
    document_type: str
    date: date
    area_id: int
    description: str | None = None
    proposed_by: str | None = None
    note: str | None = None
    lines: list[StockLineInput]
