"""Unit tests for token revocation blacklist."""

import time
from backend.token_blacklist import TokenBlacklist


def test_token_blacklist_lifecycle():
    bl = TokenBlacklist()
    assert bl.is_revoked("jti_1") is False

    bl.revoke("jti_1", exp=int(time.time() + 10))
    assert bl.is_revoked("jti_1") is True

    # Expired token in blacklist
    bl.revoke("jti_2", exp=int(time.time() - 2))
    assert bl.is_revoked("jti_2") is False


def test_token_blacklist_purge():
    bl = TokenBlacklist()
    bl.revoke("active", exp=int(time.time() + 100))
    bl.revoke("dead", exp=int(time.time() - 10))
    purged = bl.purge_expired()
    assert purged == 1
    assert bl.is_revoked("active") is True
