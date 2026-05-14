
CACHE_HIT = {
    "days_count": 1,
    "cached": ["2026-05-12"],
    "repo_data": ["2026-05-12"],
    "expected_repo_calls": 0,
    "expected_cache_calls": 1,
}

CACHE_MISS = {
    "cached": None,
    "repo_data": ["2026-05-12"],
    "expected_repo_calls": 1,
    "expected_cache_calls": 1,
}

INVALID_QUERY = {
    "days_count": "one",
    "cached": None,
    "repo_data": ["2026-05-12"],
    "expected_repo_calls": 0,
    "expected_cache_calls": 1,
}