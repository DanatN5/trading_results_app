import json
import hashlib
from datetime import datetime
from .models import TradingResults





def get_query(query, filters):
    if filters.oil_id:
        query = query.where(TradingResults.oil_id.in_(filters.oil_id))
    if filters.delivery_basis_id:
        query = query.where(TradingResults.delivery_basis_id.in_(filters.delivery_basis_id))
    if filters.delivery_type_id:
        query = query.where(TradingResults.delivery_type_id.in_(filters.delivery_type_id))

    return query


def make_cache_key(prefix: str, params: dict) -> str:
    raw = json.dumps(params, sort_keys=True)
    return f"{prefix}:{hashlib.md5(raw.encode()).hexdigest()}"


def get_date_for_prefix(date: dict[str: datetime]) -> str:
    start_date = date['start_date'].strftime('%Y.%m.%d.%H:%M')
    end_date = date['end_date'].strftime('%Y.%m.%d.%H:%M')

    return f"{start_date}-{end_date}"

def to_dict(obj):
    result = {}
    for col in obj.__table__.columns:
        value = getattr(obj, col.name)
        if isinstance(value, datetime):
            value = value.isoformat()
        result[col.name] = value
    return result