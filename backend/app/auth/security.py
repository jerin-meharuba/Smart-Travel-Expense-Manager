"""Password hashing and JWT helpers."""

from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, get_secret_key


ALGORITHM = "HS256"
password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Return an Argon2 password hash; plain passwords are never stored."""
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Check a plain password against its stored Argon2 hash."""
    return password_hasher.verify(password, password_hash)


def create_access_token(user_id: int) -> str:
    """Create a short-lived bearer token containing the user identifier."""
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expires_at}
    return jwt.encode(payload, get_secret_key(), algorithm=ALGORITHM)


def decode_access_token(token: str) -> int | None:
    """Return a token's user ID, or None when it is invalid or expired."""
    try:
        payload = jwt.decode(token, get_secret_key(), algorithms=[ALGORITHM])
        subject = payload.get("sub")
        return int(subject) if subject is not None else None
    except (jwt.PyJWTError, TypeError, ValueError):
        return None
