import json

from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import get_db, get_filters, get_redis
from .helpers import (
    get_date_for_prefix,
    get_query,
    get_ttl,
    make_cache_key,
    to_dict,
)
from .models import TradingResults
from .schemas import FiltersBase, PeriodBase

router = APIRouter()


@router.get('/trading_days')
async def get_last_trading_dates(
    db: AsyncSession = Depends(get_db),
    days_count: int = 0,
    redis=Depends(get_redis),
    ):

    params = days_count
    cache_key = make_cache_key('days', params)
    
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    query = (select(TradingResults.date)
             .distinct()
             .order_by(desc(TradingResults.date))
    )
    if days_count:
        query = query.limit(days_count)
    dates = await db.execute(query)
    results = dates.scalars().all()

    await redis.set(
        cache_key,
        json.dumps([date.strftime('%Y.%m.%d.%H:%M') for date in results]),
        ex=get_ttl())

    return results


@router.get('/get_trading_results')
async def get_trading_results(
    filters: FiltersBase = Depends(get_filters),
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_redis),
    ):
    params = filters.model_dump(exclude_none=True)
    cache_key = make_cache_key('results', params)
    
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    query = select(TradingResults)
    if filters:
        query = get_query(query, filters)

    result = await db.execute(query)
    results = result.scalars().all()

    await redis.set(
        cache_key,
        json.dumps([to_dict(i) for i in results]),
        ex=get_ttl()
        )

    return results
    

@router.post('/get_dynamics')
async def get_dynamics(
    peirod: PeriodBase,
    filters: FiltersBase = Depends(get_filters),
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_redis),
    ):
    params = filters.model_dump(exclude_none=True)
    prefix = get_date_for_prefix(peirod.model_dump(exclude_none=True))
    cache_key = make_cache_key(prefix, params)
    
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    query = (
        select(TradingResults)
        .where(TradingResults.date.between(peirod.start_date, peirod.end_date))
    )
    if filters:
        query = get_query(query, filters)
    
    result = await db.execute(query)
    dynamics = result.scalars().all()

    await redis.set(
        cache_key,
        json.dumps([to_dict(i) for i in dynamics]),
        ex=get_ttl()
        )

    return dynamics

