# Workout 6 — Introducing Tokens as Assertions

In Workout 6, a token is treated as just a signed statement attached to a request. Nothing more. It could be hand-generated, locally signed, issued by your own code, or even a mock. The crucial mindset shift: **a token is not identity**; it’s a claim that must be verified.

This workout exists to break the shortcut “token = user logged in.” Instead, the token is “an assertion that something is allowed to happen, *if and only if* it verifies correctly.” Only after internalizing that idea does it make sense to hook up a real IdP.

---

## Token model for this workout

To stay focused on the authorization boundary (and not on an IdP), we use a symmetric signing key that represents whatever trusted issuer your system might eventually have. Rules:

1. Tokens are JWTs signed with `HS256` using a shared secret.
2. Each token must contain `iss`, `aud`, `sub`, and `exp` claims.
3. The backend verifies signature, issuer, audience, and expiration before accepting `/protected`.

### Generating a demo token

```bash
cd part1/workout6/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export WORKOUT6_TOKEN_SECRET="change-me"
export WORKOUT6_ISSUER="https://demo-issuer"
export WORKOUT6_AUDIENCE="workout6-api"

python - <<'PY'
from datetime import datetime, timedelta, timezone
from jose import jwt

secret = 'change-me'
claims = {
    'iss': 'https://demo-issuer',
    'aud': 'workout6-api',
    'sub': 'user-123',
    'scope': 'demo.read',
    'exp': datetime.now(timezone.utc) + timedelta(minutes=5)
}
print(jwt.encode(claims, secret, algorithm='HS256'))
PY
```

Copy the printed token value into `$TOKEN` for the curl example below.

---

## Backend quickstart

```bash
cd part1/workout6/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export WORKOUT6_TOKEN_SECRET="change-me"
export WORKOUT6_ISSUER="https://demo-issuer"
export WORKOUT6_AUDIENCE="workout6-api"
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Optional env vars: `WORKOUT6_TOKEN_ALG` (default `HS256`).

---

## Endpoints

- `GET /health` — returns `{ "status": "ok" }`.
- `GET /public` — returns a hello-world payload without needing a token.
- `GET /protected` — requires an `Authorization: Bearer <token>` header. Verification steps:
  - signature matches `WORKOUT6_TOKEN_SECRET`
  - `iss` equals `WORKOUT6_ISSUER`
  - `aud` contains `WORKOUT6_AUDIENCE`
  - token is not expired

Example call after generating `$TOKEN`:

```bash
curl -i \
  -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/protected
```

The response body echoes a subset of the validated claims so you can see what the token asserted.

---

## Framing tokens as assertions

- A token **asserts** that an actor may invoke `/protected`. The backend accepts the request *only if* it can verify that assertion.
- In this workout the signing key stands in for whatever trusted issuer you might use later. The backend never trusts a token by default; it checks the signature, issuer, audience, expiry, and any additional claims you decide to enforce.
- Later workouts can plug in a full Identity Provider or map claims to roles/scopes. For now, the presence of a valid, verifiable token is enough to flip the `/protected` decision from "always no" to "yes when verified".
