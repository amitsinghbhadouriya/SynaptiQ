"""FastAPI router for user authentication, registration, and session control."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends
from .auth_schemas import UserCredentials, UserRegistration, AuthTokenResponse
from .password_utils import hash_password, verify_password
from .auth import create_access_token
from .rate_limiter import default_rate_limiter

auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

# Demo user storage for local standalone runs
USERS_DB = {
    "admin": {
        "password_hash": hash_password("synaptiq-admin-pass"),
        "role": "admin",
        "email": "admin@synaptiq.ai"
    }
}


@auth_router.post("/login", response_model=AuthTokenResponse)
async def login(creds: UserCredentials):
    allowed, remaining, retry_after = default_rate_limiter.is_allowed(creds.username)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded (30 req/min). Retry in {retry_after:.1f}s"
        )

    user = USERS_DB.get(creds.username)
    if not user or not verify_password(creds.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(user_id=creds.username, role=user["role"])
    return AuthTokenResponse(
        access_token=token,
        user={"username": creds.username, "role": user["role"], "email": user["email"]}
    )
