from typing import Optional
from fastapi import Query
from .schemas import FiltersBase


def get_filters(
        oil_id: Optional[list[str]] = Query(None),
        delivery_type_id: Optional[list[str]] = Query(None),
        delivery_basis_id: Optional[list[str]] = Query(None),
):
    return FiltersBase(
        oil_id=oil_id,
        delivery_type_id=delivery_type_id,
        delivery_basis_id=delivery_basis_id,
    )
