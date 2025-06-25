from sqlmodel import Session, create_engine,SQLModel
from models import EventType, Event, Participant,User
from config.app_config import settings

DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

def get_db_conn():
    with Session(engine) as session:
        yield session