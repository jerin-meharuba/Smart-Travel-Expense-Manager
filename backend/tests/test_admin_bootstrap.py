"""Tests for the interactive administrator provisioning command."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.admin.bootstrap import provision_admin
from app.auth.models import User
from app.auth.security import verify_password


def test_provision_admin_creates_normalized_admin_with_hashed_password() -> None:
    engine = create_engine("sqlite://")
    User.__table__.create(engine)

    with Session(engine) as db, db.begin():
        user, created = provision_admin(db, " Admin@Hotmail.com ", "strong-test-password")

        assert created is True
        assert user.email == "admin@hotmail.com"
        assert user.role == "admin"
        assert user.password_hash != "strong-test-password"
        assert verify_password("strong-test-password", user.password_hash)

    engine.dispose()


def test_provision_admin_promotes_existing_user_and_replaces_password() -> None:
    engine = create_engine("sqlite://")
    User.__table__.create(engine)

    with Session(engine) as db, db.begin():
        existing_user = User(
            email="admin@hotmail.com",
            password_hash="old-hash",
            role="user",
        )
        db.add(existing_user)
        db.flush()

        user, created = provision_admin(db, "admin@hotmail.com", "new-test-password")

        assert created is False
        assert user.role == "admin"
        assert user.password_hash != "old-hash"
        assert verify_password("new-test-password", user.password_hash)

    engine.dispose()
