"""Workout 4 backend with a protected endpoint that rejects by default."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


class PublicPayload(BaseModel):
    message: str
    workout: str


app = FastAPI(title="AuthN Workout 4")


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/public", response_model=PublicPayload)
async def public_endpoint() -> PublicPayload:
    return PublicPayload(message="Public hello", workout="protected-endpoint")


@app.get("/protected")
async def protected_endpoint() -> None:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Protected endpoint rejects all requests in workout 4",
    )
