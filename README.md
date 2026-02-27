# Outreach

A full-stack application for managing community outreach events, participants, and user authentication. Built with FastAPI backend and React + TypeScript frontend.

## Features

- **Event Management** — Create, update, delete, and filter events by date range
- **Event Types** — Categorize events with custom types
- **Participant Tracking** — Register and manage event participants
- **User Management** — User accounts with role-based access (Member, Admin)
- **Authentication** — JWT-based authentication with bcrypt password hashing
- **React Frontend** — Modern SPA with Tailwind CSS styling
- **Database Migrations** — Schema versioning with Alembic

## Tech Stack

### Backend
- **Framework:** FastAPI + Uvicorn
- **ORM:** SQLModel (SQLAlchemy + Pydantic)
- **Database:** SQLite (default), with MySQL and PostgreSQL support
- **Auth:** JWT via python-jose, bcrypt via passlib
- **Testing:** pytest with httpx async client
- **Migrations:** Alembic

### Frontend
- **Framework:** React 18 + TypeScript
- **Build Tool:** Vite
- **Routing:** React Router v6
- **Forms:** react-hook-form + zod validation
- **HTTP Client:** Axios with JWT interceptors
- **Styling:** Tailwind CSS
- **Icons:** Lucide React

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
├── main.py             # Application entry point
├── frontend/           # React SPA
│   ├── src/
│   │   ├── api/        # Axios client with JWT interceptors
│   │   ├── components/ # Reusable UI components
│   │   ├── contexts/   # React Context (Auth)
│   │   ├── pages/      # Route-level components
│   │   ├── routes/     # Routing configuration
│   │   ├── types/      # TypeScript definitions
│   │   └── App.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
└── static/             # Built frontend (production)
```

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+

### Installation

```bash
# Clone the repository
git clone https://github.com/wikotun/outreach.git
cd outreach

# Install backend dependencies
make install

# Install frontend dependencies
make frontend-install
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

**Development mode** (two terminals):

```bash
# Terminal 1: Start backend
make dev

# Terminal 2: Start frontend
make frontend-dev
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Production mode:**

```bash
# Build frontend
make frontend-build

# Run backend (serves static files)
make run
```

### Available Make Commands

| Command | Description |
|---------|-------------|
| `make install` | Create venv and install Python dependencies |
| `make dev` | Run backend with hot reload |
| `make run` | Run backend in production mode |
| `make test` | Run tests |
| `make frontend-install` | Install frontend dependencies |
| `make frontend-dev` | Run frontend dev server |
| `make frontend-build` | Build frontend for production |
| `make migrate` | Apply database migrations |
| `make migrate-new msg='...'` | Create a new migration |

## API Reference

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
make test
```

Tests use an in-memory SQLite database and cover all major endpoints including error cases.

## Database Migrations

```bash
# Generate a new migration after model changes
make migrate-new msg="description of changes"

# Apply migrations
make migrate
```

## License

This project is unlicensed. See the repository for details.
