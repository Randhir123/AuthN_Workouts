# Workout 12 — The Issuer Exists Before Any App

## What we’re doing

Locate IBM Security Verify’s issuer identity and retrieve its OpenID Connect discovery document. This establishes the root of trust before any application is configured.

## Why it matters

The issuer is the root of trust. Applications do not trust Verify because they are manually configured to; they trust it because its identity and metadata are globally discoverable and cryptographically stable.

## Steps

1. Identify your tenant base URL (example: `https://randhirapp.verify.ibm.com`).
2. Construct the issuer URL: `https://<tenant>.verify.ibm.com/oauth2`.
3. Fetch the discovery document:

   ```bash
   curl https://<tenant>.verify.ibm.com/oauth2/.well-known/openid-configuration
   ```

4. Record the following fields from the JSON output:
   - `issuer`
   - `authorization_endpoint`
   - `token_endpoint`
   - `jwks_uri`

   Example values:

   ```json
   {
     "issuer": "https://randhirapp.verify.ibm.com/oauth2",
     "authorization_endpoint": "https://randhirapp.verify.ibm.com/oauth2/authorize",
     "token_endpoint": "https://randhirapp.verify.ibm.com/oauth2/token",
     "jwks_uri": "https://randhirapp.verify.ibm.com/oauth2/jwks"
   }
   ```

No console clicks are required—this workout is about recognizing that the issuer’s metadata exists independently of any application configuration.
