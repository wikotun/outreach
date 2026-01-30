# Outreach

A FastAPI-based REST API for managing community outreach events, participants, and user authentication.

## Features

- **Event Management** — Create, update, delete, and filter events by date range
- **Event Types** — Categorize events with custom types
- **Participant Tracking** — Register and manage event participants
- **User Management** — User accounts with role-based access (Member, Admin)
- **Authentication** — JWT-based authentication with bcrypt password hashing
- **Database Migrations** — Schema versioning with Alembic

## Tech Stack

- **Framework:** FastAPI + Uvicorn
- **ORM:** SQLModel (SQLAlchemy + Pydantic)
- **Database:** SQLite (default), with MySQL and PostgreSQL support
- **Auth:** JWT via python-jose, bcrypt via passlib
- **Testing:** pytest with httpx async client
- **Migrations:** Alembic

## Project Structure

```
outreach/
├── auth/               # Authentication & JWT security
├── config/             # App settings and database configuration
├── routes/             # API route handlers
├── schemas/            # Pydantic request/response models
├── tests/              # Test suite with fixtures
├── alembic/            # Database migration scripts
├── models.py           # SQLModel ORM models
└── main.py             # Application entry point
```

## Getting Started

### Prerequisites

- Python 3.12+

### Installation

```bash
# Clone the repository
git clone https://github.com/wikotun/outreach.git
cd outreach

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
secret_key="your-secret-key"
algorithm="HS256"
access_token_expire_minutes=30
database_url="sqlite:///./database.db"
db_username="root"
db_password="password"
host="localhost"
port=8000
log_level="debug"
```

### Running the Application

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --host localhost --port 8000 --reload
```

The API will be available at `http://localhost:8000`. Interactive docs are served at `/docs` (Swagger UI) and `/redoc` (ReDoc).

## API Endpoints

### Event Types (`/type`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/type/create` | Create an event type |
| GET | `/type/read/{id}` | Get an event type |
| GET | `/type/list` | List all event types |
| PUT | `/type/update/{id}` | Update an event type |
| DELETE | `/type/delete/{id}` | Delete an event type |

### Events (`/event`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/event/create` | Create an event |
| GET | `/event/list` | List all events |
| GET | `/event/read/{id}` | Get an event |
| GET | `/event/list/{start_date}/{end_date}` | Filter events by date range |
| PUT | `/event/update/{id}` | Update an event |
| DELETE | `/event/delete/{id}` | Delete an event |
| POST | `/event/participant/add/{event_id}` | Add a participant to an event |

### Participants (`/participant`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/participant/create` | Create a participant |
| GET | `/participant/list` | List all participants |
| GET | `/participant/list/{event_id}` | List participants for an event |
| GET | `/participant/read/{id}` | Get a participant |
| DELETE | `/participant/delete/{id}` | Delete a participant |

### Users (`/user`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/user/create` | Create a user |
| GET | `/user/read/{id}` | Get a user by ID |
| GET | `/user/find/{username}` | Find a user by username |
| GET | `/user/list` | List all users |
| DELETE | `/user/delete/{id}` | Delete a user |

### Authentication (`/security`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/security/token` | Login and receive a JWT access token |
| GET | `/security/users/me` | Get the currently authenticated user |

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_event_routes.py
```

Tests use an in-memory SQLite database and cover all major endpoints including error cases.

## Database Migrations

```bash
# Generate a new migration after model changes
alembic revision --autogenerate -m "description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## License

This project is unlicensed. See the repository for details.
