from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .database import AsyncSessionLocal
from .models import TradingResults



router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.get('/trading_days')
async def get_last_trading_dates(db: AsyncSession = Depends(get_db)):
    query = select(TradingResults.date)
    dates = await db.execute(query)

    return dates.scalars().all()


