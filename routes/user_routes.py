from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from config.db import get_db_conn
from models import User
from schemas.user import UserSchema, UserSchemaInput
from security.auth_filter import pwd_context
from domain.constants import Role

router = APIRouter(
    prefix="/user",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create", response_model=UserSchema, description="Creates a new user record in the database")
async def create_user(user: UserSchemaInput, db: Session = Depends(get_db_conn)):
    new_user = User(**user.model_dump())
    new_user.user_role = Role.MEMBER.value
    pwd_hash = pwd_context.hash(user.password)
    new_user.password = pwd_hash
    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
    return new_user


@router.get("/read/{id}")
async def get_user(id: int, db: Session = Depends(get_db_conn)):
    db_user = db.query(User).filter(User.id == id).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found in database")
    return db_user

@router.get("/find/{username}")
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
