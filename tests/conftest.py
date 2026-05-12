import pytest

from unittest.mock import AsyncMock
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.dependencies import get_repo, get_filters, get_cache_storage


@pytest.fixture
def mock_repo():
    return AsyncMock()

@pytest.fixture
def mock_cache():
    return AsyncMock()

@pytest.fixture
async def client(mock_repo, mock_cache):
    app.dependency_overrides[get_cache_storage] = lambda: mock_cache
    app.dependency_overrides[get_repo] = lambda: mock_repo

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
    
    app.dependency_overrides.clear()

