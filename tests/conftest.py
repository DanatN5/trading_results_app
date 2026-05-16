import pytest

from unittest.mock import AsyncMock
from httpx import AsyncClient, ASGITransport
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.main import app
from app.dependencies import get_repo, get_filters, get_cache_storage
from app.database import Base
from app.models import TradingResults
from app.repository import SQLAlchemyRepo


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


# --- фикстура с контейнером postgres (вернет sync url) ---
@pytest.fixture(scope="session")
async def postgres_container():
    container = PostgresContainer("postgres:15")

    container.start()

    yield container

    container.stop()


@pytest.fixture(scope="session")
async def engine(postgres_container):
    sync_url = postgres_container.get_connection_url()

    async_url = sync_url.replace("postgresql", "postgresql+asyncpg")

    engine = create_async_engine(url=async_url, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()

@pytest.fixture
async def session(engine):
    SessionLocal = async_sessionmaker(
        bind=engine,
        expire_on_commit=False
    )

    async with SessionLocal() as session:
        yield session

        await session.rollback()


@pytest.fixture
async def test_repo(session):
    return SQLAlchemyRepo(session)


