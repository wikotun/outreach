import datetime

from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from config.db import get_db_conn
from models import User
from email_validator import validate_email, EmailNotValidError
import os
from jose import jwt, JWTError
from routes import user_routes

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)


def authenticate_user(username_or_email: str, password: str, db: Session = Depends(get_db_conn)) -> User | None:
    try:
        validate_email(username_or_email)
        query_filter = User.email
    except EmailNotValidError:
        query_filter = User.username
    user = (
        db.query(User)
        .filter(query_filter == username_or_email)
        .first()
    )
    if not user or not pwd_context.verify(
            password, user.password
    ):
        return
    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    token_expiration_minutes: str | None = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    secret_key: str | None = os.getenv("SECRET_KEY")
    algorithm_type: str | None = os.getenv("ALGORITHM")
    expire = datetime.utcnow() + datetime.timedelta(
        minutes=token_expiration_minutes
    )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, secret_key, algorithm=algorithm_type
    )
    return encoded_jwt


def decode_access_token(token: str) -> User | None:
    try:
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
        )
        username: str = payload.get("sub")
    except JWTError:
        return
    if not username:
        return
    user = user_routes.find_user(username)
    return user
