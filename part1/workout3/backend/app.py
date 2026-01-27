"""Workout 3 backend that has an explicit trust boundary via CORS."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:8001",
    "http://localhost:8001",
]


class HelloPayload(BaseModel):
    message: str
    workout: str
    allowedOrigins: list[str]


app = FastAPI(title="AuthN Workout 3")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_model=HelloPayload)
async def hello_world() -> HelloPayload:
    return HelloPayload(
        message="Hello from workout 3",
        workout="cors-trust-boundary",
        allowedOrigins=ALLOWED_ORIGINS,
    )
