from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime


class EventType(SQLModel, table=True):
    __tablename__ = "Event_Type"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    description: str = Field(nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self):
        return f"EventType(id={self.id}, name='{self.name}', description='{self.description}', created_at='{self.created_at}')"


class Event(SQLModel, table=True):
    __tablename__ = "Event"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False, max_length=50)
    event_date: date = Field(nullable=False)
    description: str = Field(nullable=True)
    location: str = Field(nullable=True, max_length=200)
    event_type_id: int = Field(foreign_key="Event_Type.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    participants: list["Participant"] = Relationship(
        back_populates="event",
        # link_model=Participant,
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    def __repr__(self):
        return f"Event(id={self.id}, name='{self.name}', description='{self.description}', location='{self.location}',event_type_id={self.event_type_id},created_at='{self.created_at}')"


class Participant(SQLModel, table=True):
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
    created_at: datetime = Field(default_factory=datetime.utcnow)
    event_id: int = Field(foreign_key="Event.id", nullable=False)
    event: "Event" = Relationship(back_populates="participants")

    def __repr__(self):
        return (f"Participant(id={self.id}, first_name='{self.first_name}', "
                f"last_name='{self.last_name}', email='{self.email}', "
                f"phone='{self.phone}', address='{self.address}', "
                f"city='{self.city}', state='{self.state}', "
                f"zip_code='{self.zip_code}', created_at='{self.created_at}',event_id={self.event_id})")


class User(SQLModel, table=True):
    __tablename__ = "User"

    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False, max_length=50)
    password: str = Field(nullable=False, max_length=100)
    first_name: str = Field(index=False, nullable=True, max_length=50)
    last_name: str = Field(index=False, nullable=True, max_length=50)
    email: str = Field(index=True, nullable=False, max_length=100)
    user_role: str =  Field(nullable=True,max_length=20)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}',first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}', created_at='{self.created_at}')"
