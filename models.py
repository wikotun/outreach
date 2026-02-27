"""Database models for the outreach application.

This module defines the SQLModel ORM classes that map to database tables
for events, event types, participants, and users.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime, timezone


def utc_now() -> datetime:
    """Return the current UTC timestamp.

    Returns:
        Current datetime with UTC timezone.
    """
    return datetime.now(timezone.utc)


class EventType(SQLModel, table=True):
    """Event type classification model.

    Represents a category or type of event (e.g., workshop, conference, meetup).

    Attributes:
        id: Primary key identifier.
        name: Name of the event type.
        description: Optional description of the event type.
        created_at: Timestamp when the record was created.
    """
    __tablename__ = "Event_Type"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    description: str = Field(nullable=True)
    created_at: datetime = Field(default_factory=utc_now)

    def __repr__(self):
        return f"EventType(id={self.id}, name='{self.name}', description='{self.description}', created_at='{self.created_at}')"


class Event(SQLModel, table=True):
    """Event model representing scheduled events.

    Stores information about events including name, date, location,
    and associated participants.

    Attributes:
        id: Primary key identifier.
        name: Name of the event.
        event_date: Date when the event occurs.
        description: Optional description of the event.
        location: Optional location where the event takes place.
        event_type_id: Foreign key to the event type.
        created_at: Timestamp when the record was created.
        participants: List of participants registered for this event.
    """

    __tablename__ = "Event"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False, max_length=50)
    event_date: date = Field(nullable=False)
    description: str = Field(nullable=True)
    location: str = Field(nullable=True, max_length=200)
    event_type_id: int = Field(foreign_key="Event_Type.id", nullable=False)
    created_at: datetime = Field(default_factory=utc_now)
    participants: list["Participant"] = Relationship(
        back_populates="event",
        # link_model=Participant,
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    def __repr__(self):
        return f"Event(id={self.id}, name='{self.name}', description='{self.description}', location='{self.location}', event_type_id={self.event_type_id}, created_at='{self.created_at}')"


class Participant(SQLModel, table=True):
    """Participant model for event attendees.

    Stores contact and address information for individuals
    registered to attend events.

    Attributes:
        id: Primary key identifier.
        first_name: Participant's first name.
        last_name: Participant's last name.
        email: Participant's email address.
        phone: Optional phone number.
        address: Optional street address.
        city: Optional city name.
        state: Optional two-letter state code.
        zip_code: Optional postal code.
        created_at: Timestamp when the record was created.
        event_id: Foreign key to the associated event.
        event: Relationship to the Event model.
    """

    __tablename__ = "Participant"

    id: int = Field(default=None, primary_key=True)
    first_name: str = Field(index=False, nullable=False, max_length=50)
    last_name: str = Field(index=False, nullable=False, max_length=50)
    email: str = Field(index=True, nullable=False, max_length=50)
    phone: str = Field(index=False, nullable=True, max_length=15)
    address: str = Field(index=False, nullable=True, max_length=100)
    city: str = Field(index=False, nullable=True, max_length=30)
    state: str = Field(index=False, nullable=True, max_length=2)
    zip_code: str = Field(index=False, nullable=True, max_length=10)
    created_at: datetime = Field(default_factory=utc_now)
    event_id: int = Field(foreign_key="Event.id", nullable=False)
    event: "Event" = Relationship(back_populates="participants")

    def __repr__(self):
        return (f"Participant(id={self.id}, first_name='{self.first_name}', "
                f"last_name='{self.last_name}', email='{self.email}', "
                f"phone='{self.phone}', address='{self.address}', "
                f"city='{self.city}', state='{self.state}', "
                f"zip_code='{self.zip_code}', created_at='{self.created_at}', event_id={self.event_id})")


class User(SQLModel, table=True):
    """User model for application authentication.

    Stores user credentials and profile information for
    users who can access the system.

    Attributes:
        id: Primary key identifier.
        username: Unique username for login.
        password: Hashed password.
        first_name: Optional user's first name.
        last_name: Optional user's last name.
        email: User's email address.
        user_role: Role assigned to the user (e.g., MEMBER, ADMIN).
        created_at: Timestamp when the record was created.
    """

    __tablename__ = "User"

    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False, max_length=50)
    password: str = Field(nullable=False, max_length=100)
    first_name: str = Field(index=False, nullable=True, max_length=50)
    last_name: str = Field(index=False, nullable=True, max_length=50)
    email: str = Field(index=True, nullable=False, max_length=100)
    user_role: str = Field(nullable=True, max_length=20)
    created_at: datetime = Field(default_factory=utc_now)

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}', created_at='{self.created_at}')"
