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


@router.get('/get_trading_results')
async def get_trading_results(
    filters: FiltersBase = Depends(get_filters),
    db: AsyncSession = Depends(get_db)
    ):

    query = select(TradingResults)

    if filters.oil_id:
        query = query.where(TradingResults.oil_id.in_(filters.oil_id))
    if filters.delivery_basis_id:
        query = query.where(TradingResults.delivery_basis_id.in_(filters.delivery_basis_id))
    if filters.delivery_type_id:
        query = query.where(TradingResults.delivery_type_id.in_(filters.delivery_type_id))

    results = await db.execute(query)
    return results.scalars().all()
    


@router.get('/get_dynamics')
async def get_dynamics(
    # dates: DatesBase,
    filters: FiltersBase = Depends(get_filters),
    db: AsyncSession = Depends(get_db)
    ):

    query = select(TradingResults)#.where(TradingResults.date.between(dates))

    if filters.oil_id:
        query = query.where(TradingResults.oil_id.in_(filters.oil_id))
    if filters.delivery_basis_id:
        query = query.where(TradingResults.delivery_basis_id.in_(filters.delivery_basis_id))
    if filters.delivery_type_id:
        query = query.where(TradingResults.delivery_type_id.in_(filters.delivery_type_id))
    
    dynamics = await db.execute(query)
    return dynamics.scalars().all()
