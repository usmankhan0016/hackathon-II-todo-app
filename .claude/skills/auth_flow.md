---
name: auth-flow
description: Implement end-to-end authentication flow validation from signup through protected requests. Use when testing and validating complete auth scenarios.
---

# Auth Flow Skill - End-to-End Authentication Validation

## Instructions

Implement comprehensive validation of the complete authentication flow from user registration through authenticated API requests, including token lifecycle management.

### 1. **Signup Flow Validation**
   - User submits email and password
   - Backend validates input (format, length, strength)
   - Backend hashes password securely (bcrypt)
   - Backend checks for duplicate email (409 Conflict)
   - Backend creates user in database
   - Backend generates access token (JWT)
   - Backend generates refresh token (JWT)
   - Frontend receives tokens in response
   - Frontend stores tokens securely (localStorage or httpOnly cookie)
   - User redirected to dashboard
   - Verify token contains user_id in `sub` claim
   - Verify token contains email in token payload

### 2. **Login Flow Validation**
   - User submits email and password
   - Backend queries user by email
   - Backend verifies password hash matches
   - Invalid credentials return 401 (no user enumeration)
   - Backend generates fresh access token
   - Backend generates fresh refresh token
   - Frontend stores both tokens
   - User redirected to dashboard
   - Verify old tokens are invalidated
   - Verify new tokens have current timestamp

### 3. **Protected Request Flow**
   - Frontend retrieves token from storage
   - Frontend attaches token in Authorization header: `Bearer <token>`
   - Backend middleware extracts and verifies token
   - Backend validates token signature
   - Backend validates token expiration
   - Backend extracts user_id from `sub` claim
   - Backend verifies user exists in database
   - Backend injects user_id into request context
   - Endpoint accesses protected resource
   - Response only contains user's own data
   - Return 401 if token missing/invalid
   - Return 403 if user_id doesn't match resource ownership

### 4. **Token Refresh Flow**
   - Access token approaches expiration (< 5 minutes)
   - Frontend calls refresh endpoint with refresh token
   - Backend validates refresh token
   - Backend generates new access token
   - Backend optionally generates new refresh token
   - Backend returns new access tokens
   - Frontend updates stored tokens
   - Frontend retries original request with new token
   - Request succeeds without user intervention

### 5. **Logout Flow**
   - User clicks logout
   - Frontend clears stored tokens
   - Frontend clears user session/cookies
   - Frontend redirects to login page
   - Subsequent requests to protected endpoints return 401
   - Backend optional: add token to blacklist (revocation)

### 6. **Error Scenarios**
   - **Invalid credentials**: 401 Unauthorized (generic message)
   - **Expired token**: 401 Unauthorized + refresh attempt
   - **Invalid signature**: 401 Unauthorized
   - **Missing token**: 401 Unauthorized with "Authentication required"
   - **Malformed header**: 401 Unauthorized
   - **Token tampering**: 401 Unauthorized
   - **Cross-user access**: 403 Forbidden
   - **User deleted**: 401 Unauthorized

## Example Implementation

### Signup Flow Test
```python
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_signup_success():
    """Test successful signup flow."""
    # Request
    response = client.post("/api/auth/signup", json={
        "email": "newuser@example.com",
        "password": "SecurePass123"
    })

    # Assertions
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["email"] == "newuser@example.com"
    assert data["user_id"]

    # Verify token contents
    import jwt
    payload = jwt.decode(data["access_token"], options={"verify_signature": False})
    assert payload["sub"] == data["user_id"]
    assert payload["email"] == "newuser@example.com"
    assert "exp" in payload
    assert "iat" in payload

def test_signup_duplicate_email():
    """Test signup with existing email."""
    # Create first user
    client.post("/api/auth/signup", json={
        "email": "duplicate@example.com",
        "password": "SecurePass123"
    })

    # Try to create with same email
    response = client.post("/api/auth/signup", json={
        "email": "duplicate@example.com",
        "password": "DifferentPass123"
    })

    assert response.status_code == 409
    assert "already registered" in response.json()["detail"]

def test_signup_invalid_email():
    """Test signup with invalid email."""
    response = client.post("/api/auth/signup", json={
        "email": "not-an-email",
        "password": "SecurePass123"
    })

    assert response.status_code == 422
    assert "email" in response.json()

def test_signup_weak_password():
    """Test signup with weak password."""
    response = client.post("/api/auth/signup", json={
        "email": "user@example.com",
        "password": "weak"
    })

    assert response.status_code == 422
    assert "password" in response.json()
```

### Login Flow Test
```python
def test_login_success():
    """Test successful login flow."""
    # Create user
    signup_response = client.post("/api/auth/signup", json={
        "email": "testuser@example.com",
        "password": "SecurePass123"
    })
    user_id = signup_response.json()["user_id"]

    # Login
    response = client.post("/api/auth/signin", json={
        "email": "testuser@example.com",
        "password": "SecurePass123"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user_id"] == user_id

def test_login_invalid_password():
    """Test login with wrong password."""
    # Create user
    client.post("/api/auth/signup", json={
        "email": "testuser@example.com",
        "password": "CorrectPassword123"
    })

    # Try wrong password
    response = client.post("/api/auth/signin", json={
        "email": "testuser@example.com",
        "password": "WrongPassword123"
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_login_nonexistent_user():
    """Test login with nonexistent email."""
    response = client.post("/api/auth/signin", json={
        "email": "nonexistent@example.com",
        "password": "AnyPassword123"
    })

    assert response.status_code == 401
    # No user enumeration - same message as wrong password
    assert response.json()["detail"] == "Invalid credentials"
```

### Protected Request Flow Test
```python
def test_protected_endpoint_with_token():
    """Test accessing protected endpoint with valid token."""
    # Signup and get token
    signup_response = client.post("/api/auth/signup", json={
        "email": "user@example.com",
        "password": "SecurePass123"
    })
    access_token = signup_response.json()["access_token"]

    # Access protected endpoint
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json()["items"] == []  # Empty list for new user

def test_protected_endpoint_without_token():
    """Test accessing protected endpoint without token."""
    response = client.get("/api/tasks")

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required"

def test_protected_endpoint_with_invalid_token():
    """Test accessing protected endpoint with invalid token."""
    response = client.get(
        "/api/tasks",
        headers={"Authorization": "Bearer invalid.token.here"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_protected_endpoint_with_expired_token():
    """Test accessing protected endpoint with expired token."""
    import jwt
    from datetime import datetime, timedelta
    import os

    # Create expired token
    payload = {
        "sub": "test-user-id",
        "email": "test@example.com",
        "exp": datetime.utcnow() - timedelta(hours=1)
    }
    expired_token = jwt.encode(
        payload,
        os.getenv("BETTER_AUTH_SECRET"),
        algorithm="HS256"
    )

    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Token expired"
```

### Token Refresh Flow Test
```python
def test_token_refresh_success():
    """Test successful token refresh."""
    # Signup
    signup_response = client.post("/api/auth/signup", json={
        "email": "user@example.com",
        "password": "SecurePass123"
    })
    refresh_token = signup_response.json()["refresh_token"]
    original_access_token = signup_response.json()["access_token"]

    # Refresh token
    response = client.post("/api/auth/refresh", json={
        "refresh_token": refresh_token
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    # New token should be different from old
    assert data["access_token"] != original_access_token

    # Verify new token works
    tasks_response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {data['access_token']}"}
    )
    assert tasks_response.status_code == 200

def test_token_refresh_with_invalid_token():
    """Test token refresh with invalid refresh token."""
    response = client.post("/api/auth/refresh", json={
        "refresh_token": "invalid.token.here"
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid refresh token"

def test_token_refresh_with_expired_refresh_token():
    """Test token refresh with expired refresh token."""
    import jwt
    from datetime import datetime, timedelta
    import os

    # Create expired refresh token
    payload = {
        "sub": "test-user-id",
        "type": "refresh",
        "exp": datetime.utcnow() - timedelta(days=1)
    }
    expired_refresh_token = jwt.encode(
        payload,
        os.getenv("BETTER_AUTH_SECRET"),
        algorithm="HS256"
    )

    response = client.post("/api/auth/refresh", json={
        "refresh_token": expired_refresh_token
    })

    assert response.status_code == 401
    assert "expired" in response.json()["detail"]
```

### Logout Flow Test
```typescript
// Frontend logout test
import { render, screen, fireEvent } from '@testing-library/react';
import { useRouter } from 'next/navigation';
import LogoutButton from '@/components/LogoutButton';
import * as authLib from '@/lib/auth';

jest.mock('next/navigation');
jest.mock('@/lib/auth');

test('logout clears tokens and redirects', async () => {
  const mockPush = jest.fn();
  (useRouter as jest.Mock).mockReturnValue({ push: mockPush });

  render(<LogoutButton />);
  const button = screen.getByText('Logout');

  fireEvent.click(button);

  // Verify tokens cleared
  expect(authLib.clearTokens).toHaveBeenCalled();

  // Verify redirect to login
  expect(mockPush).toHaveBeenCalledWith('/login');

  // Verify subsequent requests to protected endpoints return 401
  const response = await fetch('/api/tasks', {
    headers: { 'Authorization': 'Bearer undefined' }
  });
  expect(response.status).toBe(401);
});
```

### End-to-End Auth Flow Scenario
```python
def test_complete_auth_flow():
    """Test complete authentication flow from signup to protected request."""
    # 1. Signup
    signup_response = client.post("/api/auth/signup", json={
        "email": "e2e@example.com",
        "password": "CompleteFlow123"
    })
    assert signup_response.status_code == 201
    access_token = signup_response.json()["access_token"]
    user_id = signup_response.json()["user_id"]

    # 2. Create task with authenticated request
    task_response = client.post(
        "/api/tasks",
        json={"title": "Test Task"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert task_response.status_code == 201
    task_id = task_response.json()["id"]

    # 3. Verify task belongs to user
    assert task_response.json()["user_id"] == user_id

    # 4. Logout in frontend (clear tokens)
    client.cookies.clear()

    # 5. Try to access protected endpoint without token
    protected_response = client.get("/api/tasks")
    assert protected_response.status_code == 401

    # 6. Login again
    login_response = client.post("/api/auth/signin", json={
        "email": "e2e@example.com",
        "password": "CompleteFlow123"
    })
    assert login_response.status_code == 200
    new_access_token = login_response.json()["access_token"]

    # 7. Access protected endpoint with new token
    tasks_response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {new_access_token}"}
    )
    assert tasks_response.status_code == 200
    # Verify task is still there and belongs to user
    assert len(tasks_response.json()["items"]) == 1
    assert tasks_response.json()["items"][0]["id"] == task_id
```

## Acceptance Criteria
- [ ] Signup flow creates user and returns tokens
- [ ] Tokens contain correct user_id in `sub` claim
- [ ] Tokens contain correct email in payload
- [ ] Duplicate email signup returns 409
- [ ] Invalid email signup returns 422
- [ ] Weak password signup returns 422
- [ ] Login with correct credentials succeeds
- [ ] Login with wrong password returns 401
- [ ] Nonexistent user login returns 401 (no enumeration)
- [ ] Protected requests with valid token succeed
- [ ] Protected requests without token return 401
- [ ] Protected requests with invalid token return 401
- [ ] Protected requests with expired token return 401
- [ ] Token refresh generates new access token
- [ ] Invalid refresh token returns 401
- [ ] Expired refresh token returns 401
- [ ] Logout clears tokens
- [ ] Post-logout requests to protected endpoints return 401
- [ ] End-to-end flow works seamlessly
- [ ] All error scenarios properly handled

## Dependencies
- **pytest**: Testing framework (backend)
- **FastAPI TestClient**: API testing
- **@testing-library/react**: Component testing (frontend)
- **jest**: JavaScript testing framework
- **python-jose/jwt**: Token validation
- **pytest-asyncio**: Async test support

## Related Skills
- `security_validation` – Validate user isolation and data access
- `jwt_middleware` – Token verification implementation
- `auth_routes` – Auth endpoints to test
- `error_handling` – Error scenarios in auth
