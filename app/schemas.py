from datetime import UTC, datetime

from pydantic import BaseModel, Field, field_validator


class FiltersBase(BaseModel):
    oil_id: list[str] | None = None
    delivery_type_id: list[str] | None = None
    delivery_basis_id: list[str] | None = None


class PeriodBase(BaseModel):
    start_date: datetime = Field(..., lt=datetime.now(tz=UTC))
    end_date: datetime

    @field_validator("end_date")
    @classmethod
    def check_start_date(cls, val: datetime, values: dict) -> datetime | ValueError:
        if val < values.data["start_date"]:
            msg = "Конечная дата должна быть раньше начальной"
            raise ValueError(msg)
        return val
