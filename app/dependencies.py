from typing import Optional

from fastapi import Query

from app.cache_storage import CacheStorage, RedisCacheStorage
from app.database import AsyncSessionLocal
from app.redis_config import redis_client
from app.schemas import FiltersBase


def get_filters(
    oil_id: Optional[list[str]] = Query(None),
    delivery_type_id: Optional[list[str]] = Query(None),
    delivery_basis_id: Optional[list[str]] = Query(None),
) -> FiltersBase:
    return FiltersBase(
        oil_id=oil_id,
        delivery_type_id=delivery_type_id,
        delivery_basis_id=delivery_basis_id,
    )


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def get_cache_storage() -> CacheStorage:
    return RedisCacheStorage(redis_client)