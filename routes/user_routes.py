from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
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
async def create_user(user: UserSchemaInput, db: Session = Depends(get_db_conn)):
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
async def get_user(id: int, db: Session = Depends(get_db_conn)):
    db_user = db.query(User).filter(User.id == id).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found in database")
    return db_user

@router.get("/find/{username}", response_model=UserSchema, description="Finds a user by username")
async def find_user(username: str, db: Session = Depends(get_db_conn)):
    db_user = db.query(User).filter(User.username == username).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found in database")
    return db_user


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, description="deletes a user record")
async def delete_user(id: int, db: Session = Depends(get_db_conn)):
    db_user = db.query(User).filter(User.id == id).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found in database")

    db.delete(db_user)
    db.commit()
    return

@router.get("/list", response_model=list[UserSchema], description="Lists all users in the database")
async def list_all_users(db: Session= Depends(get_db_conn)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found in database")
    return users