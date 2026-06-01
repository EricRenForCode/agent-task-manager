"""
Auth router: login, refresh, and user-info endpoints.
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from src.database import get_db
from src.auth.models import User
from src.auth.schemas import (
    LoginRequest, TokenResponse, RefreshRequest, AccessTokenResponse, UserResponse,
)
from src.auth.service import (
    verify_password, decode_token, create_access_token, create_refresh_token,
    get_current_user, store_refresh_token, revoke_refresh_token, is_token_revoked,
    TOKEN_TYPE_REFRESH,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.username == body.username, User.is_active == True)
    )
    user = result.scalar_one_or_none()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    try:
        payload = decode_token(refresh_token, expected_type=TOKEN_TYPE_REFRESH)
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        await store_refresh_token(db, str(user.id), payload["jti"], exp)
    except JWTError:
        pass

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_access_token(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    try:
        payload = decode_token(body.refresh_token, expected_type=TOKEN_TYPE_REFRESH)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    jti = payload.get("jti")
    if not jti:
        raise HTTPException(status_code=401, detail="Token missing jti claim")

    if await is_token_revoked(db, jti):
        raise HTTPException(status_code=401, detail="Refresh token has been revoked")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token missing subject claim")

    result = await db.execute(
        select(User).where(User.id == user_id, User.is_active == True)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=401, detail="User not found or inactive")

    await revoke_refresh_token(db, jti)
    new_access_token = create_access_token(user_id)
    return AccessTokenResponse(access_token=new_access_token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=str(current_user.id), username=current_user.username,
        email=current_user.email, is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
    )
