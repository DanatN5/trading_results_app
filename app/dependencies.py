from typing import Optional
from fastapi import Query
from .schemas import FiltersBase
from .redis_config import redis_client
from .database import AsyncSessionLocal


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


async def get_redis():
    return redis_client


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session