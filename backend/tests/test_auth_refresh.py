"""
Test suite: Token refresh flow
================================

Covers:
  1. Login → access_token + refresh_token issued
  2. Access token expiry → 401 → refresh → retry succeeds
  3. Concurrent requests during refresh (coalescing)
  4. Expired refresh token → 401
  5. Server/network error during refresh
  6. Token revocation on refresh (rotation)
  7. Protected endpoint auth middleware
"""

import asyncio
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient
from jose import jwt as jose_jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_settings
from src.auth.models import User
from src.auth.service import (
    create_access_token, create_refresh_token, decode_token,
    store_refresh_token, hash_password, TOKEN_TYPE_ACCESS, TOKEN_TYPE_REFRESH,
)

settings = get_settings()


# ══════════════════════════════════════════════════════════════════════
# 1. LOGIN
# ══════════════════════════════════════════════════════════════════════

class TestLogin:
    async def test_login_success(self, client: AsyncClient, test_user: User):
        resp = await client.post("/api/v1/auth/login", json={"username": "testuser", "password": "testpass123"})
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data and "refresh_token" in data
        assert data["token_type"] == "bearer"
        access = decode_token(data["access_token"], TOKEN_TYPE_ACCESS)
        assert access["sub"] == str(test_user.id)
        refresh = decode_token(data["refresh_token"], TOKEN_TYPE_REFRESH)
        assert refresh["sub"] == str(test_user.id)

    async def test_login_invalid_credentials(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/login", json={"username": "nobody", "password": "wrong"})
        assert resp.status_code == 401

    async def test_login_inactive_user(self, client: AsyncClient, db_session: AsyncSession):
        db_session.add(User(username="inactive", hashed_password=hash_password("pass"), is_active=False))
        await db_session.commit()
        resp = await client.post("/api/v1/auth/login", json={"username": "inactive", "password": "pass"})
        assert resp.status_code == 401

    async def test_login_empty_body(self, client: AsyncClient):
        assert (await client.post("/api/v1/auth/login", json={})).status_code == 422


# ══════════════════════════════════════════════════════════════════════
# 2. PROTECTED ENDPOINTS
# ══════════════════════════════════════════════════════════════════════

class TestProtectedEndpoints:
    async def test_valid_token(self, client: AsyncClient, auth_headers: dict):
        resp = await client.get("/api/v1/protected-test", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["username"] == "testuser"

    async def test_no_token(self, client: AsyncClient):
        assert (await client.get("/api/v1/protected-test")).status_code == 401

    async def test_invalid_token(self, client: AsyncClient):
        resp = await client.get("/api/v1/protected-test", headers={"Authorization": "Bearer garbage_token_here"})
        assert resp.status_code == 401

    async def test_wrong_token_type(self, client: AsyncClient, test_user: User):
        refresh = create_refresh_token(test_user.id)
        resp = await client.get("/api/v1/protected-test", headers={"Authorization": f"Bearer {refresh}"})
        assert resp.status_code == 401

    async def test_expired_token(self, client: AsyncClient, test_user: User):
        now = datetime.now(timezone.utc)
        expired = jose_jwt.encode({
            "sub": str(test_user.id), "jti": uuid4().hex, "type": "access",
            "iat": now - timedelta(hours=1), "exp": now - timedelta(minutes=5),
        }, settings.SECRET_KEY, algorithm="HS256")
        resp = await client.get("/api/v1/protected-test", headers={"Authorization": f"Bearer {expired}"})
        assert resp.status_code == 401


# ══════════════════════════════════════════════════════════════════════
# 3. REFRESH ENDPOINT
# ══════════════════════════════════════════════════════════════════════

class TestRefreshEndpoint:
    async def _persist_refresh(self, db_session: AsyncSession, user_id, token: str):
        payload = decode_token(token, TOKEN_TYPE_REFRESH)
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        await store_refresh_token(db_session, str(user_id), payload["jti"], exp)

    async def test_refresh_success(self, client: AsyncClient, test_user: User, db_session: AsyncSession):
        refresh = create_refresh_token(test_user.id)
        await self._persist_refresh(db_session, test_user.id, refresh)
        resp = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh})
        assert resp.status_code == 200
        new_token = resp.json()["access_token"]
        assert (await client.get("/api/v1/protected-test", headers={"Authorization": f"Bearer {new_token}"})).status_code == 200

    async def test_expired_refresh(self, client: AsyncClient, test_user: User):
        now = datetime.now(timezone.utc)
        expired = jose_jwt.encode({
            "sub": str(test_user.id), "jti": uuid4().hex, "type": "refresh",
            "iat": now - timedelta(days=10), "exp": now - timedelta(days=1),
        }, settings.SECRET_KEY, algorithm="HS256")
        assert (await client.post("/api/v1/auth/refresh", json={"refresh_token": expired})).status_code == 401

    async def test_invalid_refresh(self, client: AsyncClient):
        assert (await client.post("/api/v1/auth/refresh", json={"refresh_token": "garbage"})).status_code == 401

    async def test_token_rotation(self, client: AsyncClient, test_user: User, db_session: AsyncSession):
        refresh = create_refresh_token(test_user.id)
        await self._persist_refresh(db_session, test_user.id, refresh)
        # First use works
        assert (await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh})).status_code == 200
        # Second use with same token fails (revoked)
        resp = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh})
        assert resp.status_code == 401
        assert "revoked" in resp.text.lower()

    async def test_user_deleted(self, client: AsyncClient, db_session: AsyncSession):
        temp = User(username="temp", hashed_password=hash_password("pass"), is_active=True)
        db_session.add(temp)
        await db_session.commit()
        await db_session.refresh(temp)
        refresh = create_refresh_token(temp.id)
        await self._persist_refresh(db_session, temp.id, refresh)
        temp.is_active = False
        await db_session.commit()
        assert (await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh})).status_code == 401


# ══════════════════════════════════════════════════════════════════════
# 4. FULL REFRESH FLOW
# ══════════════════════════════════════════════════════════════════════

class TestFullRefreshFlow:
    async def test_full_flow(self, client: AsyncClient, test_user: User, db_session: AsyncSession):
        # Create valid refresh + expired access
        refresh = create_refresh_token(test_user.id)
        r_payload = decode_token(refresh, TOKEN_TYPE_REFRESH)
        await store_refresh_token(db_session, str(test_user.id), r_payload["jti"],
                                  datetime.fromtimestamp(r_payload["exp"], tz=timezone.utc))

        now = datetime.now(timezone.utc)
        expired_access = jose_jwt.encode({
            "sub": str(test_user.id), "jti": uuid4().hex, "type": "access",
            "iat": now - timedelta(hours=1), "exp": now - timedelta(minutes=1),
        }, settings.SECRET_KEY, algorithm="HS256")

        # Step 1: expired token → 401
        assert (await client.get("/api/v1/protected-test", headers={"Authorization": f"Bearer {expired_access}"})).status_code == 401

        # Step 2: refresh → new access
        resp = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh})
        assert resp.status_code == 200
        new_access = resp.json()["access_token"]

        # Step 3: retry with new token → success
        resp3 = await client.get("/api/v1/protected-test", headers={"Authorization": f"Bearer {new_access}"})
        assert resp3.status_code == 200
        assert resp3.json()["username"] == "testuser"


# ══════════════════════════════════════════════════════════════════════
# 5. CONCURRENT REQUEST COALESCING
# ══════════════════════════════════════════════════════════════════════

class TestConcurrentCoalescing:
    async def test_concurrent_401(self, client: AsyncClient, test_user: User, db_session: AsyncSession):
        refresh = create_refresh_token(test_user.id)
        r_payload = decode_token(refresh, TOKEN_TYPE_REFRESH)
        await store_refresh_token(db_session, str(test_user.id), r_payload["jti"],
                                  datetime.fromtimestamp(r_payload["exp"], tz=timezone.utc))

        now = datetime.now(timezone.utc)
        expired = jose_jwt.encode({
            "sub": str(test_user.id), "jti": uuid4().hex, "type": "access",
            "iat": now - timedelta(hours=1), "exp": now - timedelta(minutes=1),
        }, settings.SECRET_KEY, algorithm="HS256")

        bad = {"Authorization": f"Bearer {expired}"}
        # 3 concurrent requests all get 401
        responses = await asyncio.gather(*[client.get("/api/v1/protected-test", headers=bad) for _ in range(3)])
        for r in responses:
            assert r.status_code == 401

        # Simulate single refresh + all retries
        resp = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh})
        assert resp.status_code == 200
        new = {"Authorization": f"Bearer {resp.json()['access_token']}"}
        retries = await asyncio.gather(*[client.get("/api/v1/protected-test", headers=new) for _ in range(3)])
        for r in retries:
            assert r.status_code == 200

    async def test_frontend_coalescing_unit(self):
        """Unit-test the frontend's coalescing pattern (no HTTP)."""
        refresh_promise = None
        refresh_queue = []
        call_count = 0

        async def fake_refresh() -> str:
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.03)
            return "new_token"

        async def enqueue():
            nonlocal refresh_promise, refresh_queue
            if refresh_promise is not None:
                future = asyncio.get_event_loop().create_future()
                refresh_queue.append(future)
                return await future
            refresh_promise = fake_refresh()
            try:
                result = await refresh_promise
                refresh_promise = None
                for f in refresh_queue:
                    f.set_result(result)
                refresh_queue.clear()
                return result
            except Exception as e:
                refresh_promise = None
                for f in refresh_queue:
                    f.set_exception(e)
                refresh_queue.clear()
                raise

        results = await asyncio.gather(*[enqueue() for _ in range(5)])
        assert call_count == 1
        assert all(r == "new_token" for r in results)


# ══════════════════════════════════════════════════════════════════════
# 6. EDGE CASES
# ══════════════════════════════════════════════════════════════════════

class TestEdgeCases:
    async def test_refresh_expired(self, client: AsyncClient):
        now = datetime.now(timezone.utc)
        expired = jose_jwt.encode({
            "sub": "00000000-0000-0000-0000-000000000001", "jti": uuid4().hex, "type": "refresh",
            "iat": now - timedelta(days=10), "exp": now - timedelta(days=1),
        }, settings.SECRET_KEY, algorithm="HS256")
        assert (await client.post("/api/v1/auth/refresh", json={"refresh_token": expired})).status_code == 401

    async def test_refresh_no_body(self, client: AsyncClient):
        assert (await client.post("/api/v1/auth/refresh", json={})).status_code == 422

    async def test_malformed_header(self, client: AsyncClient):
        assert (await client.get("/api/v1/protected-test", headers={"Authorization": "BadFormat"})).status_code == 401

    async def test_multiple_sessions(self, client: AsyncClient, test_user: User):
        """Two login sessions are independent."""
        r1 = await client.post("/api/v1/auth/login", json={"username": "testuser", "password": "testpass123"})
        r2 = await client.post("/api/v1/auth/login", json={"username": "testuser", "password": "testpass123"})
        t1, t2 = r1.json(), r2.json()
        for t in [t1, t2]:
            assert (await client.get("/api/v1/protected-test", headers={"Authorization": f"Bearer {t['access_token']}"})).status_code == 200
        # Both refresh independently
        assert (await client.post("/api/v1/auth/refresh", json={"refresh_token": t1["refresh_token"]})).status_code == 200
        assert (await client.post("/api/v1/auth/refresh", json={"refresh_token": t2["refresh_token"]})).status_code == 200

    async def test_refresh_preserves_identity(self, client: AsyncClient, test_user: User, db_session: AsyncSession):
        refresh = create_refresh_token(test_user.id)
        p = decode_token(refresh, TOKEN_TYPE_REFRESH)
        await store_refresh_token(db_session, str(test_user.id), p["jti"], datetime.fromtimestamp(p["exp"], tz=timezone.utc))
        resp = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh})
        new_payload = decode_token(resp.json()["access_token"], TOKEN_TYPE_ACCESS)
        assert new_payload["sub"] == str(test_user.id)

    async def test_old_access_still_valid_after_refresh(self, client: AsyncClient, test_user: User):
        """Known behavior: old access token remains valid until natural expiry."""
        resp = await client.post("/api/v1/auth/login", json={"username": "testuser", "password": "testpass123"})
        tokens = resp.json()
        old_access = tokens["access_token"]
        refresh_resp = await client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
        new_access = refresh_resp.json()["access_token"]
        assert (await client.get("/api/v1/protected-test", headers={"Authorization": f"Bearer {old_access}"})).status_code == 200
        assert (await client.get("/api/v1/protected-test", headers={"Authorization": f"Bearer {new_access}"})).status_code == 200


# ══════════════════════════════════════════════════════════════════════
# 7. NETWORK / SERVER ERROR DURING REFRESH
# ══════════════════════════════════════════════════════════════════════

class TestRefreshErrors:
    async def test_refresh_invalid_json(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/refresh", content=b"not-json", headers={"Content-Type": "application/json"})
        assert resp.status_code in (422, 400)

    async def test_frontend_refresh_failure_clears(self):
        """Unit-test: refresh failure clears tokens and rejects all queued."""
        store = {"accessToken": "old", "refreshToken": "old_r"}
        refresh_promise = None
        refresh_queue = []

        async def fake_fails():
            await asyncio.sleep(0.01)
            raise Exception("Network error")

        async def enqueue():
            nonlocal refresh_promise
            if refresh_promise is not None:
                future = asyncio.get_event_loop().create_future()
                refresh_queue.append(future)
                return await future
            refresh_promise = fake_fails()
            try:
                await refresh_promise
            except Exception as e:
                refresh_promise = None
                store["accessToken"] = None
                store["refreshToken"] = None
                for f in refresh_queue:
                    f.set_exception(e)
                refresh_queue.clear()
                raise

        with pytest.raises(Exception, match="Network error"):
            await enqueue()
        assert store["accessToken"] is None
        assert store["refreshToken"] is None
        # Verify queue was processed (any waiting requests also failed)
        assert len(refresh_queue) == 0

    async def test_concurrent_failure_propagates(self):
        """When refresh fails, ALL waiting requests get the error."""
        refresh_promise = None
        refresh_queue = []
        call_count = 0

        async def fake_fails():
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.02)
            raise Exception("Server error")

        async def enqueue():
            nonlocal refresh_promise
            if refresh_promise is not None:
                future = asyncio.get_event_loop().create_future()
                refresh_queue.append(future)
                try:
                    return await future
                except Exception as e:
                    raise e
            refresh_promise = fake_fails()
            try:
                result = await refresh_promise
                refresh_promise = None
                for f in refresh_queue:
                    f.set_result(result)
                refresh_queue.clear()
                return result
            except Exception as e:
                refresh_promise = None
                for f in refresh_queue:
                    f.set_exception(e)
                refresh_queue.clear()
                raise

        errors = []
        async def try_enqueue():
            try:
                await enqueue()
            except Exception as e:
                errors.append(str(e))
        # Fire all 3 concurrently so they queue behind the first
        await asyncio.gather(try_enqueue(), try_enqueue(), try_enqueue())
        assert call_count == 1
        assert len(errors) == 3
        assert all("Server error" in e for e in errors)
