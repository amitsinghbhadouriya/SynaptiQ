"""Pydantic schemas and dataclasses for SynaptiQ authentication and sessions."""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


class UserCredentials(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username for login")
    password: str = Field(..., min_length=8, description="Plaintext password")


class UserRegistration(UserCredentials):
    email: str = Field(..., description="User contact email")
    full_name: Optional[str] = Field(None, max_length=100)
    role: str = Field(default="viewer", pattern="^(admin|evaluator|viewer)$")


class TokenPayload(BaseModel):
    sub: str = Field(..., description="User identifier")
    role: str = Field(default="viewer")
    exp: int = Field(..., description="Expiration timestamp (epoch)")
    iat: int = Field(..., description="Issued at timestamp")
    jti: Optional[str] = Field(None, description="Unique JWT ID for revocation tracking")


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600
    user: dict
