import pytest
from unittest.mock import AsyncMock

from tests.fixtures.scenarios_get_last_trading_dates import CACHE_HIT, CACHE_MISS, INVALID_QUERY

# --- тестирование логики эндпоинта --- 
@pytest.mark.anyio
@pytest.mark.parametrize("case", [CACHE_HIT, CACHE_MISS])
async def test_get_last_trading_days_main(client, mock_cache, mock_repo, case):
    mock_cache.get_cache = AsyncMock(return_value=case["cached"])
    mock_repo.get_dates = AsyncMock(return_value=case["repo_data"])
    
    response = await client.get("/v1/trading_days")

    assert response.status_code == 200
    expected_data = (case["cached"] or case["repo_data"])

    assert response.json() == expected_data

    assert mock_cache.get_cache.call_count == case["expected_cache_calls"]

    assert mock_repo.get_dates.call_count == case["expected_repo_calls"]


# # --- тестирование ошибки в query параметре --- 
@pytest.mark.anyio
@pytest.mark.parametrize("case", [CACHE_HIT, INVALID_QUERY])
async def test_get_last_trading_days_invalid_query(client, mock_cache, mock_repo, case):
    mock_cache.get_cache = AsyncMock(return_value=case["cached"])
    mock_repo.get_dates = AsyncMock(return_value=case["repo_data"])

    url = f"/v1/trading_days?days_count={case['days_count']}"

    response = await client.get(url)

    if isinstance(case['days_count'], int):
        assert response.status_code == 200
    else:
        assert response.status_code == 422
