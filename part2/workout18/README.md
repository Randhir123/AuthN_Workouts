# Workout 18 — Service-to-Service Trust Without Identity

This workout closes the trust triangle. Service A (a backend client) authenticates to IBM Security Verify with the Client Credentials grant, receives an access token, and calls Service B (a resource server). Service B does **not** trust Service A directly; it delegates verification to the IdP by introspecting the token before processing the request.

## Why it matters

Machine-to-machine authentication often precedes human identity, claims, or sessions. By wiring a resource server to an external issuer, we show how delegation works in practice: tokens are proof because the issuer says so, not because services hard-code shared secrets.

## Components

- **Service A** (`service_a/request_service_b.py`): CLI script that fetches a client_credentials token and calls Service B with it.
- **Service B** (`service_b/app.py`): FastAPI app that requires `Authorization: Bearer <token>`, verifies the token via Verify’s `/oauth2/introspect`, and returns a response only when the token is active.

## Setup

1. Ensure you have a client in IBM Security Verify with the Client Credentials grant enabled (Workout 14). Note its Client ID/Secret.
2. Export the following variables for Service A:
   ```bash
   export WORKOUT18_ISSUER="https://<tenant>.verify.ibm.com/oauth2"
   export WORKOUT18_CLIENT_ID="<CLIENT_ID>"
   export WORKOUT18_CLIENT_SECRET="<CLIENT_SECRET>"
   export WORKOUT18_SERVICE_B_URL="http://127.0.0.1:9000/data"
   ```
3. Export variables for Service B (can reuse the same client credentials for introspection or use a dedicated resource server client):
   ```bash
   export WORKOUT18_INTROSPECT_URL="https://<tenant>.verify.ibm.com/oauth2/introspect"
   export WORKOUT18_RESOURCE_CLIENT_ID="<CLIENT_ID>"
   export WORKOUT18_RESOURCE_CLIENT_SECRET="<CLIENT_SECRET>"
   export WORKOUT18_EXPECTED_AUD="<CLIENT_ID>"  # optional audience check
   ```

## Running Service B

```bash
cd part2/workout18/service_b
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 9000 --reload
```

## Running Service A

In another terminal:

```bash
cd part2/workout18/service_a
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python request_service_b.py
```

Example request (Service A -> Service B):

```bash
curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:9000/data
```

Example response from Service B:

```json
{
  "message": "Service B trusted the token",
  "issuer": "https://randhirapp.verify.ibm.com/oauth2",
  "subject": "<CLIENT_ID>",
  "aud": ["<CLIENT_ID>"],
  "scopes": null
}
```

The script prints the access token (masked) and the response from Service B. If Service B rejects the token, you’ll see the exact reason (inactive token, invalid signature, etc.). Example:

```
Access token (masked): cace6X_X…QyXzUw
Service B response:
  message: Service B trusted the token
  issuer: https://randhirapp.verify.ibm.com/oauth2
  subject: <CLIENT_ID>
  aud: ['<CLIENT_ID>']
  scopes: None
```


## Notes

- Service B delegates trust to Verify by calling `/oauth2/introspect`. Swap in JWT verification later to avoid the network hop.
- Service A and Service B *usually* have different client credentials in production. We reuse the same Verify client here purely for simplicity.
- No human identity is involved—this pattern is pure delegation between services.
