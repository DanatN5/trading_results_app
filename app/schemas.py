from datetime import UTC, datetime

from pydantic import BaseModel, Field, model_validator


class FiltersBase(BaseModel):
    oil_id: list[str] | None = None
    delivery_type_id: list[str] | None = None
    delivery_basis_id: list[str] | None = None


class IntervalBase(BaseModel):
    start_date: datetime = Field(..., lt=datetime.now(tz=UTC))
    end_date: datetime

    @model_validator(mode="after")
    def check_dates(self):
        if self.start_date > self.end_date:
            msg = "Конечная дата должна быть раньше начальной"
            raise ValueError(msg)
        return self


class ResultsBase(BaseModel):
    id: int
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: int
    total: int
    count: int
    date: str
    created_on: str
    updated_on: str