"""Authenticate short-lived Workspace assertions at the modeling boundary."""

import re
from dataclasses import dataclass, field
from os import getenv
from typing import Self

import jwt

from .ports import Principal

_ALGORITHM = "HS256"
_ISSUER = "qopenbb-workspace"
_AUDIENCE = "qfm"
_TOKEN_TYPE = "qfm-identity"
_MAX_LIFETIME_SECONDS = 60
_BEARER = re.compile(r"Bearer +([A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]*)", re.IGNORECASE | re.ASCII)


class IdentityError(ValueError):
    """A missing or invalid identity assertion."""


@dataclass(frozen=True)
class IdentityVerifier:
    """Verify bearer assertions against the configured rotation key ring."""

    _keys: tuple[tuple[str, bytes], ...] = field(repr=False, default=())

    @classmethod
    def from_env(cls) -> Self:
        """Load the required current and optional previous KID/SECRET pairs."""
        try:
            current = _read_key("CURRENT")
            previous = _read_key("PREVIOUS")
        except (IdentityError, UnicodeError):
            return cls()
        if current is None:
            return cls()
        if previous is None:
            return cls((current,))
        if current[0] == previous[0]:
            return cls()
        return cls((current, previous))

    def authenticate(self, authorization: str | None) -> Principal:
        """Return the exact authenticated subject or raise a sanitized error."""
        bearer = _BEARER.fullmatch(authorization or "")
        if self._keys and bearer:
            try:
                return self._verify(bearer[1])
            except (jwt.PyJWTError, ValueError, TypeError, OverflowError, RecursionError):
                pass
        raise IdentityError("Invalid identity assertion")

    def _verify(self, token: str) -> Principal:
        header = jwt.get_unverified_header(token)
        if header.get("alg") != _ALGORITHM or header.get("typ") != _TOKEN_TYPE:
            raise IdentityError("Invalid identity assertion")
        key = dict(self._keys).get(header.get("kid"))
        if key is None:
            raise IdentityError("Invalid identity assertion")
        claims = jwt.decode(
            token,
            key,
            algorithms=[_ALGORITHM],
            issuer=_ISSUER,
            audience=_AUDIENCE,
            options={"require": ["iss", "aud", "sub", "iat", "exp"], "strict_aud": True},
        )
        issued, expires = claims["iat"], claims["exp"]
        if type(issued) is not int or type(expires) is not int or not 0 < expires - issued <= _MAX_LIFETIME_SECONDS:
            raise IdentityError("Invalid identity assertion")
        return Principal(subject=claims["sub"])


def _read_key(slot: str) -> tuple[str, bytes] | None:
    kid = getenv(f"QFM_IDENTITY_{slot}_KID")
    secret = getenv(f"QFM_IDENTITY_{slot}_SECRET")
    if kid is None and secret is None:
        return None
    if not kid or kid.split() != [kid] or not secret or secret.split() != [secret]:
        raise IdentityError("Invalid identity assertion")
    # The bridge and service use the same UTF-8 secret bytes. Provisioning supplies entropy.
    key = secret.encode("utf-8")
    if len(key) < 32:
        raise IdentityError("Invalid identity assertion")
    return kid, key
