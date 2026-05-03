from app.models import TradingResults


def get_query(query, filters):
    if filters.oil_id:
        query = query.where(TradingResults.oil_id.in_(filters.oil_id))
    if filters.delivery_basis_id:
        query = query.where(
            TradingResults.delivery_basis_id.in_(filters.delivery_basis_id)
        )
    if filters.delivery_type_id:
        query = query.where(
            TradingResults.delivery_type_id.in_(filters.delivery_type_id)
        )

    return query

