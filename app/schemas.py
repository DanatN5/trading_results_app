from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime



class FiltersBase(BaseModel):
    oil_id: Optional[list[str]] = None
    delivery_type_id: Optional[list[str]] = None
    delivery_basis_id: Optional[list[str]] = None


class PeriodBase(BaseModel):
    start_date: datetime = Field(..., lt=datetime.now())
    end_date: datetime

    @field_validator('end_date')
    def check_start_date(cls, val, values):
        if val < values.data.get("start_date"):
            raise ValueError("Конечная дата должна быть раньше начальной")
        return val
