from pydantic import BaseModel, Field


class ProductInput(BaseModel):
    code: str = Field(min_length=1)
    name: str = Field(min_length=1)
    unit: str = Field(min_length=1)
    note: str | None = None

