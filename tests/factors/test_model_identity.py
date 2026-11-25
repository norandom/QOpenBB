from time import time

import jwt
import pytest
from qopenbb_data.modeling.service.identity import IdentityError, IdentityVerifier
from qopenbb_data.modeling.service.ports import Principal

CURRENT = "0123456789abcdef" * 4
PREVIOUS = "fedcba9876543210" * 4
ENV = {
    "QFM_IDENTITY_CURRENT_KID": "active",
    "QFM_IDENTITY_CURRENT_SECRET": CURRENT,
    "QFM_IDENTITY_PREVIOUS_KID": "retiring",
    "QFM_IDENTITY_PREVIOUS_SECRET": PREVIOUS,
}


@pytest.fixture
def identity_env(monkeypatch):
    for name in ENV:
        monkeypatch.delenv(name, raising=False)
    return monkeypatch


@pytest.fixture
def verifier(identity_env):
    for name, value in ENV.items():
        identity_env.setenv(name, value)
    return IdentityVerifier.from_env()


def assertion(*, claims=None, headers=None, algorithm="HS256", secret=CURRENT):
    now = int(time())
    payload = {
        "iss": "qopenbb-workspace", "aud": "qfm", "sub": "user-18",
        "iat": now - 1, "exp": now + 59,
    }
    for name, value in (claims or {}).items():
        if value is None:
            payload.pop(name)
        else:
            payload[name] = value
    header = {"kid": "active", "typ": "qfm-identity"} | (headers or {})
    if header["kid"] is None:
        del header["kid"]
    return jwt.encode(payload, secret, algorithm=algorithm, headers=header)


@pytest.mark.parametrize(("kid", "secret"), [("active", CURRENT), ("retiring", PREVIOUS)])
def test_authenticates_pinned_key(verifier, kid, secret):
    token = assertion(headers={"kid": kid}, secret=secret)
    assert verifier.authenticate(f"bEaReR {token}") == Principal(subject="user-18")
    assert secret not in repr(verifier)


@pytest.mark.parametrize("separator", ["\n", "\t", "\N{NO-BREAK SPACE}"])
def test_rejects_invalid_bearer_separator(verifier, separator):
    with pytest.raises(IdentityError):
        verifier.authenticate(f"Bearer{separator}{assertion()}")


def test_rotation_is_optional(identity_env):
    for name, value in ENV.items():
        if "_CURRENT_" in name:
            identity_env.setenv(name, value)
    verifier = IdentityVerifier.from_env()
    assert verifier.authenticate(f"Bearer {assertion()}").subject == "user-18"
    with pytest.raises(IdentityError):
        verifier.authenticate(f"Bearer {assertion(headers={'kid': 'retiring'}, secret=PREVIOUS)}")


@pytest.mark.parametrize(
    "overrides",
    [
        {"QFM_IDENTITY_CURRENT_KID": None, "QFM_IDENTITY_CURRENT_SECRET": None,
         "QFM_IDENTITY_PREVIOUS_KID": None, "QFM_IDENTITY_PREVIOUS_SECRET": None},
        {"QFM_IDENTITY_CURRENT_KID": None},
        {"QFM_IDENTITY_CURRENT_SECRET": None},
        {"QFM_IDENTITY_CURRENT_KID": " "},
        {"QFM_IDENTITY_CURRENT_SECRET": "short"},
        {"QFM_IDENTITY_CURRENT_SECRET": " " * 64},
        {"QFM_IDENTITY_PREVIOUS_KID": None},
        {"QFM_IDENTITY_PREVIOUS_SECRET": None},
        {"QFM_IDENTITY_PREVIOUS_SECRET": "short"},
        {"QFM_IDENTITY_PREVIOUS_KID": "active"},
    ],
)
def test_invalid_configuration_fails_closed_at_use(identity_env, overrides):
    for name, value in (ENV | overrides).items():
        if value is not None:
            identity_env.setenv(name, value)
    verifier = IdentityVerifier.from_env()
    with pytest.raises(IdentityError, match="^Invalid identity assertion$"):
        verifier.authenticate(f"Bearer {assertion()}")


@pytest.mark.parametrize("authorization", [None, "", "Bearer", "Bearer ", "Basic abc", "Bearer a b", "Bearer nonsense"])
def test_rejects_bad_authorization(verifier, authorization):
    with pytest.raises(IdentityError):
        verifier.authenticate(authorization)


@pytest.mark.parametrize(
    "headers",
    [
        {"kid": None}, {"kid": ""}, {"kid": "third"}, {"kid": "retiring"},
        {"typ": None}, {"typ": "JWT"}, {"typ": "wrong-type"},
    ],
)
def test_rejects_bad_header(verifier, headers):
    with pytest.raises(IdentityError):
        verifier.authenticate(f"Bearer {assertion(headers=headers)}")


@pytest.mark.parametrize(("algorithm", "secret"), [("HS256", PREVIOUS), ("HS384", CURRENT), ("none", None)])
def test_rejects_wrong_signature_or_algorithm(verifier, algorithm, secret):
    with pytest.raises(IdentityError):
        verifier.authenticate(f"Bearer {assertion(algorithm=algorithm, secret=secret)}")


@pytest.mark.parametrize(
    "claims",
    [
        {"iss": None}, {"iss": "other"}, {"aud": None}, {"aud": "other"}, {"aud": ["qfm", "other"]},
        {"sub": None}, {"sub": ""}, {"sub": " "}, {"sub": 42}, {"sub": "x" * 129},
        {"iat": None}, {"iat": "1"}, {"iat": []}, {"iat": True}, {"iat": 1.5},
        {"exp": None}, {"exp": "1"}, {"exp": {}}, {"exp": True}, {"exp": 1.5},
        {"nbf": {}},
    ],
)
def test_rejects_invalid_claims(verifier, claims):
    token = assertion(claims=claims)
    with pytest.raises(IdentityError, match="^Invalid identity assertion$") as failure:
        verifier.authenticate(f"Bearer {token}")
    assert failure.value.__context__ is None


@pytest.mark.parametrize(
    ("issued_offset", "expiry_offset"),
    [(-61, -1), (-61, 0), (5, 20), (0, 0), (-2, -3), (-1, 60)],
)
def test_rejects_invalid_time_window(verifier, issued_offset, expiry_offset):
    now = int(time())
    token = assertion(claims={"iat": now + issued_offset, "exp": now + expiry_offset})
    with pytest.raises(IdentityError):
        verifier.authenticate(f"Bearer {token}")
