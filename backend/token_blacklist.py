"""Token revocation blacklist and active session tracking store."""

from __future__ import annotations

import time
import threading
from typing import Set, Dict


class TokenBlacklist:
    def __init__(self):
        self._blacklisted_jtis: Dict[str, int] = {}
        self._lock = threading.Lock()

    def revoke(self, jti: str, exp: int) -> None:
        """Mark a token JTI as revoked until its expiration epoch."""
        with self._lock:
            self._blacklisted_jtis[jti] = exp

    def is_revoked(self, jti: str) -> bool:
        """Check if a token has been explicitly revoked."""
        with self._lock:
            if jti not in self._blacklisted_jtis:
                return False
            if time.time() > self._blacklisted_jtis[jti]:
                del self._blacklisted_jtis[jti]
                return False
            return True

    def purge_expired(self) -> int:
        """Purge entries whose expiration time has elapsed."""
        now = time.time()
        with self._lock:
            initial = len(self._blacklisted_jtis)
            self._blacklisted_jtis = {
                k: v for k, v in self._blacklisted_jtis.items() if v > now
            }
            return initial - len(self._blacklisted_jtis)


token_blacklist = TokenBlacklist()
