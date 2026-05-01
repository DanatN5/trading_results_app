import json

from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_cache_storage, get_db, get_filters
from app.helpers import (
    get_date_for_prefix,
    get_query,
    get_ttl,
    make_cache_key,
    to_dict,
)
from app.models import TradingResults
from app.schemas import FiltersBase, PeriodBase

router = APIRouter()


@router.get("/trading_days")
async def get_last_trading_dates(
    db: AsyncSession = Depends(get_db),
    days_count: int = 0,
    cache=Depends(get_cache_storage),
) -> list[str]:

    params = days_count
    print(params)
    cache_key = make_cache_key("days", params)

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

    await cache.set_cache(
        cache_key,
        json.dumps([date.strftime("%Y.%m.%d.%H:%M") for date in results]),
        ex=get_ttl(),
    )

    return results


@router.get("/get_trading_results")
async def get_trading_results(
    filters: FiltersBase = Depends(get_filters),
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_cache_storage),
) -> list[str]:
    params = filters.model_dump(exclude_none=True)
    cache_key = make_cache_key("results", params)

    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    query = select(TradingResults)
    if filters:
        query = get_query(query, filters)

    result = await db.execute(query)
    results = result.scalars().all()

    await redis.set(
        cache_key, json.dumps([to_dict(i) for i in results]), ex=get_ttl()
    )

    return results


@router.post("/get_dynamics")
async def get_dynamics(
    peirod: PeriodBase,
    filters: FiltersBase = Depends(get_filters),
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_cache_storage),
) -> list[str]:
    params = filters.model_dump(exclude_none=True)
    prefix = get_date_for_prefix(peirod.model_dump(exclude_none=True))
    cache_key = make_cache_key(prefix, params)

    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    query = select(TradingResults).where(
        TradingResults.date.between(peirod.start_date, peirod.end_date)
    )
    if filters:
        query = get_query(query, filters)

    result = await db.execute(query)
    dynamics = result.scalars().all()

    await redis.set(
        cache_key, json.dumps([to_dict(i) for i in dynamics]), ex=get_ttl()
    )

    return dynamics
