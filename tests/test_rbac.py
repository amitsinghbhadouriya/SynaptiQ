"""Unit tests for Role-Based Access Control logic."""

from backend.rbac import has_permission


def test_rbac_admin_permissions():
    assert has_permission("admin", "workspaces:delete") is True
    assert has_permission("admin", "evaluations:run") is True
    assert has_permission("admin", "settings:manage") is True


def test_rbac_viewer_permissions():
    assert has_permission("viewer", "workspaces:read") is True
    assert has_permission("viewer", "workspaces:delete") is False
    assert has_permission("viewer", "evaluations:run") is False
