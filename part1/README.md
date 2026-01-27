# Part I — Requests, Tokens, and Trust Boundaries

Part I contains workouts 1–10. They start with a “hello world” backend, then progressively add trust boundaries, protected endpoints, and token mechanics until we reach key rotation. Every folder under `part1/` is self-contained; follow the README in each workout for details.

## Workouts

| # | Title | Focus |
|---|-------|-------|
| 1 | [Hello-world backend (no auth)](workout1/README.md) | Minimal FastAPI backend serving responses without authentication. |
| 2 | [A Client That Can Call the Backend](workout2/README.md) | Browser as caller to observe the unauthenticated boundary. |
| 3 | [Trust Boundaries and CORS](workout3/README.md) | Make origins explicit with CORS allow-lists. |
| 4 | [Introducing a Protected Endpoint](workout4/README.md) | First hard "no"—endpoint now rejects by default. |
| 5 | [What Are We Actually Protecting?](workout5/README.md) | Document the meaning and impact of the protected action. |
| 6 | [Introducing Tokens as Assertions](workout6/README.md) | Treat tokens as verifiable claims using symmetric JWTs. |
| 7 | [JWT Structure and Signatures](workout7/README.md) | Inspect headers/payloads/signatures and verify them manually. |
| 8 | [Verifying Tokens Correctly](workout8/README.md) | Enforce algorithm pinning, signature checks, and descriptive failures. |
| 9 | [Expiry, Replay, and Time](workout9/README.md) | Handle `exp`/`nbf` plus prevent token replay via `jti`. |
| 10 | [Key Rotation and Failure Modes](workout10/README.md) | Accept multiple signing keys and simulate rotation errors. |

## How to navigate

```bash
# Example: run Workout 6 backend
cd part1/workout6/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Each workout builds on the mental model of the previous one, so read them sequentially. Once these foundations make sense, you’re ready for Part II (identity providers, delegation, etc.).
