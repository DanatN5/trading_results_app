import pytest

from unittest.mock import AsyncMock
from httpx import AsyncClient, ASGITransport
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.main import app
from app.dependencies import get_repo, get_filters, get_cache_storage
from app.database import Base
from app.models import TradingResults


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




