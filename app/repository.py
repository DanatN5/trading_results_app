from typing import Protocol, Any
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import TradingResults
from app.schemas import FiltersBase, IntervalBase
from app.helpers import get_query

class Repository(Protocol):
    async def get_dates(self, days_count: int) -> list[str]: pass

    async def get(self, filters: FiltersBase, interval: IntervalBase = None) -> list[dict]: pass



class SQLAlchemyRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_dates(self, days_count: int) -> list[str]:
        query = (
        select(TradingResults.date)
        .distinct()
        .order_by(desc(TradingResults.date))
        )
        if days_count:
            query = query.limit(days_count)
        dates = await self._session.execute(query)
        results = dates.scalars().all()
        data = [date.strftime("%Y-%m-%dT%H:%M") for date in results]

        return data
    
    async def get(self, filters: FiltersBase, interval:IntervalBase = None) -> list[dict]:

        query = select(TradingResults)
        if interval:
            query = query.where(
            TradingResults.date.between(interval.start_date, interval.end_date),
            )
        if filters:
            query = get_query(query, filters)

        result = await self._session.execute(query)
        results = result.scalars().all()

        data = [table.to_dict() for table in results]

        return data