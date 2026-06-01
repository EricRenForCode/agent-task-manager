"""
Auth service: JWT creation, verification, password hashing, and user dependency.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_settings
from src.database import get_db
from src.auth.models import User, RefreshToken

settings = get_settings()

TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_REFRESH = "refresh"

ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
REFRESH_TOKEN_EXPIRE_DAYS: int = 7

bearer_scheme = HTTPBearer(auto_error=False)


# ── password helpers ──────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


# ── JWT helpers ───────────────────────────────────────────────────────

def _create_token(data: dict, expires_delta: timedelta, token_type: str) -> str:
    now = datetime.now(timezone.utc)
    to_encode = data.copy()
    to_encode.update({
        "jti": uuid4().hex,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def create_access_token(user_id: str | UUID) -> str:
    return _create_token(
        data={"sub": str(user_id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type=TOKEN_TYPE_ACCESS,
    )


def create_refresh_token(user_id: str | UUID) -> str:
    return _create_token(
        data={"sub": str(user_id)},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        token_type=TOKEN_TYPE_REFRESH,
    )


def decode_token(token: str, expected_type: str) -> dict:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"],
            options={"require": ["exp", "sub", "type", "jti"]},
        )
    except JWTError:
        raise
    if payload.get("type") != expected_type:
        raise JWTError("Invalid token type")
    return payload


# ── refresh-token DB helpers (accept explicit db session) ─────────────

async def store_refresh_token(
    db: AsyncSession, user_id: str | UUID, jti: str, expires_at: datetime,
) -> None:
    # Ensure naive UTC datetime for TIMESTAMP WITHOUT TIME ZONE column
    if expires_at.tzinfo is not None:
        expires_at = expires_at.replace(tzinfo=None)
    record = RefreshToken(user_id=str(user_id), token_jti=jti, expires_at=expires_at)
    db.add(record)
    await db.commit()


async def revoke_refresh_token(db: AsyncSession, jti: str) -> bool:
    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token_jti == jti, RefreshToken.is_revoked == False
        )
    )
    record = result.scalar_one_or_none()
    if record:
        record.is_revoked = True
        await db.commit()
        return True
    return False


async def is_token_revoked(db: AsyncSession, jti: str) -> bool:
    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token_jti == jti, RefreshToken.is_revoked == True
        )
    )
    return result.scalar_one_or_none() is not None


# ── user dependency ───────────────────────────────────────────────────

async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_token(credentials.credentials, expected_type=TOKEN_TYPE_ACCESS)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token missing subject claim")

    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid user ID in token")

    result = await db.execute(
        select(User).where(User.id == str(user_uuid), User.is_active == True)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user
