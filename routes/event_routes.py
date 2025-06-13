from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db_conn
from models import Event, Participant
from schemas.event import EventSchemaInput, EventSchema
from schemas.participant import ParticipantSchemaInput

router = APIRouter(
    prefix="/event",
    tags=["Events"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=EventSchema, description="Creates an event record in the database")
async def create_event(event: EventSchemaInput, db: Session = Depends(get_db_conn)):
    new_evnt = Event(**event.model_dump())
    db.add(new_evnt)
    db.commit()
    db.refresh(new_evnt)

    return new_evnt


@router.get("/list", response_model=EventSchema, description="Returns the events in the database")
async def get_events(db: Session = Depends(get_db_conn)):
    return db.query(Event).all()


@router.get("/read/{id}", response_model=EventSchema)
async def get_event(id: int, db: Session = Depends(get_db_conn)):
    event = db.query(Event).filter(Event.id == id).first()

    if not event:
        raise HTTPException(status_code=c, detail="Event type not found")
    return event


@router.get("/list/{start_date}/{end_date}", response_model=EventSchema,
            description="Returns events in the database for a given date range")
async def find_events_by_date(start_date: date, end_date: date, db: Session = Depends(get_db_conn)):
    return (db.query(Event).filter
        (
            (Event.event_date >= start_date) & (Event.event_date <= end_date)
        )
    )


@router.put("/update/{id}", response_model=EventSchema, description="Updates an event record")
async def update_event(id: int, evnt: EventSchemaInput, db: Session = Depends(get_db_conn)):
    db_evnt = db.query(Event).filter(Event.id == id).first()

    if not db_evnt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event record not found")

    db_evnt.name = evnt.name
    db_evnt.description = evnt.description
    db_evnt.event_date = evnt.event_date
    db_evnt.location = evnt.location
    db_evnt.event_type_id = evnt.event_type_id

    db.commit()
    db.refresh(db_evnt)

    return db_evnt

@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, description="Deletes a given event record")
async def delete_event(id: int, db: Session = Depends(get_db_conn)):
    event = db.query(Event).filter(Event.id == id).first()

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event record not found")

    db.delete(event)
    db.commit()
    return

@router.post("/participant/add/{event_id}",response_model=EventSchema,description="Adds a participant record to an event")
async def add_participant_to_event(event_id:int, participant: ParticipantSchemaInput, db: Session = Depends(get_db_conn)):
    event = db.query(Event).filter(Event.id == id).first()

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event record not found")

    db_participant =  Participant(**participant.model_dump())
    db.add(db_participant)

    event.participants.add(participant)
    db.add(event)
    db.commit()
    db.refresh(event)

    return event




