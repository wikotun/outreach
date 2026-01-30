from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.db import get_db_conn
from models import Participant
from schemas.participant import ParticipantSchema, ParticipantSchemaInput


router = APIRouter(
    prefix="/participant",
    tags=["Participants"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create", response_model= ParticipantSchema, description="add a participant to an event")
async def create_participant(input: ParticipantSchemaInput, db: Session = Depends(get_db_conn)):
    participant = Participant(**input.model_dump())
    db.add(participant)
    db.commit()
    db.refresh(participant)

    return participant

@router.get("/list/{event_id}",response_model=list[ParticipantSchema], description="Lists the participants for a given event")
async def list_participants(event_id: int,db: Session=Depends(get_db_conn)):
    return db.query(Participant).filter(Participant.event_id == event_id)


@router.get("/read/{id}",response_model=ParticipantSchema,description="Returns the details for a given participant id")
async def get_participant(id: int, db: Session=Depends(get_db_conn)):
    participant = db.query(Participant).filter(Participant.id == id).first()

    return participant

@router.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_participant(id: int, db: Session=Depends(get_db_conn)):
    participant = db.query(Participant).filter(Participant.id == id).first()

    if not participant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Participant record not found")

    db.delete(participant)
    db.commit()
    return


@router.get("/list",response_model=list[ParticipantSchema],description="Returns all the participants in the database")
async def list_all_participants(db: Session=Depends(get_db_conn)):
    return db.query(Participant).all()


