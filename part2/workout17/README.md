# Workout 17 — Breaking Trust Intentionally

## What we’re doing

Deliberately cause token verification to fail and observe how IBM Security Verify responds.

## Why this matters

Security is defined by failure modes, not success paths. A system that accepts invalid tokens is broken, regardless of how well valid tokens work. This workout confirms that verification fails correctly when tokens, credentials, or context are wrong.

## What we actually do

Reuse the OAuth2 introspection endpoint from Workout 16, but intentionally introduce errors.

### Case 1 — Introspect with an invalid token

```bash
curl -s -X POST "https://randhirapp.verify.ibm.com/oauth2/introspect" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -u "<CLIENT_ID>:<CLIENT_SECRET>" \
  -d "token=not-a-real-token" | jq
```

**Actual result:**
```json
{"active":false}
```

### Case 2 — Wrong client credentials

```bash
curl -s -X POST "https://randhirapp.verify.ibm.com/oauth2/introspect" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -u "wrong:credentials" \
  -d "token=T6tLpFrQQ0uqN5We5x4Kh-LY66ifIZZ87Z0h4izhx8Y.I0QBdfHpYWxmT8116CNqc8g9urTy4wcu6CfkZC6goG62n2iyqod7StrYZ39j0oSOgwKlV6rH5xGmANnn-jhCyQ.M18xNzY5NzcxOTA5XzUw" | jq
```

**Actual result:**
```json
{"error":"request_unauthorized","error_description":"CSIAQ0155E The requested OAuth 2.0 Client could not be authenticated."}
```

### Case 3 — Expired token

Wait for the token to expire (or craft one with a short lifetime), then introspect it again:

```bash
curl -s -X POST "https://randhirapp.verify.ibm.com/oauth2/introspect" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -u "<CLIENT_ID>:<CLIENT_SECRET>" \
  -d "token=<EXPIRED_ACCESS_TOKEN>" | jq
```
**Actual result:**
```json
{"active":false}
```
