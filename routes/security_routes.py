from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config.db import get_db_conn
from schemas.token import Token
from auth.security import pwd_context, create_access_token, authenticate_user,decode_access_token
from fastapi.security import OAuth2PasswordBearer
from models import User

router = APIRouter(
    prefix="/security",
    tags=["Security"],
    responses={404: {"description": "Not found"}},
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/security/token")

@router.post("/token", response_model=Token)
async def login_for_access_token(login: str, pwd: str,db: Session = Depends(get_db_conn)):


    user = await authenticate_user(login, pwd,db)


    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(access_token = await create_access_token(data={"sub": user.username}), token_type="bearer")


@router.get("/users/me", response_model=User)
async def get_current_user(token: str,db: Session = Depends(get_db_conn)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = await decode_access_token(token,db)

    if user is None:
        raise credentials_exception
    return user
