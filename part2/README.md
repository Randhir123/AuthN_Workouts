# Part 2 — Introducing an Identity Provider: IBM Security Verify

In Part 1 we stripped authentication down to its essence: cryptographic statements carried over HTTP. No passwords, no sessions, no identity providers—just signed facts and verification rules. Part 2 introduces a real Identity Provider (IdP) and shows what fundamentally changes when token issuance, key management, and authentication policy are delegated to a managed system.

We use **IBM Security Verify** because it mirrors the landscape many teams operate in: a SaaS identity platform that is secure by default, policy-driven, and deliberately constrained. This part is about understanding the boundary between applications and identity, and learning to trust tokens as independently verifiable facts rather than opaque artifacts issued by a black box.

| # | Title | Focus |
|---|-------|-------|
| 11 | [Meeting the Identity Provider](workout11/README.md) | Orientation inside the IBM Security Verify console (no changes yet). |
| 12 | [The Issuer Exists Before Any App](workout12/README.md) | Discover the Verify issuer and its OIDC metadata before configuring apps. |
| 13 | [Understanding Keys Without Seeing Them](workout13/README.md) | Fetch the JWKS and inspect Verify's published signing keys. |
| 14 | [Creating a Service Identity (API Client)](workout14/README.md) | Create a Client Credentials API client for non-human identity. |
| 15 | [Minting the First Token](workout15/README.md) | Request a client_credentials token and inspect its claims. |
| 16 | [Verifying an Opaque Token via Introspection](workout16/README.md) | Call the introspection endpoint to validate reference tokens. |
| 17 | [Breaking Trust Intentionally](workout17/README.md) | Deliberately cause introspection failures and observe responses. |
| 18 | [Service-to-Service Trust Without Identity](workout18/README.md) | Service A fetches a token, Service B verifies via Verify introspection. |
