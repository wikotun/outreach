"""Participant API routes.

This module provides CRUD endpoints for managing event participants.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from config.db import get_db_conn
from models import Participant
from schemas.participant import ParticipantSchema, ParticipantSchemaInput


router = APIRouter(
    prefix="/participant",
    tags=["Participants"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create", response_model=ParticipantSchema, description="add a participant to an event")
async def create_participant(input: ParticipantSchemaInput, db: Session = Depends(get_db_conn)) -> Participant:
    """Create a new participant record.

    Args:
        input: Participant data for the new record.
        db: Database session.

    Returns:
        The created participant with its generated id.
    """
    participant = Participant(**input.model_dump())
    db.add(participant)
    db.commit()
    db.refresh(participant)

    return participant

@router.get("/list/{event_id}", response_model=list[ParticipantSchema], description="Lists the participants for a given event")
async def list_participants(event_id: int, db: Session = Depends(get_db_conn)) -> list[Participant]:
    """List all participants for a specific event.

    Args:
        event_id: The event ID to filter participants by.
        db: Database session.

    Returns:
        List of participants registered for the event.
    """
    return list(db.exec(select(Participant).where(Participant.event_id == event_id)).all())


@router.get("/read/{id}", response_model=ParticipantSchema, description="Returns the details for a given participant id")
async def get_participant(id: int, db: Session = Depends(get_db_conn)) -> Participant | None:
    """Retrieve a single participant by ID.

    Args:
        id: The participant ID to retrieve.
        db: Database session.

    Returns:
        The requested participant record, or None if not found.
    """
    participant = db.exec(select(Participant).where(Participant.id == id)).first()

    return participant

@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_participant(id: int, db: Session = Depends(get_db_conn)) -> None:
    """Delete a participant record.

    Args:
        id: The participant ID to delete.
        db: Database session.

    Raises:
        HTTPException: 404 error if participant not found.
    """
    participant = db.exec(select(Participant).where(Participant.id == id)).first()

    if not participant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Participant record not found")

    db.delete(participant)
    db.commit()
    return


@router.get("/list", response_model=list[ParticipantSchema], description="Returns all the participants in the database")
async def list_all_participants(db: Session = Depends(get_db_conn)) -> list[Participant]:
    """Retrieve all participants from the database.

    Args:
        db: Database session.

    Returns:
        List of all participant records.
    """
    return list(db.exec(select(Participant)).all())


