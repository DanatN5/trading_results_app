from sqlalchemy.sql.selectable import Select

from app.models import TradingResults
from app.schemas import FiltersBase


def get_query(query: Select, filters: FiltersBase) -> Select:
    if filters.oil_id:
        query = query.where(TradingResults.oil_id.in_(filters.oil_id))
    if filters.delivery_basis_id:
        query = query.where(
            TradingResults.delivery_basis_id.in_(filters.delivery_basis_id),
        )
    if filters.delivery_type_id:
        query = query.where(
            TradingResults.delivery_type_id.in_(filters.delivery_type_id),
        )

    return query
