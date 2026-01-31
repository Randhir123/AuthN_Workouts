# Workout 16 — Verifying an Opaque Token via Introspection

## What we’re doing

Verify an opaque access token by calling IBM Security Verify’s OAuth 2.0 introspection endpoint.

## Why it matters

OAuth offers two verification models:

- **JWTs** — verified locally using JWKS.
- **Opaque tokens** — verified remotely via introspection.

Choosing between them has architectural consequences for latency, scaling, and trust boundaries. This workout introduces the introspection path so you experience the trade-offs firsthand.

## Steps

1. Obtain an opaque access token (e.g., from Workout 15 before switching to JWTs).
2. Call the introspection endpoint with those token values. Verify typically exposes it at `https://<tenant>.verify.ibm.com/oauth2/introspect`.

   ```bash
   curl -X POST https://<tenant>.verify.ibm.com/oauth2/introspect \
     -u <CLIENT_ID>:<CLIENT_SECRET> \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "token=<ACCESS_TOKEN>"
   ```

3. Inspect the JSON response. Look for fields like `active`, `sub`, `scope`, `exp`.
4. Note how this differs from JWT verification: the resource server must call Verify synchronously to confirm the token’s validity.

Document the latency and output to compare with JWT-based verification in later workouts.

### Example invocation

```bash
curl -s -X POST "https://randhirapp.verify.ibm.com/oauth2/introspect" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -u "<CLIENT_ID>:<CLIENT_SECRET>" \
  -d "token=Mp2L_9CrYGzqOZLaSb7zKdPkwL3rramLxXZLbtqVWjE.bbdB1yPaEM4mj5kWxQpf5PBigj4aKLVVIOgkT5r1lq1aOqEvlR9J8DGAYursXdgGvsfnUui9jocXZecB5Fc93A.M18xNzY5NjgwMzI4XzUw"
```

Sample response (fields truncated):

```json
{
  "active": true,
  "aud": ["<CLIENT_ID>"],
  "client_id": "<CLIENT_ID>",
  "exp": 1769779109,
  "grant_id": "9d9f6c19-8873-4694-b821-b86e424bd34e",
  "grant_type": "client_credentials",
  "iat": 1769771909,
  "iss": "https://randhirapp.verify.ibm.com/oauth2",
  "sub": "<CLIENT_ID>",
  "token_type": "bearer"
}
```

If the client credentials are missing or invalid, Verify returns `invalid_request` / `request_unauthorized` errors—introspection requires authenticated callers.
