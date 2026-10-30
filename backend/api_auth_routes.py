"""FastAPI router for user authentication, registration, and session control."""

from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, HTTPException, Request
from .auth_schemas import UserCredentials, UserRegistration, AuthTokenResponse
from .password_utils import hash_password, verify_password
from .auth import create_access_token
from .rate_limiter import default_rate_limiter

auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

# In-memory user store initialized with admin account
USERS_DB = {
    "admin": {
        "password_hash": hash_password("synaptiq-admin-pass"),
        "role": "admin",
        "email": "admin@synaptiq.ai"
    }
}


def _find_user(identifier: str) -> tuple[Optional[str], Optional[dict]]:
    """Look up user by username or email address."""
    ident_lower = identifier.strip().lower()
    for username, data in USERS_DB.items():
        if username.lower() == ident_lower or data.get("email", "").lower() == ident_lower:
            return username, data
    return None, None


@auth_router.post("/login", response_model=AuthTokenResponse)
async def login(creds: UserCredentials):
    ident = (creds.username_or_email or creds.username or "").strip()
    if not ident:
        raise HTTPException(status_code=400, detail="Username or email is required")

    allowed, remaining, retry_after = default_rate_limiter.is_allowed(ident)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded (30 req/min). Retry in {retry_after:.1f}s"
        )

    username, user = _find_user(ident)
    if not user or not verify_password(creds.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(user_id=username, role=user["role"])
    return AuthTokenResponse(
        access_token=token,
        token=token,
        user={"username": username, "role": user["role"], "email": user["email"]}
    )


@auth_router.post("/register", response_model=AuthTokenResponse)
async def register(creds: UserRegistration):
    username = creds.username.strip()
    email = creds.email.strip()

    allowed, remaining, retry_after = default_rate_limiter.is_allowed(username)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded (30 req/min). Retry in {retry_after:.1f}s"
        )

    if username.lower() in [u.lower() for u in USERS_DB]:
        raise HTTPException(status_code=400, detail="Username already registered")

    for u_data in USERS_DB.values():
        if u_data.get("email", "").lower() == email.lower():
            raise HTTPException(status_code=400, detail="Email already registered")

    user_entry = {
        "password_hash": hash_password(creds.password),
        "role": creds.role,
        "email": email,
        "full_name": creds.full_name
    }
    USERS_DB[username] = user_entry

    token = create_access_token(user_id=username, role=creds.role)
    return AuthTokenResponse(
        access_token=token,
        token=token,
        user={"username": username, "role": creds.role, "email": email}
    )


@auth_router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}
