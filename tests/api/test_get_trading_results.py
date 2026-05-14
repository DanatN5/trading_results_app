import pytest
from unittest.mock import AsyncMock

from tests.fixtures.scenarios_get_trading_results import CACHE_HIT, CACHE_MISS

# --- тестирование логики эндпоинта --- 
@pytest.mark.anyio
@pytest.mark.parametrize("case", [CACHE_HIT, CACHE_MISS])
async def test_get_trading_results(client, mock_cache, mock_repo, case):
    mock_cache.get_cache = AsyncMock(return_value=case["cached"])
    mock_repo.get = AsyncMock(return_value=case["repo_data"])

    

    response = await client.get("/v1/get_trading_results")

    assert response.status_code == 200
    expected_data = (case["cached"] or case["repo_data"])

    assert response.json() == expected_data

    assert mock_cache.get_cache.call_count == case["expected_cache_calls"]

    assert mock_repo.get.call_count == case["expected_repo_calls"]

