from pydantic import BaseModel, Field


class AreaInput(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None
    is_active: bool = True

