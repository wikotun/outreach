from pydantic import BaseModel
from typing import Optional


class ParticipantBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip_code: str
    event_id: Optional[int] = None



class ParticipantSchema(ParticipantBase):
    id: int
    class Config:
        from_attributes = True


class ParticipantSchemaInput(ParticipantBase):
    pass