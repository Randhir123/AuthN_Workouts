"""Workout 6 backend that treats tokens as assertions."""
from __future__ import annotations

import os
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

EXPECTED_ISSUER = os.environ.get("WORKOUT6_ISSUER", "https://example-issuer")
EXPECTED_AUDIENCE = os.environ.get("WORKOUT6_AUDIENCE", "workout6-api")
TOKEN_SECRET = os.environ.get("WORKOUT6_TOKEN_SECRET", "workout6-demo-secret")
TOKEN_ALGORITHM = os.environ.get("WORKOUT6_TOKEN_ALG", "HS256")

bearer_scheme = HTTPBearer(auto_error=False)
app = FastAPI(title="AuthN Workout 6")


class PublicPayload(BaseModel):
    message: str
    workout: str


class ProtectedPayload(BaseModel):
    message: str
    workout: str
    claims: dict[str, Any]


async def verify_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict[str, Any]:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        claims = jwt.decode(
            token,
            TOKEN_SECRET,
            algorithms=[TOKEN_ALGORITHM],
            audience=EXPECTED_AUDIENCE,
            issuer=EXPECTED_ISSUER,
        )
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return claims


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/public", response_model=PublicPayload)
async def public_endpoint() -> PublicPayload:
    return PublicPayload(message="Public hello", workout="token-assertions")


@app.get("/protected", response_model=ProtectedPayload)
async def protected_endpoint(claims: dict[str, Any] = Depends(verify_token)) -> ProtectedPayload:
    return ProtectedPayload(
        message="Protected action performed",
        workout="token-assertions",
        claims=claims,
    )
