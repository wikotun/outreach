from fastapi import APIRouter, Depends, HTTPException, status
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

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = authenticate_user(login, pwd)
    token_str = create_access_token(data={"sub": login})

    print("token str: "+ token_str)
    return
