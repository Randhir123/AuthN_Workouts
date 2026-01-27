"""Workout 10 backend demonstrating key rotation and failure modes."""
from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Any, Dict

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

EXPECTED_ISSUER = os.environ.get("WORKOUT10_ISSUER", "https://demo-issuer")
EXPECTED_AUDIENCE = os.environ.get("WORKOUT10_AUDIENCE", "workout10-api")
JWKS_PATH = os.environ.get("WORKOUT10_JWKS_PATH")
JWKS_INLINE = os.environ.get("WORKOUT10_JWKS_JSON")

bearer_scheme = HTTPBearer(auto_error=False)
app = FastAPI(title="AuthN Workout 10")


def _load_jwks() -> Dict[str, Dict[str, Any]]:
    """Load JWKS from file or inline JSON."""
    if JWKS_INLINE:
        raw = json.loads(JWKS_INLINE)
    elif JWKS_PATH:
        with open(JWKS_PATH, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    else:
        return {}
    return {key["kid"]: key for key in raw.get("keys", []) if key.get("use") in {None, "sig"}}


@lru_cache(maxsize=1)
def get_jwks_cache() -> Dict[str, Dict[str, Any]]:
    return _load_jwks()


def signature_from_jwk(token: str) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        header = jwt.get_unverified_header(token)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token header",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    kid = header.get("kid")
    if not kid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing kid header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    jwks = get_jwks_cache()
    key = jwks.get(kid)
    if not key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unknown signing key: {kid}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return header, key


class ProtectedPayload(BaseModel):
    message: str
    key_id: str
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
    header, key = signature_from_jwk(token)
    alg = header.get("alg")

    try:
        claims = jwt.decode(
            token,
            key,
            algorithms=[alg],
            audience=EXPECTED_AUDIENCE,
            issuer=EXPECTED_ISSUER,
        )
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    claims["_kid"] = key["kid"]
    return claims


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/admin/reload-keys")
async def reload_keys() -> dict[str, str]:
    get_jwks_cache.cache_clear()
    get_jwks_cache()
    return {"status": "reloaded"}


@app.get("/protected", response_model=ProtectedPayload)
async def protected_endpoint(claims: dict[str, Any] = Depends(verify_token)) -> ProtectedPayload:
    key_id = claims.pop("_kid", "unknown")
    return ProtectedPayload(
        message="Protected action succeeded",
        key_id=key_id,
        claims=claims,
    )
