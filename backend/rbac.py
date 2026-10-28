"""Role-Based Access Control (RBAC) enforcement and permission levels."""

from __future__ import annotations

from typing import Set, Dict

ROLE_PERMISSIONS: Dict[str, Set[str]] = {
    "admin": {
        "workspaces:read", "workspaces:write", "workspaces:delete",
        "evaluations:run", "evaluations:read", "evaluations:delete",
        "settings:manage", "users:manage"
    },
    "evaluator": {
        "workspaces:read", "workspaces:write",
        "evaluations:run", "evaluations:read"
    },
    "viewer": {
        "workspaces:read",
        "evaluations:read"
    }
}


def has_permission(role: str, permission: str) -> bool:
    """Verifies if the specified role possesses the given permission flag."""
    return permission in ROLE_PERMISSIONS.get(role, set())
