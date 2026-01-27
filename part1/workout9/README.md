# Workout 9 — Expiry, Replay, and Time

Tokens that were valid once may no longer be valid now. In Workout 9 we treat time as an adversary: `exp`, `nbf`, and `jti` claims matter, and replayed tokens are rejected. Authentication is a continuous decision every time `/protected` runs.

---

## Objectives

1. Enforce expiration (`exp`) and not-before (`nbf`) explicitly, including clock-skew handling.
2. Track `jti` (token IDs) in memory to detect simple replay attempts.
3. Surface clear error codes when a token is expired, not-yet-valid, or replayed.

---

## Backend quickstart

```bash
cd part1/workout9/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export WORKOUT9_TOKEN_SECRET="change-me"
export WORKOUT9_ISSUER="https://demo-issuer"
export WORKOUT9_AUDIENCE="workout9-api"
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

---

## Endpoints

- `GET /health` — returns `{ "status": "ok" }`.
- `GET /protected` — requires a bearer token signed with the shared secret and containing `exp`, `nbf`, and `jti` claims. The server checks:
  - signature, issuer, audience (same as workout 8)
  - `nbf` <= now + skew
  - `exp` >= now - skew
  - `jti` has not been seen before (in-memory replay cache)

Replay detection stores each `jti` for the remaining lifetime of the token. Any subsequent request with the same `jti` is rejected with `409 Conflict`.

---

## Demo workflow

1. Mint a token with `exp` 2 minutes from now, `nbf` slightly in the past, and a unique `jti`:

```bash
python - <<'PY'
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from jose import jwt

secret = 'change-me'
claims = {
    'iss': 'https://demo-issuer',
    'aud': 'workout9-api',
    'sub': 'user-123',
    'scope': 'demo.read',
    'exp': datetime.now(timezone.utc) + timedelta(minutes=2),
    'nbf': datetime.now(timezone.utc) - timedelta(seconds=10),
    'jti': str(uuid4()),
}
print(jwt.encode(claims, secret, algorithm='HS256'))
PY
```

2. Call `/protected` twice:

```bash
curl -i -H "Authorization: Bearer $TOKEN" http://localhost:8000/protected
# 200 OK on first use

curl -i -H "Authorization: Bearer $TOKEN" http://localhost:8000/protected
# 409 Conflict with {"detail":"Token replay detected"}
```

3. Wait until `exp` and call again to see `401 Token expired`.

---

## Why time matters

- **Expiry** ensures a stolen token eventually stops working.
- **Not-before** lets you stage tokens for future actions but rejects premature use.
- **Replay tracking** proves that a token cannot simply be captured and reused indefinitely, forcing attackers to obtain fresh assertions.

Carry these mechanics forward—future workouts will integrate real storage or caches to persist replay protection beyond a single process.
