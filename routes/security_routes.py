"""Security API routes.

This module provides authentication endpoints for user login
and retrieving the current authenticated user.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config.db import get_db_conn
from schemas.token import Token
from auth.security import pwd_context, create_access_token, authenticate_user, decode_access_token, get_user_principal
from fastapi.security import OAuth2PasswordBearer
from models import User
from typing import Annotated

router = APIRouter(
    prefix="/security",
    tags=["Security"],
    responses={404: {"description": "Not found"}},
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/security/token")

@router.post("/token", response_model=Token)
async def login_for_access_token(login: str, pwd: str, db: Session = Depends(get_db_conn)) -> Token:
    """Authenticate user and return a JWT access token.

    Args:
        login: Username for authentication.
        pwd: Password for authentication.
        db: Database session.

    Returns:
        Token object containing the access token and token type.

    Raises:
        HTTPException: 401 error if credentials are invalid.
    """
    user = await authenticate_user(login, pwd, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(access_token=await create_access_token(data={"sub": user.username}), token_type="bearer")


@router.get("/users/me", response_model=User)
async def get_user_me(user: Annotated[User, Depends(get_user_principal)]) -> User:
    """Get the current authenticated user's profile.

    Args:
        user: The authenticated user from the JWT token.

    Returns:
        The current user's profile information.
    """
    return user

