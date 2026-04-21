from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class FiltersBase(BaseModel):
    oil_id: Optional[str] = None
    delivery_type_id: Optional[int] = None
    delivery_basis_id: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None



# class DynamicsFilterBase(FiltersBase):
#     start_date: date
#     end_date: date
