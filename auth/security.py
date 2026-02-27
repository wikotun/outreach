"""Security and authentication utilities.

This module provides password hashing, JWT token creation/verification,
and user authentication functions for the application.
"""

from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from sqlmodel import Session, select
from config.db import get_db_conn
from config.app_config import settings
from models import User
from email_validator import validate_email, EmailNotValidError
from jose import jwt, JWTError
from routes import user_routes
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer


pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password: str) -> str:
    """Hash a plaintext password using bcrypt.

    Args:
        password: The plaintext password to hash.

    Returns:
        The bcrypt-hashed password string.
    """
    return pwd_context.hash(password)


def verify_password(plain_pwd: str, hash_pwd: str) -> bool:
    """Verify a plaintext password against a hashed password.

    Args:
        plain_pwd: The plaintext password to verify.
        hash_pwd: The hashed password to compare against.

    Returns:
        True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_pwd, hash_pwd)


async def authenticate_user(uname: str, password: str, db: Session) -> User | None:
    """Authenticate a user by username and password.

    Args:
        uname: The username to authenticate.
        password: The plaintext password to verify.
        db: Database session for querying user records.

    Returns:
        The User object if authentication succeeds, None otherwise.
    """
    user = db.exec(
        select(User).where(User.username == uname)
    ).first()

    if not user or not verify_password(
            password, user.password
    ):
        return None
    return user


async def create_access_token(data: dict) -> str:
    """Create a JWT access token.

    Args:
        data: Dictionary containing claims to encode in the token.
            Typically includes 'sub' (subject) with the username.

    Returns:
        The encoded JWT token string.
    """
    to_encode = data.copy()
    print(f"Token data to encode: {to_encode}")
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    print(f"Token expiration time: {expire}")

    to_encode.update({"exp": expire})
    print(f"Token data to encode: {to_encode}")

    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )
    print(f"Encoded JWT: {encoded_jwt}")
    return encoded_jwt


async def decode_access_token(token: str, db: Session) -> User | None:
    """Decode a JWT token and retrieve the associated user.

    Args:
        token: The JWT token string to decode.
        db: Database session for querying user records.

    Returns:
        The User object if token is valid and user exists, None otherwise.
    """
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=ALGORITHM
        )
        username: str = payload.get("sub")
        print(f"Decoded username: {username}")
    except JWTError:
        print("JWT Error: Invalid token")
        return None
    if not username:
        return None

    print(f"Finding user with username: {username}")
    user = await user_routes.find_user(username, db)
    print(f"Found user: {user}")
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db_conn)) -> User:
    """Get the current authenticated user from a JWT token.

    This is a FastAPI dependency that extracts and validates
    the JWT token from the request Authorization header.

    Args:
        token: JWT token extracted from the Authorization header.
        db: Database session for querying user records.

    Returns:
        The authenticated User object.

    Raises:
        HTTPException: 401 error if credentials are invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_routes.find_user(username, db)
    if user is None:
        raise credentials_exception
    return user


async def get_user_principal(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """Get the current user principal for authorization.

    This is a FastAPI dependency that wraps get_current_user
    and can be used for role-based access control.

    Args:
        current_user: The authenticated user from get_current_user.

    Returns:
        The authenticated User object.
    """
    print(f"Current user: {current_user}")
    return current_user
