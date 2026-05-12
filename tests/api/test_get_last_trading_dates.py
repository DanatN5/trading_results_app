import pytest
from unittest.mock import AsyncMock

from tests.fixtures.scenarios import CACHE_HIT, CACHE_MISS

@pytest.mark.anyio
@pytest.mark.parametrize("case", [CACHE_HIT, CACHE_MISS])
async def test_get_last_trading_days(client, mock_cache, mock_repo, case):
    mock_cache.get_cache = AsyncMock(return_value=case["cached"])
    mock_repo.get_dates = AsyncMock(return_value=case["repo_data"])

    url = (
        f"/v1/trading_days?days_count={case['days_count']}"
        if case["days_count"] > 0
        else "/v1/trading_days"
    )

    response = await client.get(url)

    assert response.status_code == 200
    expected_data = (case["cached"] or case["repo_data"])

    assert response.json() == expected_data

    assert mock_cache.get_cache.call_count == case["expected_cache_calls"]

    assert mock_repo.get.call_count == case["expected_repo_calls"]