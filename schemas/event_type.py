from pydantic import BaseModel
from typing import Optional

class EventTypeBase(BaseModel):
    name: str
    description: Optional[str] = None

class EventTypeSchema(EventTypeBase):
    id: int

    class Config:
        from_attributes = True

class EventTypeSchemaInput(EventTypeBase):
    pass
