"""Event Type API routes.

This module provides CRUD endpoints for managing event types
(categories of events like workshops, conferences, etc.).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from config.db import get_db_conn
from models import EventType
from schemas.event_type import EventTypeSchema, EventTypeSchemaInput
from config.app_config import settings
import logging

router = APIRouter(
    prefix="/type",
    tags=["Event Types"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create", response_model=EventTypeSchema)
async def create_event_type(event_type: EventTypeSchemaInput, db: Session = Depends(get_db_conn)) -> EventType:
    """Create a new event type.

    Args:
        event_type: Event type data for the new record.
        db: Database session.

    Returns:
        The created event type with its generated id.
    """
    new_event_type = EventType(**event_type.model_dump())
    db.add(new_event_type)
    db.commit()
    db.refresh(new_event_type)
    return new_event_type


@router.get("/read/{id}", response_model=EventTypeSchema)
async def get_event_type(id: int, db: Session = Depends(get_db_conn)) -> EventType:
    """Retrieve a single event type by ID.

    Args:
        id: The event type ID to retrieve.
        db: Database session.

    Returns:
        The requested event type record.

    Raises:
        HTTPException: 404 error if event type not found.
    """
    event_type = db.exec(select(EventType).where(EventType.id == id)).first()

    if not event_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event type not found")
    return event_type


@router.put("/update/{id}", response_model=EventTypeSchema)
async def update_event_type(id: int, event_type: EventTypeSchemaInput, db: Session = Depends(get_db_conn)) -> EventType:
    """Update an existing event type.

    Args:
        id: The event type ID to update.
        event_type: Updated event type data.
        db: Database session.

    Returns:
        The updated event type record.

    Raises:
        HTTPException: 404 error if event type not found.
    """
    db_event_type = db.exec(select(EventType).where(EventType.id == id)).first()

    if not db_event_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event type not found")

    db_event_type.name = event_type.name
    db_event_type.description = event_type.description
    db.commit()
    db.refresh(db_event_type)

    return db_event_type


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event_type(id: int, db: Session = Depends(get_db_conn)) -> None:
    """Delete an event type.

    Args:
        id: The event type ID to delete.
        db: Database session.

    Raises:
        HTTPException: 404 error if event type not found.
    """
    db_event_type = db.exec(select(EventType).where(EventType.id == id)).first()

    if not db_event_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event type not found")

    db.delete(db_event_type)
    db.commit()
    return


@router.get("/list", response_model=list[EventTypeSchema])
async def get_event_types(db: Session = Depends(get_db_conn)) -> list[EventType]:
    """Retrieve all event types.

    Args:
        db: Database session.

    Returns:
        List of all event type records.
    """
    print(f"Fetching all event types from {settings.db_username}")
    return list(db.exec(select(EventType)).all())
