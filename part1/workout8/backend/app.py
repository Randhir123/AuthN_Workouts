"""Workout 8 backend that enforces strict token verification."""
from __future__ import annotations

import os
from datetime import timedelta
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError
from pydantic import BaseModel

TOKEN_SECRET = os.environ.get("WORKOUT8_TOKEN_SECRET", "workout8-demo-secret")
TOKEN_ALG = os.environ.get("WORKOUT8_TOKEN_ALG", "HS256")
EXPECTED_ISSUER = os.environ.get("WORKOUT8_ISSUER", "https://demo-issuer")
EXPECTED_AUDIENCE = os.environ.get("WORKOUT8_AUDIENCE", "workout8-api")
LEEWAY_SECONDS = int(os.environ.get("WORKOUT8_LEEWAY_SECONDS", "30"))

bearer_scheme = HTTPBearer(auto_error=False)
app = FastAPI(title="AuthN Workout 8")


class ProtectedPayload(BaseModel):
    message: str
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
        header = jwt.get_unverified_header(token)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token header",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    alg = header.get("alg")
    if alg != TOKEN_ALG:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unexpected alg {alg}; expected {TOKEN_ALG}",
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Claim verification failed: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except JWTError as exc:
        detail = "Signature verification failed" if "Signature verification failed" in str(exc) else "Token verification failed"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return claims


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/protected", response_model=ProtectedPayload)
async def protected_endpoint(claims: dict[str, Any] = Depends(verify_token)) -> ProtectedPayload:
    return ProtectedPayload(message="Protected action succeeded", claims=claims)
