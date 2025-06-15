from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db_conn
from models import EventType
from schemas.event_type import EventTypeSchema, EventTypeSchemaInput
from config.app_config import settings

router = APIRouter(
    prefix="/type",
    tags=["Event Types"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create", response_model = EventTypeSchema)
async def create_event_type(event_type: EventTypeSchemaInput, db: Session = Depends(get_db_conn)):
    new_event_type = EventType(**event_type.model_dump())
    db.add(new_event_type)
    db.commit()
    db.refresh(new_event_type)
    return new_event_type


@router.get("/read/{id}", response_model=EventTypeSchema)
async def get_event_type(id: int, db: Session = Depends(get_db_conn)):
    event_type = db.query(EventType).filter(EventType.id == id).first()

    if not event_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event type not found")
    return event_type


@router.put("/update/{id}", response_model=EventTypeSchema)
async def update_event_type(id: int, event_type: EventTypeSchemaInput, db: Session = Depends(get_db_conn)):
    db_event_type = db.query(EventType).filter(EventType.id == id).first()

    if not db_event_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event type not found")

    db_event_type.name = event_type.name
    db_event_type.description = event_type.description
    db.commit()
    db.refresh(db_event_type)

    return db_event_type


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event_type(id: int, db: Session = Depends(get_db_conn)):
    db_event_type = db.query(EventType).filter(EventType.id == id).first()

    if not db_event_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event type not found")

    db.delete(db_event_type)
    db.commit()
    return


@router.get("/list", response_model=list[EventTypeSchema])
async def get_event_types(db: Session = Depends(get_db_conn)):
    return db.query(EventType).all()
