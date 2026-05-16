import time

from app.core.config import get_settings
from app.core.security import create_auth_token, verify_auth_token


def test_auth_token_verifies_before_expiry(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_token_ttl_seconds", 10)
    monkeypatch.setattr(time, "time", lambda: 1000)
    token = create_auth_token("admin")

    monkeypatch.setattr(time, "time", lambda: 1009)

    assert verify_auth_token(token) == "admin"


def test_auth_token_expires_after_ttl(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "auth_token_ttl_seconds", 10)
    monkeypatch.setattr(time, "time", lambda: 1000)
    token = create_auth_token("admin")

    monkeypatch.setattr(time, "time", lambda: 1011)

    assert verify_auth_token(token) is None
