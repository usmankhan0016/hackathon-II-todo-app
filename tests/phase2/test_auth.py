"""
Essential Authentication Tests - Phase 2
Tests signup and signin functionality with FastAPI TestClient
"""

import pytest
from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.src.phase2.main import app
from backend.src.phase2.database import get_db
from backend.src.phase2.models import User
from backend.src.phase2.config import get_settings

# Test database
TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/todo_app_test"

# Create async engine for test database
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


# Test database dependency override
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


# Apply override
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
async def client():
    """Create async test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
async def setup_database():
    """Setup test database before each test"""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)

    yield

    # Cleanup after test
    async with test_engine.begin() as conn:
        await conn.run_sync(User.metadata.drop_all)


class TestSignup:
    @pytest.mark.asyncio
    async def test_signup_success(self, client):
        """Test successful user signup"""
        response = client.post(
            "/api/signup",
            json={"email": "test@example.com", "password": "TestPass123", "name": "Test User"},
        )

        assert response.status_code == 201
        data = response.json()
        assert "user" in data
        assert "tokens" in data
        assert data["user"]["email"] == "test@example.com"
        assert data["user"]["name"] == "Test User"
        assert "access_token" in data["tokens"]
        assert "refresh_token" in data["tokens"]

    @pytest.mark.asyncio
    async def test_signup_duplicate_email(self, client):
        """Test signup with duplicate email fails"""
        # Create first user
        client.post(
            "/api/signup",
            json={"email": "duplicate@example.com", "password": "TestPass123", "name": "User 1"},
        )

        # Try to create second user with same email
        response = client.post(
            "/api/signup",
            json={"email": "duplicate@example.com", "password": "TestPass123", "name": "User 2"},
        )

        assert response.status_code == 409
        assert "already registered" in response.json()["message"].lower()

    @pytest.mark.asyncio
    async def test_signup_weak_password(self, client):
        """Test signup with weak password fails"""
        response = client.post(
            "/api/signup", json={"email": "test@example.com", "password": "123", "name": "Test"}
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_signup_invalid_email(self, client):
        """Test signup with invalid email fails"""
        response = client.post(
            "/api/signup", json={"email": "invalid-email", "password": "TestPass123"}
        )

        assert response.status_code == 422


class TestSignin:
    @pytest.mark.asyncio
    async def test_signin_success(self, client):
        """Test successful user signin"""
        # First signup
        client.post(
            "/api/signup",
            json={"email": "signin@example.com", "password": "TestPass123", "name": "Signin Test"},
        )

        # Then signin
        response = client.post(
            "/api/signin", json={"email": "signin@example.com", "password": "TestPass123"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert "tokens" in data
        assert "access_token" in data["tokens"]
        assert "refresh_token" in data["tokens"]

    @pytest.mark.asyncio
    async def test_signin_wrong_password(self, client):
        """Test signin with wrong password fails"""
        # First signup
        client.post(
            "/api/signup",
            json={"email": "wrongpass@example.com", "password": "TestPass123", "name": "Test"},
        )

        # Try signin with wrong password
        response = client.post(
            "/api/signin", json={"email": "wrongpass@example.com", "password": "WrongPass123"}
        )

        assert response.status_code == 401
        assert "invalid credentials" in response.json()["message"].lower()

    @pytest.mark.asyncio
    async def test_signin_nonexistent_user(self, client):
        """Test signin with non-existent user fails"""
        response = client.post(
            "/api/signin", json={"email": "nonexistent@example.com", "password": "TestPass123"}
        )

        assert response.status_code == 401
        assert "invalid credentials" in response.json()["message"].lower()


class TestTokenGeneration:
    @pytest.mark.asyncio
    async def test_tokens_different_each_signin(self, client):
        """Test that tokens are different on each signin (security)"""
        # Signup
        client.post(
            "/api/signup",
            json={"email": "token@example.com", "password": "TestPass123", "name": "Token Test"},
        )

        # Signin twice
        response1 = client.post("/api/signin", json={"email": "token@example.com", "password": "TestPass123"})
        response2 = client.post("/api/signin", json={"email": "token@example.com", "password": "TestPass123"})

        token1 = response1.json()["tokens"]["access_token"]
        token2 = response2.json()["tokens"]["access_token"]

        # Tokens should be different (different timestamps)
        assert token1 != token2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
