# Workout 10 — Key Rotation and Failure Modes

Part I ends by breaking assumptions. Signing keys rotate, tokens outlive those keys, and systems must survive the transition without either rejecting everyone or letting expired trust linger. Workout 10 shows why authentication fails in production and sets the stage for bringing in real Identity Providers.

---

## Objectives

1. Accept multiple signing keys at once (old + new) via a rotation-aware JWKS.
2. Reject tokens signed by keys that have been retired, even if they were once valid.
3. Surface clear failure paths when the verifier loses a key (e.g., rotated before the backend updated) versus when the token is genuinely invalid.
4. Demonstrate how refreshing JWKS or reloading secrets keeps the system alive.

---

## Scenario

- `kid=old-key` — legacy key that signed tokens issued before rotation; expires soon.
- `kid=new-key` — current signing key.
- `kid=retired-key` — key removed from the JWKS; any token referencing it must be rejected even if the signature math still works.

Tokens carry a `kid` header. The backend loads a JWKS (JSON Web Key Set) with all active keys and enforces `iss`/`aud`/`exp` like before. Rotation is simulated by editing the JWKS and reloading the app.

---

## Backend quickstart

```bash
cd part1/workout10/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export WORKOUT10_ISSUER="https://demo-issuer"
export WORKOUT10_AUDIENCE="workout10-api"
export WORKOUT10_JWKS_PATH="/absolute/path/to/jwks.json"
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

You can also set `WORKOUT10_JWKS_JSON` with the JWKS document inline. The backend caches keys but exposes `POST /admin/reload-keys` to re-read the JWKS, emulating a rotation event.

---

## JWKS example

```json
{
  "keys": [
    {
      "kty": "RSA",
      "kid": "old-key",
      "use": "sig",
      "alg": "RS256",
      "n": "...",
      "e": "AQAB"
    },
    {
      "kty": "RSA",
      "kid": "new-key",
      "use": "sig",
      "alg": "RS256",
      "n": "...",
      "e": "AQAB"
    }
  ]
}
```

To simulate retirement, remove `old-key` from the JWKS, call `/admin/reload-keys`, and try verifying an old token.

---

## Endpoints

- `GET /health` — sanity check.
- `GET /protected` — requires `Authorization: Bearer <token>` signed with any active key.
- `POST /admin/reload-keys` — refreshes the JWKS cache (no auth in this workout to keep focus on rotation mechanics).

---

## Exercises

1. **Valid old token** — sign with `old-key`, verify before rotation, then remove key and confirm the token fails with `Unknown signing key`.
2. **Race condition** — rotate to `new-key` but forget to call `/admin/reload-keys`; watch the backend reject new tokens until refreshed.
3. **Retired key compromise** — add a `retired-key` entry with `use=enc` only; ensure the backend refuses to use keys not marked for signatures.
4. **Multiple algorithms** — add an `ES256` key and ensure the backend rejects it if `alg` doesn’t match expectations.

Document how often the backend should refresh keys and what happens when it can’t. This closes Part I by showing that managing keys is non-trivial—and why IdPs exist to do it for us.
