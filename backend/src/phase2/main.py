"""
FastAPI Application - Phase 2: Authentication System
Main application entry point with CORS, error handlers, and middleware setup.
"""

import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import NoResultFound

from .config import get_settings
from .database import check_db_health, close_db, init_db
from .handlers.errors import AuthError, auth_error_handler

# Import routes to register them
from .routes import auth, tasks  # noqa: F401

# Import models to register them with SQLModel metadata before table creation
from .models import User, Task  # noqa: F401 - models must be imported before table creation

# Configuration
settings = get_settings()

# Logging setup
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    """Handle startup and shutdown events."""
    # Startup
    logger.info("Starting Todo App Backend - Phase 2: Authentication System")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Database: {settings.DATABASE_URL[:50]}...")

    # Initialize database tables
    logger.info("Initializing database tables...")
    try:
        await init_db()
        logger.info("Database tables initialized successfully")

        # Check database health
        is_healthy = await check_db_health()
        if is_healthy:
            logger.info("Database connection healthy")
        else:
            logger.warning("Database connection check failed")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down Todo App Backend")
    await close_db()
    logger.info("Database connections closed")


# Initialize FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description="Authentication System for Todo App",
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    lifespan=lifespan,
)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (localhost testing)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("CORS Enabled for all origins")

# Register error handlers
app.add_exception_handler(AuthError, auth_error_handler)

# Database error handlers
from .handlers.db_errors import integrity_error_handler, operational_error_handler, no_result_found_handler
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(OperationalError, operational_error_handler)
app.add_exception_handler(NoResultFound, no_result_found_handler)

# Include routers
from .routes.auth import router as auth_router
from .routes.tasks import router as tasks_router

app.include_router(auth_router, prefix=settings.API_PREFIX)
app.include_router(tasks_router, prefix=settings.API_PREFIX)

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """
    Health check endpoint for monitoring.

    Returns:
        dict with status "ok"
    """
    return {"status": "ok", "service": "todo-app-auth"}


# Root endpoint
@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    """
    Root endpoint.

    Returns:
        dict with welcome message
    """
    return {
        "message": "Todo App Authentication API",
        "version": settings.API_VERSION,
        "docs": "/docs",
    }


# Global exception handler for validation errors
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Handle ValueError exceptions with proper error response."""
    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": str(exc),
            "status_code": 422,
        },
    )


# Global exception handler for general exceptions
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions with proper error response."""
    error_code = "INTERNAL_SERVER_ERROR"
    status_code = 500
    message = "An internal server error occurred"

    if settings.DEBUG:
        message = str(exc)

    return JSONResponse(
        status_code=status_code,
        content={
            "error": error_code,
            "message": message,
            "status_code": status_code,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
