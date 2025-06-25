from datetime import datetime, timedelta, timezone
from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
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
    return pwd_context.hash(password)


def verify_password(plain_pwd, hash_pwd) -> bool:
    return pwd_context.verify(plain_pwd, hash_pwd)


async def authenticate_user(uname: str, password: str, db: Session):
    user = (
        db.query(User)
        .filter(User.username == uname)
        .first()
    )

    if not user or not verify_password(
            password, user.password
    ):
        return None
    return user


async def create_access_token(data: dict) -> str:
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


async def decode_access_token(token: str, db: Session) -> User:
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
    user = user_routes.find_user(username, db)
    print(f"Found user: {user}")
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = user_routes.find_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user


async def get_user_principal(current_user: Annotated[User, Depends(get_current_user)]):
    print(f"Current user: {current_user}")
    return current_user
