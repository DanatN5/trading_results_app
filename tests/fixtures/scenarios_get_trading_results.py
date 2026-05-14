
DATA = {
    "id": 1,
    "exchange_product_id": "prod",
    "exchange_product_name": "name",
    "oil_id": "oil_id",
    "delivery_basis_id": "delivery_basis_id",
    "delivery_basis_name": "delivery_basis_name",
    "delivery_type_id": "delivery_type_id",
    "volume": 1,
    "total": 2,
    "count":  3,
    "date": "2026-05-12",
    "created_on": "2026-05-12",
    "updated_on": "2026-05-12"

}

VALID_DATES = {"start_date": "2026-04-10",
               "end_date": "2026-05-10"}

INVALID_DATES = {"start_date": "2026-04-10",
               "end_date": "2026-03-10"}


CACHE_HIT = {
    "dates": VALID_DATES,
    "cached": [DATA],
    "repo_data": [DATA],
    "expected_repo_calls": 0,
    "expected_cache_calls": 1,
}

CACHE_MISS = {
    "dates": VALID_DATES,
    "cached": None,
    "repo_data": [DATA],
    "expected_repo_calls": 1,
    "expected_cache_calls": 1,
}

INVALID_REQUEST = {
    "dates": INVALID_DATES,
    "cached": None,
    "repo_data": ["2026-05-12"],
    "expected_repo_calls": 0,
    "expected_cache_calls": 1,
}