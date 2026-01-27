# Workout 7 — JWT Structure and Signatures

In this workout we stop treating the token as an opaque blob. Instead we open it, inspect every part, and verify the signature deliberately. Headers, payloads, and signatures become first-class—we reason about how integrity is enforced and how it can fail if verification is sloppy.

You can reuse tokens from Workout 6 or mint new ones. The point is to understand exactly what the backend is trusting when `/protected` accepts a request.

---

## Goals

- Decode JWT headers and payloads without validating to see what is being asserted.
- Verify signatures manually to understand what the backend *should* be doing.
- Experiment with failure modes (wrong secret, mismatched `alg`, tampered payload) to see how easy it is to get verification wrong.

---

## Tooling provided

`part1/workout7/tools/jwt_lab.py` is a small script with two subcommands:

1. `decode` — splits the JWT, base64url-decodes the header/payload, and prints them as JSON without verifying.
2. `verify` — verifies the signature using the symmetric key from Workout 6 (or any key you provide) and prints the resulting claims.

Install dependencies (same as Workout 6) and run:

```bash
cd part1/workout7/tools
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Decode without verifying
python jwt_lab.py decode --token "$TOKEN"

# Verify using HS256 secret
python jwt_lab.py verify --token "$TOKEN" --secret "$WORKOUT6_TOKEN_SECRET"
```

Flags:

- `--secret` — symmetric key (required for `verify`).
- `--algorithm` — defaults to `HS256`.
- `--audience`, `--issuer` — optional checks to mirror backend behavior.

---

## Exercises

1. **Inspect the header** — what `alg` and `kid` are present? If someone changed `alg` to `none`, would your backend catch it?
2. **Tamper with the payload** — edit the payload JSON (e.g., change `sub`) and re-encode it. Can you produce a token that still decrypts but fails signature validation? Use the script to confirm.
3. **Wrong key** — verify with the wrong secret. Observe the exact exception raised. What would your backend return?
4. **Expired token** — change `exp` to the past and verify. Ensure the verifier actually checks expiration.

Document what you learn; the next workouts will rely on this mental model to reason about key rotation, multiple algorithms, and IdP integration.
