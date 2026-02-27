"""Pydantic schemas for authentication token responses.

This module defines the schema for JWT token responses
from authentication endpoints.
"""

from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """Schema for authentication token responses.

    Returned by the login endpoint upon successful authentication.

    Attributes:
        access_token: The JWT access token string.
        token_type: The type of token (typically 'bearer').
    """

    access_token: str
    token_type: str
