from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from .database import AsyncSessionLocal
from .models import TradingResults
from .schemas import FiltersBase
from .dependencies import get_filters



router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.get('/trading_days')
async def get_last_trading_dates(db: AsyncSession = Depends(get_db), days_count: int = 0):
    query = select(TradingResults.date).distinct().order_by(desc(TradingResults.date))
    if days_count:
        query = query.limit(days_count)
    dates = await db.execute(query)

    return dates.scalars().all()


@router.get('/dynamics')
async def get_dynamics(filters: FiltersBase = Depends(get_filters), db: AsyncSession = Depends(get_db)):
    query = select(TradingResults)

    if filters.start_date:
        query = query.where(TradingResults.date > filters.start_date)

    dynamics = await db.execute(query)
    return dynamics.scalars().all()
    

