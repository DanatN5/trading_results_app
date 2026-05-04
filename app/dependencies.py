
from asyncio import AsyncGenerator

from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache_storage import CacheStorage, RedisCacheStorage
from app.database import AsyncSessionLocal
from app.redis_config import redis_client
from app.schemas import FiltersBase


def get_filters(
    oil_id: list[str] | None = Query(None),
    delivery_type_id: list[str] | None = Query(None),
    delivery_basis_id: list[str] | None = Query(None),
) -> FiltersBase:
    return FiltersBase(
        oil_id=oil_id,
        delivery_type_id=delivery_type_id,
        delivery_basis_id=delivery_basis_id,
    )


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


def get_cache_storage() -> CacheStorage:
    return RedisCacheStorage(redis_client)
