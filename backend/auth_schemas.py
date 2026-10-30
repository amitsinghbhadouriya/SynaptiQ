"""Pydantic schemas and dataclasses for SynaptiQ authentication and sessions."""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


class UserCredentials(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=100, description="Username for login")
    username_or_email: Optional[str] = Field(None, min_length=1, max_length=100, description="Username or email for login")
    password: str = Field(..., min_length=1, description="Plaintext password")


class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: str = Field(..., description="User contact email")
    password: str = Field(..., min_length=4, description="Plaintext password")
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
    token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int = 3600
    user: dict
