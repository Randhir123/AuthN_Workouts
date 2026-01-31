"""Service B: resource server that verifies tokens via introspection."""
from __future__ import annotations

import os
from typing import Any

import httpx
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

INTROSPECT_URL = os.environ.get("WORKOUT18_INTROSPECT_URL")
RESOURCE_CLIENT_ID = os.environ.get("WORKOUT18_RESOURCE_CLIENT_ID")
RESOURCE_CLIENT_SECRET = os.environ.get("WORKOUT18_RESOURCE_CLIENT_SECRET")
EXPECTED_AUD = os.environ.get("WORKOUT18_EXPECTED_AUD")

if not INTROSPECT_URL or not RESOURCE_CLIENT_ID or not RESOURCE_CLIENT_SECRET:
    raise RuntimeError("Service B requires WORKOUT18_INTROSPECT_URL, *_CLIENT_ID, *_CLIENT_SECRET")

bearer_scheme = HTTPBearer(auto_error=False)
app = FastAPI(title="Workout 18 - Service B")


async def introspect_token(token: str) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.post(
            INTROSPECT_URL,
            data={"token": token},
            auth=(RESOURCE_CLIENT_ID, RESOURCE_CLIENT_SECRET),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    if resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Introspection failed: {resp.status_code}",
        )
    payload = resp.json()
    if not payload.get("active"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inactive",
        )
    if EXPECTED_AUD:
        audience = payload.get("aud")
        audiences = audience if isinstance(audience, list) else [audience]
        if EXPECTED_AUD not in audiences:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Audience mismatch",
            )
    return payload


async def require_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict[str, Any]:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )
    token = credentials.credentials
    return await introspect_token(token)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/data")
async def protected_endpoint(claims: dict[str, Any] = Depends(require_token)) -> dict[str, Any]:
    return {
        "message": "Service B trusted the token",
        "issuer": claims.get("iss"),
        "subject": claims.get("sub"),
        "aud": claims.get("aud"),
        "scopes": claims.get("scope"),
    }
