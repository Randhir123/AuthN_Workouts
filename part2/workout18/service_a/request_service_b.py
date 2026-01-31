"""Service A: obtain a client_credentials token and call Service B."""
from __future__ import annotations

import os
import sys
from typing import Any

import requests

ISSUER = os.environ.get("WORKOUT18_ISSUER")
CLIENT_ID = os.environ.get("WORKOUT18_CLIENT_ID")
CLIENT_SECRET = os.environ.get("WORKOUT18_CLIENT_SECRET")
SERVICE_B_URL = os.environ.get("WORKOUT18_SERVICE_B_URL", "http://127.0.0.1:9000/data")
SCOPE = os.environ.get("WORKOUT18_SCOPE", "")

REQUIRED = [ISSUER, CLIENT_ID, CLIENT_SECRET]
if any(v is None for v in REQUIRED):
    sys.exit("WORKOUT18_ISSUER, WORKOUT18_CLIENT_ID, WORKOUT18_CLIENT_SECRET must be set")


def fetch_token() -> str:
    token_url = f"{ISSUER.rstrip('/')}/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    if SCOPE:
        payload["scope"] = SCOPE

    resp = requests.post(
        token_url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=payload,
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    token = data.get("access_token")
    if not token:
        raise RuntimeError(f"Token response missing access_token: {data}")
    return token


def call_service_b(token: str) -> dict[str, Any]:
    resp = requests.get(
        SERVICE_B_URL,
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def mask(token: str) -> str:
    if len(token) <= 16:
        return token
    return f"{token[:8]}…{token[-6:]}"


def main() -> None:
    token = fetch_token()
    print(f"Access token (masked): {mask(token)}")
    data = call_service_b(token)
    print("Service B response:")
    for key, value in data.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
