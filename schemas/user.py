"""Pydantic schemas for User API requests and responses.

This module defines the data validation and serialization schemas
for user-related API operations.
"""

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    """Base schema for user data.

    Contains common fields shared between input and output schemas.

    Attributes:
        username: Unique username for login.
        password: User's password (plaintext in input, hashed in storage).
        first_name: User's first name.
        last_name: User's last name.
        email: User's email address.
    """

    username: str
    password: str
    first_name: str
    last_name: str
    email: str


class UserSchema(UserBase):
    """Schema for user API responses.

    Includes the database-generated id field for responses.

    Attributes:
        id: Unique identifier for the user.
    """

    id: int
    model_config = ConfigDict(from_attributes=True)


class UserSchemaInput(UserBase):
    """Schema for user creation and update requests.

    Inherits all fields from UserBase without the id field.
    """

    pass
