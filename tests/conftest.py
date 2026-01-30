import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool

from main import app
from config.db import get_db_conn
from models import EventType, Event, Participant, User
from auth.security import get_password_hash


@pytest.fixture(scope="session")
def test_db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture()
def db_session(test_db):
    with Session(test_db) as session:
        yield session
        session.rollback()


@pytest_asyncio.fixture()
async def client(db_session):
    def _override():
        yield db_session

    app.dependency_overrides[get_db_conn] = _override
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


# --------------- helper fixtures ---------------

@pytest.fixture()
def create_event_type(db_session):
    def _create(name="Workshop", description="A test workshop"):
        et = EventType(name=name, description=description)
        db_session.add(et)
        db_session.commit()
        db_session.refresh(et)
        return et
    return _create


@pytest.fixture()
def create_event(db_session, create_event_type):
    def _create(
        name="Community Outreach",
        event_date="2025-06-15",
        description="Test event",
        location="Main Hall",
        event_type_id=None,
    ):
        if event_type_id is None:
            et = create_event_type()
            event_type_id = et.id

        from datetime import date as _date
        if isinstance(event_date, str):
            event_date = _date.fromisoformat(event_date)

        ev = Event(
            name=name,
            event_date=event_date,
            description=description,
            location=location,
            event_type_id=event_type_id,
        )
        db_session.add(ev)
        db_session.commit()
        db_session.refresh(ev)
        return ev
    return _create


@pytest.fixture()
def create_user(db_session):
    def _create(
        username="testuser",
        password="secret123",
        first_name="Test",
        last_name="User",
        email="test@example.com",
        user_role="MEMBER",
    ):
        u = User(
            username=username,
            password=get_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            email=email,
            user_role=user_role,
        )
        db_session.add(u)
        db_session.commit()
        db_session.refresh(u)
        return u
    return _create


@pytest.fixture()
def create_participant(db_session, create_event):
    def _create(
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
        phone="555-1234",
        address="123 Main St",
        city="Springfield",
        state="IL",
        zip_code="62704",
        event_id=None,
    ):
        if event_id is None:
            ev = create_event()
            event_id = ev.id

        p = Participant(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            event_id=event_id,
        )
        db_session.add(p)
        db_session.commit()
        db_session.refresh(p)
        return p
    return _create
