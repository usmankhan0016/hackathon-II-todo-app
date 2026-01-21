"""
Authentication middleware for JWT token verification.
Extracts and verifies tokens, injects user_id into request context.
"""

from typing import Callable

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from ..auth.jwt import verify_token
from ..handlers.errors import TokenExpiredError, TokenInvalidError, TokenMissingError

# HTTP Bearer scheme for Authorization header
security = HTTPBearer(auto_error=False)


async def get_current_user_id(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> str:
    """
    Extract and verify JWT token, return user_id.

    This dependency should be used on protected endpoints to enforce authentication.

    Args:
        request: FastAPI request object
        credentials: HTTP Authorization credentials (Bearer token)

    Returns:
        str: User ID extracted from JWT token

    Raises:
        TokenMissingError: If Authorization header is missing
        TokenInvalidError: If token is invalid or malformed
        TokenExpiredError: If token has expired

    Example:
        @app.get("/protected")
        async def protected_route(user_id: str = Depends(get_current_user_id)):
            return {"user_id": user_id}
    """
    # Check if credentials provided
    if not credentials:
        raise TokenMissingError()

    token = credentials.credentials

    # Verify token and extract user_id
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")

        if not user_id:
            raise TokenInvalidError()

        # Store user_id in request state for later use
        request.state.user_id = user_id

        return user_id

    except JWTError as e:
        # Check if token expired
        error_message = str(e).lower()
        if "expired" in error_message:
            raise TokenExpiredError()
        else:
            raise TokenInvalidError()


class AuthMiddleware:
    """
    Middleware to automatically verify JWT tokens on all requests.

    This can be added to FastAPI app to enforce authentication globally,
    with exceptions for specific routes.
    """

    def __init__(
        self,
        exclude_paths: list[str] | None = None,
    ):
        """
        Initialize auth middleware.

        Args:
            exclude_paths: List of paths to exclude from authentication
                           (e.g., ["/api/auth/signup", "/api/auth/signin"])
        """
        self.exclude_paths = exclude_paths or []

    async def __call__(
        self,
        request: Request,
        call_next: Callable,
    ):
        """
        Process request through middleware.

        Args:
            request: FastAPI request
            call_next: Next middleware/route handler

        Returns:
            Response from next handler
        """
        # Skip authentication for excluded paths
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        # Skip authentication for health/docs endpoints
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Extract Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            # No token provided - let the route handler decide if it's required
            return await call_next(request)

        # Extract token
        token = auth_header.split(" ")[1] if " " in auth_header else None

        if token:
            try:
                # Verify token and inject user_id
                payload = verify_token(token)
                user_id = payload.get("sub")

                if user_id:
                    request.state.user_id = user_id

            except JWTError:
                # Token invalid, but don't block - let route handler decide
                pass

        # Continue to next handler
        return await call_next(request)


def get_user_id_from_request(request: Request) -> str | None:
    """
    Get user_id from request state (if set by middleware).

    Args:
        request: FastAPI request

    Returns:
        str | None: User ID if authenticated, None otherwise

    Example:
        @app.get("/optional-auth")
        async def route(request: Request):
            user_id = get_user_id_from_request(request)
            if user_id:
                return {"message": f"Hello {user_id}"}
            return {"message": "Hello guest"}
    """
    return getattr(request.state, "user_id", None)
