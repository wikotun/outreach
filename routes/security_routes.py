from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config.db import get_db_conn
from schemas.token import Token
from auth.security import pwd_context, create_access_token, authenticate_user
from models import User
router = APIRouter(
    prefix="/security",
    tags=["Security"],
    responses={404: {"description": "Not found"}},
)


@router.post("/token", response_model=Token)
async def login_for_access_token(login: str, pwd: str):
    user = authenticate_user(login, pwd)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(access_token=create_access_token(data={"sub": user.username}), token_type="bearer")
