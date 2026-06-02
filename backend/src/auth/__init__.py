"""
Auth module: JWT-based access + refresh token flow.

Token lifecycle:
  1. POST /api/v1/auth/login        → access_token + refresh_token
  2. Use access_token in Authorization header for API calls
  3. On 401, POST /api/v1/auth/refresh  → new access_token
  4. If refresh_token expired → redirect to login
"""

from src.auth.service import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
    get_current_user,
    TOKEN_TYPE_ACCESS,
    TOKEN_TYPE_REFRESH,
)
from src.auth.router import router as auth_router

__all__ = [
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "hash_password",
    "verify_password",
    "get_current_user",
    "TOKEN_TYPE_ACCESS",
    "TOKEN_TYPE_REFRESH",
    "auth_router",
]
