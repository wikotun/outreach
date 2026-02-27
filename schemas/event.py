"""Pydantic schemas for Event API requests and responses.

This module defines the data validation and serialization schemas
for event-related API operations.
"""

from datetime import date
from pydantic import BaseModel, ConfigDict
from typing import Optional


class EventBase(BaseModel):
    """Base schema for event data.

    Contains common fields shared between input and output schemas.

    Attributes:
        name: Name of the event.
        event_date: Date when the event occurs.
        description: Optional description of the event.
        location: Location where the event takes place.
        event_type_id: Optional foreign key to the event type.
    """

    name: str
    event_date: date
    description: Optional[str] = None
    location: str
    event_type_id: Optional[int] = None


class EventSchema(EventBase):
    """Schema for event API responses.

    Includes the database-generated id field for responses.

    Attributes:
        id: Unique identifier for the event.
    """

    id: int
    model_config = ConfigDict(from_attributes=True)


class EventSchemaInput(EventBase):
    """Schema for event creation and update requests.

    Inherits all fields from EventBase without the id field.
    """

    pass
