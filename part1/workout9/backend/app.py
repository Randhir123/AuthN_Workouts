"""Workout 9 backend that enforces expiry, not-before, and replay detection."""
from __future__ import annotations

import os
import time
from datetime import timedelta
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError
from pydantic import BaseModel

TOKEN_SECRET = os.environ.get("WORKOUT9_TOKEN_SECRET", "workout9-demo-secret")
TOKEN_ALG = os.environ.get("WORKOUT9_TOKEN_ALG", "HS256")
EXPECTED_ISSUER = os.environ.get("WORKOUT9_ISSUER", "https://demo-issuer")
EXPECTED_AUDIENCE = os.environ.get("WORKOUT9_AUDIENCE", "workout9-api")
LEEWAY_SECONDS = int(os.environ.get("WORKOUT9_LEEWAY_SECONDS", "30"))

bearer_scheme = HTTPBearer(auto_error=False)
app = FastAPI(title="AuthN Workout 9")


class ProtectedPayload(BaseModel):
    message: str
    claims: dict[str, Any]


# In-memory replay cache: jti -> expiry timestamp
REPLAY_CACHE: dict[str, float] = {}


def purge_replay_cache() -> None:
    now = time.time()
    expired = [jti for jti, expiry in REPLAY_CACHE.items() if expiry <= now]
    for jti in expired:
        REPLAY_CACHE.pop(jti, None)


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
        header = jwt.get_unverified_header(token)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token header",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    if header.get("alg") != TOKEN_ALG:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unexpected alg {header.get('alg')}; expected {TOKEN_ALG}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        claims = jwt.decode(
            token,
            TOKEN_SECRET,
            algorithms=[TOKEN_ALG],
            audience=EXPECTED_AUDIENCE,
            issuer=EXPECTED_ISSUER,
            options={"leeway": timedelta(seconds=LEEWAY_SECONDS)},
        )
    except ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except JWTClaimsError as exc:
        detail = str(exc)
        if "NotBefore" in detail:
            detail = "Token not valid yet"
        else:
            detail = f"Claim verification failed: {detail}"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    jti = claims.get("jti")
    if not jti:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing jti claim",
            headers={"WWW-Authenticate": "Bearer"},
        )

    purge_replay_cache()
    now = time.time()
    expiry_ts = float(claims.get("exp", now))
    existing_expiry = REPLAY_CACHE.get(jti)
    if existing_expiry and existing_expiry > now:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Token replay detected",
            headers={"WWW-Authenticate": "Bearer"},
        )

    REPLAY_CACHE[jti] = expiry_ts

    return claims


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/protected", response_model=ProtectedPayload)
async def protected_endpoint(claims: dict[str, Any] = Depends(verify_token)) -> ProtectedPayload:
    return ProtectedPayload(message="Protected action succeeded", claims=claims)
