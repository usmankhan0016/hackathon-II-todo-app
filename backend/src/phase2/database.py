"""
Database connection module for Phase 2 Authentication System.
Handles SQLModel session management, connection pooling, and health checks.
"""

import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from .config import get_settings
from .models import User, Task  # Import all models for metadata registration

# Get settings
settings = get_settings()

# Logging setup
logger = logging.getLogger(__name__)

# Convert postgresql:// to postgresql+asyncpg:// for async support
# Remove sslmode parameter as asyncpg uses different SSL config
database_url = settings.DATABASE_URL
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Remove sslmode query parameter if present (asyncpg uses ssl=True instead)
if "?sslmode=" in database_url or "&sslmode=" in database_url:
    import re
    database_url = re.sub(r'[?&]sslmode=[^&]*', '', database_url)
    database_url = re.sub(r'[?&]channel_binding=[^&]*', '', database_url)

# Create async engine with connection pooling
# For Neon PostgreSQL, SSL is required but asyncpg handles it automatically
engine = create_async_engine(
    database_url,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_size=5,  # Minimum connections in pool
    max_overflow=15,  # Maximum additional connections (total 20)
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,  # Recycle connections after 1 hour
    # AsyncPG automatically uses SSL for connections
    connect_args={"ssl": "require"} if "neon.tech" in database_url else {},
)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.

    Usage in FastAPI:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            ...

    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize database tables.
    Creates all tables defined in SQLModel metadata.

    Should be called during application startup.
    """
    # Models already imported above
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(SQLModel.metadata.create_all)


async def check_db_health() -> bool:
    """
    Check database connection health.

    Returns:
        bool: True if database is reachable, False otherwise
    """
    try:
        async with AsyncSessionLocal() as session:
            # Simple query to test connection
            await session.execute("SELECT 1")
            return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


async def close_db() -> None:
    """
    Close database connections.
    Should be called during application shutdown.
    """
    await engine.dispose()
