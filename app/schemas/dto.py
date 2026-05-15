from dataclasses import dataclass


@dataclass(slots=True)
class StockLineData:
    """DTO for passing stock line data between routes, services, and repositories."""

    product_id: int
    quantity: int
    note: str | None = None
