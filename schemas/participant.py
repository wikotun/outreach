"""Pydantic schemas for Participant API requests and responses.

This module defines the data validation and serialization schemas
for participant-related API operations.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional


class ParticipantBase(BaseModel):
    """Base schema for participant data.

    Contains common fields shared between input and output schemas.

    Attributes:
        first_name: Participant's first name.
        last_name: Participant's last name.
        email: Participant's email address.
        phone: Participant's phone number.
        address: Street address.
        city: City name.
        state: Two-letter state code.
        zip_code: Postal code.
        event_id: Optional foreign key to the associated event.
    """

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
    """Schema for participant API responses.

    Includes the database-generated id field for responses.

    Attributes:
        id: Unique identifier for the participant.
    """

    id: int
    model_config = ConfigDict(from_attributes=True)


class ParticipantSchemaInput(ParticipantBase):
    """Schema for participant creation and update requests.

    Inherits all fields from ParticipantBase without the id field.
    """

    pass
