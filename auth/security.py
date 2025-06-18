

from datetime import datetime,timedelta
from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from config.db import get_db_conn
from config.app_config import settings
from models import User
from email_validator import validate_email, EmailNotValidError
from jose import jwt, JWTError
from routes import user_routes


pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


async def authenticate_user(uname: str, password: str, db: Session):
    user = (
        db.query(User)
        .filter(User.username == uname)
        .first()
    )

    if not user or not pwd_context.verify(
            password, user.password
    ):
        return None
    return user


async def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now() + timedelta(
        minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


async def decode_access_token(token: str,db:Session) -> User:

    print(f"Decoding token: {token}")
    print(f"Using secret key: {SECRET_KEY}")
    print(f"Using algorithm: {ALGORITHM}")

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
    user = user_routes.find_user(username,db)
    print(f"Found user: {user}")
    return user
