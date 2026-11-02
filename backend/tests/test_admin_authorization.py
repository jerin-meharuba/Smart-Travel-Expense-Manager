"""Focused tests for the shared administrator authorization boundary."""

import pytest
from fastapi import HTTPException

from app.auth.dependencies import require_admin
from app.auth.models import User


def test_regular_user_is_rejected_from_admin_routes() -> None:
    regular_user = User(id=1, email="user@example.com", password_hash="hash", role="user")

    with pytest.raises(HTTPException) as error:
        require_admin(regular_user)

    assert error.value.status_code == 403


def test_administrator_is_accepted_for_admin_routes() -> None:
    administrator = User(id=2, email="admin@example.com", password_hash="hash", role="admin")

    assert require_admin(administrator) is administrator
