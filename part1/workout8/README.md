# Workout 8 — Verifying Tokens Correctly

A token is not enough by itself. In this workout we make verification explicit: signatures are checked, algorithms are constrained, and invalid tokens are rejected loudly. Authentication is about proving that the token in hand is valid for *this* request, *right now*.

---

## Verification rules enforced here

1. **Algorithm pinning** — only the expected algorithm is accepted. `alg="none"` or unexpected algorithms are rejected.
2. **Signature validation** — HMAC signatures are recomputed with the shared secret (from Workout 6) and compared in constant time.
3. **Issuer / audience / expiry** — all must match the configured values.
4. **Clock skew** — configurable leeway is applied so you can reason about real systems.
5. **Descriptive failures** — the backend surfaces which check failed (`alg`, signature, claims, expiry) to reinforce that each step happens independently.

---

## Backend quickstart

```bash
cd part1/workout8/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export WORKOUT8_TOKEN_SECRET="change-me"
export WORKOUT8_ISSUER="https://demo-issuer"
export WORKOUT8_AUDIENCE="workout8-api"
export WORKOUT8_LEEWAY_SECONDS=30
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Optional env vars: `WORKOUT8_TOKEN_ALG` (default `HS256`).

---

## Minting a compatible token

```bash
python - <<'PY'
from datetime import datetime, timedelta, timezone
from jose import jwt
secret = 'change-me'
claims = {
    'iss': 'https://demo-issuer',
    'aud': 'workout8-api',
    'sub': 'user-123',
    'scope': 'demo.read',
    'exp': datetime.now(timezone.utc) + timedelta(minutes=5)
}
print(jwt.encode(claims, secret, algorithm='HS256'))
PY
```

Copy the printed token into `$TOKEN` for the curl examples.

---

## Endpoints & curl examples

- `GET /health`

```bash
curl -i http://localhost:8000/health
```

- `GET /protected` (requires `Authorization: Bearer <token>`)

```bash
curl -i \
  -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/protected
```

### Failure demonstrations

Signature tampering:

```bash
BROKEN_TOKEN="${TOKEN}tamper"
curl -i \
  -H "Authorization: Bearer $BROKEN_TOKEN" \
  http://localhost:8000/protected
# HTTP/1.1 401 Unauthorized
# {"detail":"Signature verification failed"}
```

Wrong algorithm (change header to `HS512` and re-sign with same secret):

```bash
curl -i \
  -H "Authorization: Bearer $HS512_TOKEN" \
  http://localhost:8000/protected
# HTTP/1.1 401 Unauthorized
# {"detail":"Unexpected alg HS512; expected HS256"}
```

Expired token (set `exp` in the past):

```bash
curl -i \
  -H "Authorization: Bearer $EXPIRED_TOKEN" \
  http://localhost:8000/protected
# HTTP/1.1 401 Unauthorized
# {"detail":"Token expired"}
```

Audience mismatch:

```bash
curl -i \
  -H "Authorization: Bearer $WRONG_AUD_TOKEN" \
  http://localhost:8000/protected
# HTTP/1.1 401 Unauthorized
# {"detail":"Claim verification failed: Audience mismatch"}
```

Successful response shows the verified claims. Failures return the descriptive message shown.

---

## Suggested exercises

1. **Break the signature** — tamper with the payload and confirm the backend returns `Signature verification failed`.
2. **Wrong algorithm** — send a token with `alg=HS512` or `alg=none` and watch it fail before signature validation even runs.
3. **Expired token** — set `exp` in the past; toggle `WORKOUT8_LEEWAY_SECONDS` to see how skew affects acceptance.
4. **Missing claims** — remove `aud` or `iss` and confirm the backend raises `Claim verification failed`.
5. **Scope enforcement (optional)** — extend `protected_endpoint` to require `scope` or `sub` to match something specific.

Document what happens for each case so future workouts (introducing IdPs and multi-issuer scenarios) inherit a clear verification baseline.
