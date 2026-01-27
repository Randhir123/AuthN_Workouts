"""Small lab script for inspecting and verifying JWTs."""
from __future__ import annotations

import argparse
import base64
import json
from datetime import datetime, timezone
from typing import Any

from jose import JWTError, jwt


def _b64url_decode(data: str) -> bytes:
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def decode_command(token: str) -> None:
    try:
        header_b64, payload_b64, signature_b64 = token.split('.')
    except ValueError as exc:
        raise SystemExit('Token must have three parts separated by "."') from exc

    header = json.loads(_b64url_decode(header_b64))
    payload = json.loads(_b64url_decode(payload_b64))
    signature = _b64url_decode(signature_b64).hex()

    print('Header:')
    print(json.dumps(header, indent=2))
    print('\nPayload:')
    print(json.dumps(payload, indent=2))
    print('\nSignature (hex):')
    print(signature)


def verify_command(token: str, secret: str, algorithm: str, audience: str | None, issuer: str | None) -> None:
    try:
        claims = jwt.decode(
            token,
            secret,
            algorithms=[algorithm],
            audience=audience,
            issuer=issuer,
        )
    except JWTError as exc:
        raise SystemExit(f'Verification failed: {exc}') from exc

    print('Token verified successfully.')
    print(json.dumps(claims, indent=2))

    if 'exp' in claims:
        exp = datetime.fromtimestamp(int(claims['exp']), tz=timezone.utc)
        print(f"Expires at: {exp.isoformat()}")


def main() -> None:
    parser = argparse.ArgumentParser(description='JWT inspection lab tool')
    subparsers = parser.add_subparsers(dest='command', required=True)

    decode_parser = subparsers.add_parser('decode', help='Decode header/payload without verifying')
    decode_parser.add_argument('--token', required=True, help='JWT string')

    verify_parser = subparsers.add_parser('verify', help='Verify signature and claims')
    verify_parser.add_argument('--token', required=True, help='JWT string')
    verify_parser.add_argument('--secret', required=True, help='Shared secret or key')
    verify_parser.add_argument('--algorithm', default='HS256', help='JWT signing algorithm (default HS256)')
    verify_parser.add_argument('--audience', help='Expected audience claim')
    verify_parser.add_argument('--issuer', help='Expected issuer claim')

    args = parser.parse_args()

    if args.command == 'decode':
        decode_command(args.token)
    else:
        verify_command(args.token, args.secret, args.algorithm, args.audience, args.issuer)


if __name__ == '__main__':
    main()
