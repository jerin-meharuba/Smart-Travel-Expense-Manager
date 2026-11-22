"""Interactive command for creating or promoting an administrator account."""

from getpass import getpass

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.admin.schemas import AdminUserCreate
from app.auth.models import User
from app.auth.security import hash_password
from app.database import SessionLocal


def provision_admin(db: Session, email: str, password: str) -> tuple[User, bool]:
    """Create an admin or promote the matching account and replace its password."""
    data = AdminUserCreate(email=email, password=password, role="admin")
    user = db.scalar(select(User).where(User.email == data.email))
    created = user is None

    if user is None:
        user = User(email=data.email, password_hash=hash_password(data.password), role="admin")
        db.add(user)
    else:
        user.password_hash = hash_password(data.password)
        user.role = "admin"

    db.flush()
    return user, created


def main() -> None:
    """Prompt for credentials and provision an admin in the configured database."""
    print("This will create or promote an account in the database configured by DATABASE_URL.")
    print("If the email already exists, its password will be replaced.")
    if input("Continue? [y/N]: ").strip().lower() != "y":
        print("Cancelled.")
        return

    email = input("Admin email: ")
    password = getpass("Admin password: ")
    if password != getpass("Confirm admin password: "):
        raise SystemExit("Passwords do not match.")

    try:
        data = AdminUserCreate(email=email, password=password, role="admin")
    except ValidationError:
        raise SystemExit("Invalid email or password. Use a valid email and a password of 8 to 128 characters.")

    with SessionLocal.begin() as db:
        user, created = provision_admin(db, data.email, data.password)
        admin_email = user.email

    action = "Created" if created else "Promoted/updated"
    print(f"{action} administrator account: {admin_email}")


if __name__ == "__main__":
    main()
