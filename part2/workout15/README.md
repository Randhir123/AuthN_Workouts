# Workout 15 — Minting the First Token

## What we’re doing

Mint an access token using the Client Credentials grant and examine what kind of token the identity provider issues.

## What actually happens

IBM Security Verify issues an opaque access token for this client. The token represents delegated authority, but it does not expose its claims directly.

## Why it matters

At this point we learn a critical distinction: OAuth access tokens are not required to be JWTs. Some identity providers deliberately issue opaque tokens so that validation happens through the issuer rather than locally.

## Steps

1. Use the Client ID and Client Secret from Workout 14 to request a token:

   ```bash
   curl -X POST https://<tenant>.verify.ibm.com/oauth2/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=client_credentials&client_id=<CLIENT_ID>&client_secret=<CLIENT_SECRET>"
   ```

   Save the `access_token` from the JSON response.

2. Your token is an opaque access token. It’s designed specifically so you cannot read claims client-side. The IdP keeps the claims server-side and exposes them through introspection (and sometimes userinfo).
  ```bash
  curl -s -X POST "https://randhirapp.verify.ibm.com/oauth2/introspect" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -u "<CLIENT_ID>:<CLIENT_SECRET>" \
    -d "token=<ACCESS_TOKEN>" | jq
  ```
  Check the claims
   - `iss` (issuer)
   - `aud` (audience)
   - `exp` (expiration)
   - `sub` (subject — typically the client ID)

   Example response:

   ```json
   {
     "access_token": "Mp2L_9CrYGzqOZLaSb7zKdPkwL3rramLxXZLbtqVWjE.bbdB1yPaEM4mj5kWxQpf5PBigj4aKLVVIOgkT5r1lq1aOqEvlR9J8DGAYursXdgGvsfnUui9jocXZecB5Fc93A.M18xNzY5NjgwMzI4XzUw",
     "expires_in": 7199,
     "grant_id": "c609c265-4fbc-4245-a9f5-9ddb744c63e2",
     "scope": "",
     "token_type": "bearer"
   }
   ```

3. Note how these claims map back to the issuer metadata (Workout 12) and the service identity (Workout 14).

Keep the token handy—upcoming workouts will verify it against the JWKS and enforce authorization decisions.
