from datetime import date
from pydantic import BaseModel
from typing import Optional


class EventBase(BaseModel):
    name: str
    event_date: date
    description: Optional[str] = None
    location: str
    event_type_id: Optional[int] = None


class EventSchema(EventBase):
    id: int
    class Config:
        from_attributes = True

class EventSchemaInput(EventBase):
    pass
