import hashlib
import hmac


def make_hmac(secret: bytes, payload: str) -> str:
    return hmac.new(secret, payload.encode("utf-8"), hashlib.sha256).hexdigest()


def test_hmac_deterministic() -> None:
    sig1 = make_hmac(b"secret", "{\"a\":1}")
    sig2 = make_hmac(b"secret", "{\"a\":1}")
    assert sig1 == sig2


def test_hmac_changes_with_payload() -> None:
    sig1 = make_hmac(b"secret", "{\"a\":1}")
    sig2 = make_hmac(b"secret", "{\"a\":2}")
    assert sig1 != sig2
