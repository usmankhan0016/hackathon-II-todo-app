"""
Error handlers for authentication system.
Provides standardized error responses with machine-readable codes.
"""

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from ..schemas.auth import ErrorCode


class AuthError(HTTPException):
    """Base authentication error with error code."""

    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
    ):
        """
        Initialize authentication error.

        Args:
            status_code: HTTP status code
            error_code: Machine-readable error code
            message: User-facing error message
        """
        super().__init__(status_code=status_code, detail=message)
        self.error_code = error_code
        self.message = message


# Specific error classes


class InvalidCredentialsError(AuthError):
    """Raised when signin credentials are invalid."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=ErrorCode.AUTH_INVALID_CREDENTIALS,
            message="Invalid credentials",
        )


class EmailExistsError(AuthError):
    """Raised when email already exists during signup."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code=ErrorCode.AUTH_EMAIL_EXISTS,
            message="Email already registered",
        )


class InvalidEmailError(AuthError):
    """Raised when email format is invalid."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code=ErrorCode.AUTH_INVALID_EMAIL,
            message="Please enter a valid email",
        )


class WeakPasswordError(AuthError):
    """Raised when password is too weak."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code=ErrorCode.AUTH_WEAK_PASSWORD,
            message="Password must be at least 8 characters",
        )


class TokenExpiredError(AuthError):
    """Raised when JWT token has expired."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=ErrorCode.AUTH_TOKEN_EXPIRED,
            message="Token expired",
        )


class TokenInvalidError(AuthError):
    """Raised when JWT token is invalid or malformed."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=ErrorCode.AUTH_TOKEN_INVALID,
            message="Invalid token",
        )


class TokenMissingError(AuthError):
    """Raised when JWT token is missing from request."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=ErrorCode.AUTH_TOKEN_MISSING,
            message="Token required",
        )


class ForbiddenError(AuthError):
    """Raised when user attempts to access forbidden resource."""

    def __init__(self, message: str = "Access denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code=ErrorCode.AUTH_FORBIDDEN,
            message=message,
        )


# Error response formatter


def format_error_response(
    error_code: str,
    message: str,
    status_code: int,
) -> JSONResponse:
    """
    Format error response with standard structure.

    Args:
        error_code: Machine-readable error code
        message: User-facing error message
        status_code: HTTP status code

    Returns:
        JSONResponse: Formatted error response

    Example:
        >>> response = format_error_response(
        ...     ErrorCode.AUTH_INVALID_CREDENTIALS,
        ...     "Invalid credentials",
        ...     401
        ... )
        >>> response.status_code
        401
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "error": error_code,
            "message": message,
            "status_code": status_code,
        },
    )


# Exception handler for AuthError


async def auth_error_handler(request, exc: AuthError) -> JSONResponse:
    """
    Global exception handler for AuthError.

    Args:
        request: FastAPI request
        exc: AuthError exception

    Returns:
        JSONResponse: Formatted error response
    """
    return format_error_response(
        error_code=exc.error_code,
        message=exc.message,
        status_code=exc.status_code,
    )
