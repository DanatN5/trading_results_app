import json
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache_storage import CacheStorage, get_date_for_prefix, get_key, get_ttl
from app.dependencies import get_cache_storage, get_db, get_filters, get_repo
from app.helpers import get_query
from app.models import TradingResults
from app.schemas import FiltersBase, IntervalBase
from app.repository import Repository

router = APIRouter()

CacheDependency = Annotated[CacheStorage, Depends(get_cache_storage)]
Db = Annotated[AsyncSession, Depends(get_db)]
FiltersDependency = Annotated[FiltersBase, Depends(get_filters)]
DataBaseDependency = Annotated[Repository, Depends(get_repo)]


@router.get("/trading_days")
async def get_last_trading_dates(
    repo: DataBaseDependency,
    cache: CacheDependency,
    days_count: int = 0,
) -> list[str]:

    cache_key = get_key("days", days_count)

    cached = await cache.get_cache(cache_key)
    if cached:
        return cached

    data = await repo.get_dates(days_count)

    await cache.set_cache(cache_key, json.dumps(data), ex=get_ttl())

    return data


@router.get("/get_trading_results")
async def get_trading_results(
    repo: DataBaseDependency,
    cache: CacheDependency,
    filters: FiltersDependency,
) -> list[dict]:
    params = filters.model_dump(exclude_none=True)
    cache_key = get_key("results", params)

    cached = await cache.get_cache(cache_key)
    if cached:
        return cached

    data = await repo.get(filters)

    await cache.set_cache(cache_key, json.dumps(data), ex=get_ttl())

    return data


@router.post("/get_dynamics")
async def get_dynamics(
    interval: IntervalBase,
    cache: CacheDependency,
    repo: DataBaseDependency,
    filters: FiltersDependency,
) -> list[dict]:

    params = filters.model_dump(exclude_none=True)
    prefix = get_date_for_prefix(interval.model_dump(exclude_none=True))
    cache_key = get_key(prefix, params)

    cached = await cache.get_cache(cache_key)
    if cached:
        return cached

    data = await repo.get(filters, interval)

    await cache.set_cache(cache_key, json.dumps(data), ex=get_ttl())

    return data
