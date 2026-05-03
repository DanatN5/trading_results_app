import json
from datetime import datetime

from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache_storage import CacheStorage, get_date_for_prefix, get_ttl
from app.dependencies import get_cache_storage, get_db, get_filters
from app.helpers import get_query, to_dict
from app.models import TradingResults
from app.schemas import FiltersBase, PeriodBase

router = APIRouter()

CacheDep = Annotated[CacheStorage, Depends(get_cache_storage)]
DbDep = Annotated[AsyncSession, Depends(get_db)]

@router.get("/trading_days")
async def get_last_trading_dates(
    db: DbDep,
    cache: CacheDep,
    days_count: int = 0,
) -> list[str]:

    params = days_count
    cache_key = cache.get_key("days", params)

    cached = await cache.get_cache(cache_key)
    if cached:
        return cached

    query = (
        select(TradingResults.date)
        .distinct()
        .order_by(desc(TradingResults.date))
    )
    if days_count:
        query = query.limit(days_count)
    dates = await db.execute(query)
    results = dates.scalars().all()
    data = [date.strftime("%Y-%m-%dT%H:%M") for date in results]

    await cache.set_cache(cache_key, json.dumps(data), ex=get_ttl())

    return data


@router.get("/get_trading_results")
async def get_trading_results(
    db: DbDep,
    cache: CacheDep,
    filters: FiltersBase = Depends(get_filters),
) -> list[dict]:
    params = filters.model_dump(exclude_none=True)
    cache_key = cache.get_key("results", params)

    cached = await cache.get_cache(cache_key)
    if cached:
        return cached

    query = select(TradingResults)
    if filters:
        query = get_query(query, filters)

    result = await db.execute(query)
    results = result.scalars().all()
    data = [to_dict(i) for i in results]

    await cache.set_cache(cache_key, json.dumps(data), ex=get_ttl())

    return data


@router.post("/get_dynamics")
async def get_dynamics(
    peirod: PeriodBase,
    cache: CacheDep,
    db: DbDep,
    filters: FiltersBase = Depends(get_filters),
) -> list[dict]:
    
    params = filters.model_dump(exclude_none=True)
    prefix = get_date_for_prefix(peirod.model_dump(exclude_none=True))
    cache_key = cache.get_key(prefix, params)

    cached = await cache.get_cache(cache_key)
    if cached:
        print('fdf')
        return cached

    query = select(TradingResults).where(
        TradingResults.date.between(peirod.start_date, peirod.end_date)
    )
    if filters:
        query = get_query(query, filters)

    result = await db.execute(query)
    dynamics = result.scalars().all()

    data = [to_dict(i) for i in dynamics]

    await cache.set_cache(cache_key, json.dumps(data), ex=get_ttl())

    return data
