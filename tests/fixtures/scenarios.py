database = [
    "2026-05-12",
    "2026-05-11",
    "2026-05-10"
    ]

CACHE_HIT = {
    "days_count": 1,
    "cached": ["2026-05-12"],
    "repo_data": ["2026-05-12"],
    "expected_repo_calls": 0,
    "expected_cache_calls": 1,
}

CACHE_MISS = {
    "days_count": 1,
    "cached": None,
    "repo_data": ["2026-05-12"],
    "expected_repo_calls": 0,
    "expected_cache_calls": 1,
}