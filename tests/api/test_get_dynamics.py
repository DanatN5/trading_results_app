import pytest
from unittest.mock import AsyncMock
from datetime import datetime, date

from tests.fixtures.scenarios_get_trading_results import CACHE_HIT, CACHE_MISS, INVALID_REQUEST

# --- тестирование логики эндпоинта --- 
@pytest.mark.anyio
@pytest.mark.parametrize("case", [CACHE_HIT, CACHE_MISS])
async def test_get_dynamics(client, mock_cache, mock_repo, case):
    mock_cache.get_cache = AsyncMock(return_value=case["cached"])
    mock_repo.get = AsyncMock(return_value=case["repo_data"])

    

    response = await client.post("/v1/get_dynamics", json=case["dates"])

    assert response.status_code == 200
    expected_data = (case["cached"] or case["repo_data"])

    assert response.json() == expected_data

    assert mock_cache.get_cache.call_count == case["expected_cache_calls"]

    assert mock_repo.get.call_count == case["expected_repo_calls"]


# # --- тестирование ошибки в датах --- 
@pytest.mark.anyio
@pytest.mark.parametrize("case", [CACHE_HIT, INVALID_REQUEST])
async def test_get_last_trading_days_invalid_query(client, mock_cache, mock_repo, case):
    mock_cache.get_cache = AsyncMock(return_value=case["cached"])
    mock_repo.get = AsyncMock(return_value=case["repo_data"])

    start_date = datetime.strptime(case["dates"]["start_date"], "%Y-%m-%d").date()
    end_date = date.fromisoformat(case["dates"]["end_date"])

    response = await client.post("/v1/get_dynamics", json=case["dates"])

    if start_date < end_date:
        assert response.status_code == 200
    else:
        assert response.status_code == 422
