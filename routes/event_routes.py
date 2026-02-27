"""Event API routes.

This module provides CRUD endpoints for managing events
and adding participants to events.
"""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from config.db import get_db_conn
from models import Event, Participant
from schemas.event import EventSchemaInput, EventSchema
from schemas.participant import ParticipantSchemaInput

router = APIRouter(
    prefix="/event",
    tags=["Events"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=EventSchema, description="Creates an event record in the database", responses={
    404: {
        "description": "Item not found",
    },
    500: {
        "description": "Server error"
    }})
async def create_event(event: EventSchemaInput, db: Session = Depends(get_db_conn)) -> Event:
    """Create a new event record.

    Args:
        event: Event data for the new record.
        db: Database session.

    Returns:
        The created event with its generated id.
    """
    new_evnt = Event(**event.model_dump())
    db.add(new_evnt)
    db.commit()
    db.refresh(new_evnt)

    return new_evnt


@router.get("/list", response_model=list[EventSchema], description="Returns the events in the database", responses={
    404: {
        "description": "Item not found",
    },
    500: {
        "description": "Server error"
    }})
async def get_events(db: Session = Depends(get_db_conn)) -> list[Event]:
    """Retrieve all events from the database.

    Args:
        db: Database session.

    Returns:
        List of all event records.
    """
    return list(db.exec(select(Event)).all())


@router.get("/read/{id}", response_model=EventSchema)
async def get_event(id: int, db: Session = Depends(get_db_conn), responses={
    404: {
        "description": "Item not found",
    },
    500: {
        "description": "Server error"
    }}) -> Event:
    """Retrieve a single event by ID.

    Args:
        id: The event ID to retrieve.
        db: Database session.

    Returns:
        The requested event record.

    Raises:
        HTTPException: 404 error if event not found.
    """
    event = db.exec(select(Event).where(Event.id == id)).first()

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


@router.get("/list/{start_date}/{end_date}", response_model=list[EventSchema],
            description="Returns events in the database for a given date range", responses={
        404: {
            "description": "Item not found",
        },
        500: {
            "description": "Server error"
        }})
async def find_events_by_date(start_date: date, end_date: date, db: Session = Depends(get_db_conn)) -> list[Event]:
    """Retrieve events within a date range.

    Args:
        start_date: Start of the date range (inclusive).
        end_date: End of the date range (inclusive).
        db: Database session.

    Returns:
        List of events occurring within the specified date range.
    """
    return list(db.exec(
        select(Event).where(
            (Event.event_date >= start_date) & (Event.event_date <= end_date)
        )
    ).all())


@router.put("/update/{id}", response_model=EventSchema, description="Updates an event record", responses={
    404: {
        "description": "Item not found",
    },
    500: {
        "description": "Server error"
    }})
async def update_event(id: int, evnt: EventSchemaInput, db: Session = Depends(get_db_conn)) -> Event:
    """Update an existing event record.

    Args:
        id: The event ID to update.
        evnt: Updated event data.
        db: Database session.

    Returns:
        The updated event record.

    Raises:
        HTTPException: 404 error if event not found.
    """
    db_evnt = db.exec(select(Event).where(Event.id == id)).first()

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


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, description="Deletes a given event record",
               responses={
                   404: {
                       "description": "Item not found",
                   },
                   500: {
                       "description": "Server error"
                   }})
async def delete_event(id: int, db: Session = Depends(get_db_conn)) -> None:
    """Delete an event record.

    Deletes the event and all associated participants due to cascade.

    Args:
        id: The event ID to delete.
        db: Database session.

    Raises:
        HTTPException: 404 error if event not found.
    """
    event = db.exec(select(Event).where(Event.id == id)).first()

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event record not found")

    db.delete(event)
    db.commit()
    return


@router.post("/participant/add/{event_id}", response_model=EventSchema,
             description="Adds a participant record to an event", responses={
        404: {
            "description": "Item not found",
        },
        500: {
            "description": "Server error"
        }})
async def add_participant_to_event(event_id: int, participant: ParticipantSchemaInput,
                                   db: Session = Depends(get_db_conn)) -> Event:
    """Add a participant to an existing event.

    Creates a new participant record and associates it with the event.

    Args:
        event_id: The event ID to add the participant to.
        participant: Participant data to create.
        db: Database session.

    Returns:
        The updated event record with the new participant.

    Raises:
        HTTPException: 404 error if event not found.
    """
    event = db.exec(select(Event).where(Event.id == event_id)).first()

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event record not found")

    db_participant = Participant(**participant.model_dump())
    db.add(db_participant)

    event.participants.append(db_participant)
    db.add(event)
    db.commit()
    db.refresh(event)

    return event
