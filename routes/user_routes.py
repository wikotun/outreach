"""User API routes.

This module provides CRUD endpoints for managing user accounts.
"""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from config.db import get_db_conn
from models import User
from schemas.user import UserSchema, UserSchemaInput
from auth.security import get_password_hash
from schemas.role import Role

router = APIRouter(
    prefix="/user",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create", response_model=UserSchema, description="Creates a new user record in the database")
async def create_user(user: UserSchemaInput, db: Session = Depends(get_db_conn)) -> User:
    """Create a new user account.

    The password is hashed before storage and the user is assigned
    the MEMBER role by default.

    Args:
        user: User data for the new account.
        db: Database session.

    Returns:
        The created user with its generated id.
    """
    new_user = User(**user.model_dump())
    new_user.user_role = Role.MEMBER.value
    new_user.password = get_password_hash(user.password)
    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
    return new_user


@router.get("/read/{id}", response_model=UserSchema, description="Reads a user record from the database")
async def get_user(id: int, db: Session = Depends(get_db_conn)) -> User:
    """Retrieve a user by ID.

    Args:
        id: The user ID to retrieve.
        db: Database session.

    Returns:
        The requested user record.

    Raises:
        HTTPException: 404 error if user not found.
    """
    db_user = db.exec(select(User).where(User.id == id)).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found in database")
    return db_user

@router.get("/find/{username}", response_model=UserSchema, description="Finds a user by username")
async def find_user(username: str, db: Session = Depends(get_db_conn)) -> User:
    """Find a user by username.

    Args:
        username: The username to search for.
        db: Database session.

    Returns:
        The matching user record.

    Raises:
        HTTPException: 404 error if user not found.
    """
    db_user = db.exec(select(User).where(User.username == username)).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found in database")
    return db_user


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, description="deletes a user record")
async def delete_user(id: int, db: Session = Depends(get_db_conn)) -> None:
    """Delete a user account.

    Args:
        id: The user ID to delete.
        db: Database session.

    Raises:
        HTTPException: 404 error if user not found.
    """
    db_user = db.exec(select(User).where(User.id == id)).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found in database")

    db.delete(db_user)
    db.commit()
    return

@router.get("/list", response_model=list[UserSchema], description="Lists all users in the database")
async def list_all_users(db: Session = Depends(get_db_conn)) -> list[User]:
    """Retrieve all users from the database.

    Args:
        db: Database session.

    Returns:
        List of all user records.

    Raises:
        HTTPException: 404 error if no users found.
    """
    users = list(db.exec(select(User)).all())
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found in database")
    return users