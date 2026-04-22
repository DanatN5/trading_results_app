from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime



class FiltersBase(BaseModel):
    oil_id: Optional[list[str]] = None
    delivery_type_id: Optional[list[str]] = None
    delivery_basis_id: Optional[list[str]] = None


# class DatesBase(BaseModel):
#     start_date: datetime = Field(..., )
#     end_date: datetime = Field(..., gt=start_date)
