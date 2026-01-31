# Workout 13 — Understanding Keys Without Seeing Them

## What we’re doing

Inspect IBM Security Verify’s published signing keys via JWKS (JSON Web Key Set) to understand how trust is established without exposing private keys.

## Why it matters

The Identity Provider never shares private keys. Applications trust Verify because it publishes public keys that can be cached and verified independently. Seeing the JWKS reinforces that Verify is a cryptographic authority, not a session broker.

## Actions

1. Copy the `jwks_uri` from the discovery document you fetched in Workout 12.
2. Fetch the JWKS:

   ```bash
   curl <jwks_uri>
   ```

3. Observe the key material:
   - `kid` values (key IDs used in JWT headers)
   - `kty`, `alg`, `use` (key type, algorithm, usage)

Document what you see (number of keys, rotation hints, etc.). This confirms that Verify exposes the necessary public material for independent signature verification.

### Field reference

- `kid`: Key ID; JWT headers reference this so verifiers know which public key to use.
- `kty`: Key type (e.g., `RSA`).
- `alg`: Default signing algorithm for the key (e.g., `RS256`).
- `use`: Intended usage (`sig` = signature).
- `n`, `e`: RSA modulus and exponent—together they form the public key.
- `x5c`: (optional) X.509 certificate chain containing the same public key; useful for TLS-style validation or debugging.

### Example output

```json
{
  "keys": [
    {
      "kid": "server",
      "kty": "RSA",
      "use": "sig",
      "alg": "RS256",
      "n": "uYOH5LjlOqJWnI3dFSsP8Y8hZoAnY0FYMfez3BT1RHD3MUzGJLEEg6F6Lv_H6yvTAga7vU53yYZCKphJYGi3Pp-il1RSnrD3A56Y4LJx-8ycGhdH3iviuaRXbWPjPBnn94SD-_0wph_k64lWKGy0nz0mrkJv_J4_J-9oWqNdDD3QGxJsfbSeagB-eR-2s-n5V5490Y5_w27KRWhxEXDUEnyBL5OgfiSces3PLavxAL0b5Yp9YMupKLNijtMEaFO3Sb1F44VFelJq6HgXQ_ls-4JveHzlX0Co4AcnhmxNQRk7PnBssfOxyV0qWX14Hx3SUI5k-b8U5xsxn-gtb2f99Q",
      "e": "AQAB",
      "x5c": [
        "MIIDMjCCAhqgAwIBAgIEA5drbTANBgkqhkiG9w0BAQsFADBbMQkwBwYDVQQGEwAxCTAHBgNVBAgTADEJMAcGA1UEBxMAMQkwBwYDVQQKEwAxCTAHBgNVBAsTADEiMCAGA1UEAxMZcmFuZGhpcmFwcC52ZXJpZnkuaWJtLmNvbTAeFw0yNTA2MTcxNTA4MDVaFw0zNTA2MTUxNTA4MDVaMFsxCTAHBgNVBAYTADEJMAcGA1UECBMAMQkwBwYDVQQHEwAxCTAHBgNVBAoTADEJMAcGA1UECxMAMSIwIAYDVQQDExlyYW5kaGlyYXBwLnZlcmlmeS5pYm0uY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuYOH5LjlOqJWnI3dFSsP8Y8hZoAnY0FYMfez3BT1RHD3MUzGJLEEg6F6Lv/H6yvTAga7vU53yYZCKphJYGi3Pp+il1RSnrD3A56Y4LJx+8ycGhdH3iviuaRXbWPjPBnn94SD+/0wph/k64lWKGy0nz0mrkJv/J4/J+9oWqNdDD3QGxJsfbSeagB+eR+2s+n5V5490Y5/w27KRWhxEXDUEnyBL5OgfiSces3PLavxAL0b5Yp9YMupKLNijtMEaFO3Sb1F44VFelJq6HgXQ/ls+4JveHzlX0Co4AcnhmxNQRk7PnBssfOxyV0qWX14Hx3SUI5k+b8U5xsxn+gtb2f99QIDAQABMA0GCSqGSIb3DQEBCwUAA4IBAQCi0DVU5+A5XI9GPl2pN5RNVP6zr/4EpbGyL7dDqSh7rP6KS2edKfg0ZYxYCNpY3WHA8vnL3dtw5YiTDqcxt7fm84pVKjxFtj2D0LF4p+Oe+St98zM77RXa/aEY9HeIVAlznJ5nI0I5sG7Efqc8//P+qQmokVi8gjagaR2UMeu0IrFucX1DPQWZVz4nR26MB8ZfhYIzEdemuvZN3RuzikS7Sc7Xn5q0UVerXlcJeGAnUcj5KNKbsZ+xF/bzYgFrrrf57bZqcxufS//F+aOWsmVLH0azgVO5MkOe+DpE9yku4QWOnaSh3l9klpq9UZDZVZSR202YUin3583LlP1lrVfx"
      ]
    }
  ]
}
```

This sample is from `https://randhirapp.verify.ibm.com/oauth2/jwks`. Your tenant will emit similar fields (potentially with multiple keys), reinforcing that trust flows from published public keys.
