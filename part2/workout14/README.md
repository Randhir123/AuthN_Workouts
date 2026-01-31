# Workout 14 — Creating a Service Identity (API Client)

## What we’re doing

Create an API client using the Client Credentials grant—no users, no UI. This introduces non-human identity in IBM Security Verify.

## Why it matters

OAuth is not about login; it’s about delegation. Service-to-service interactions need their own identities, and the Client Credentials grant provides that without user involvement.

## Console actions

1. Navigate to **Security → API access → API clients** in the Verify admin console.
2. Click **Add API client**.
3. Name the client (e.g., `workout14-service`).
4. Enable the **Client Credentials** grant.
5. Save and record the generated **Client ID** and **Client Secret**.
6. Do not configure redirects or users—this client is for machine authentication only.

Store the Client ID/Secret securely; you’ll use them in upcoming workouts to request tokens.
