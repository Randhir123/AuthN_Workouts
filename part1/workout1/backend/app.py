"""Hello-world backend for AuthN workout 1 using FastAPI."""
from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="AuthN Workout 1")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Lightweight health-check endpoint."""
    return {"status": "ok"}


@app.get("/")
async def hello_world() -> dict[str, str]:
    """Return a plain hello-world payload."""
    return {"message": "Hello from workout 1", "workout": "hello-world-backend"}
