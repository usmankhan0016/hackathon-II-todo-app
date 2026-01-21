"""
Database error handlers.
Translates SQLAlchemy exceptions to HTTP responses.
"""
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import NoResultFound

from ..schemas.task import ErrorDetail


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """Handle IntegrityError (duplicate unique constraints)."""
    return JSONResponse(
        status_code=409,
        content=ErrorDetail(
            error="INTEGRITY_VIOLATION",
            message="Resource already exists",
            status_code=409
        ).dict()
    )


async def operational_error_handler(request: Request, exc: OperationalError) -> JSONResponse:
    """Handle OperationalError (DB unavailable)."""
    return JSONResponse(
        status_code=503,
        content=ErrorDetail(
            error="DATABASE_UNAVAILABLE",
            message="Database temporarily unavailable",
            status_code=503
        ).dict()
    )


async def no_result_found_handler(request: Request, exc: NoResultFound) -> JSONResponse:
    """Handle NoResultFound."""
    return JSONResponse(
        status_code=404,
        content=ErrorDetail(
            error="NOT_FOUND",
            message="Resource not found",
            status_code=404
        ).dict()
    )
