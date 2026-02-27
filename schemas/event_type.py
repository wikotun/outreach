"""Pydantic schemas for EventType API requests and responses.

This module defines the data validation and serialization schemas
for event type-related API operations.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional


class EventTypeBase(BaseModel):
    """Base schema for event type data.

    Contains common fields shared between input and output schemas.

    Attributes:
        name: Name of the event type (e.g., workshop, conference).
        description: Optional description of the event type.
    """

    name: str
    description: Optional[str] = None


class EventTypeSchema(EventTypeBase):
    """Schema for event type API responses.

    Includes the database-generated id field for responses.

    Attributes:
        id: Unique identifier for the event type.
    """

    id: int
    model_config = ConfigDict(from_attributes=True)


class EventTypeSchemaInput(EventTypeBase):
    """Schema for event type creation and update requests.

    Inherits all fields from EventTypeBase without the id field.
    """

    pass
