"""
Test configuration for Phase 2 API endpoints.
Provides test client, test database, fixtures for users/tasks.
"""
import pytest
from typing import AsyncGenerator
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from src.phase2.main import app
from src.phase2.database import get_db
from src.phase2.auth.jwt import create_access_token
from src.phase2.models import User, Task, hash_password


# In-memory SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)

# Async session factory for tests
TestingAsyncSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """Override get_db dependency with test database session."""
    async with TestingAsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Create test database tables before running tests."""
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    # Cleanup after tests
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await test_engine.dispose()


@pytest.fixture
def override_db_dependency():
    """Override the get_db dependency for tests."""
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client(override_db_dependency) -> TestClient:
    """Provide FastAPI test client with overridden database."""
    return TestClient(app)


@pytest.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    """Provide async database session for fixtures."""
    async with TestingAsyncSessionLocal() as session:
        yield session


@pytest.fixture
async def user(db: AsyncSession) -> User:
    """Create a test user."""
    user = User(
        email="test@example.com",
        password_hash=hash_password("testpass123"),
        name="Test User"
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture
async def user2(db: AsyncSession) -> User:
    """Create a second test user."""
    user = User(
        email="test2@example.com",
        password_hash=hash_password("testpass123"),
        name="Test User 2"
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture
def access_token(user: User) -> str:
    """Generate JWT access token for test user."""
    return create_access_token(user.id)


@pytest.fixture
def access_token2(user2: User) -> str:
    """Generate JWT access token for second test user."""
    return create_access_token(user2.id)
