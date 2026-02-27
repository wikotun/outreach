.PHONY: help install run dev test lint clean migrate migrate-new freeze frontend-install frontend-dev frontend-build

PYTHON := python
VENV := venv
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
UVICORN := $(VENV)/bin/uvicorn

help:
	@echo "Available commands:"
	@echo "  make install          - Create venv and install dependencies"
	@echo "  make run              - Run the server (production mode)"
	@echo "  make dev              - Run the server with hot reload"
	@echo "  make test             - Run tests"
	@echo "  make lint             - Run code linting with autopep8"
	@echo "  make clean            - Remove cache files and __pycache__"
	@echo "  make migrate          - Apply database migrations"
	@echo "  make migrate-new      - Create a new migration (usage: make migrate-new msg='description')"
	@echo "  make freeze           - Update requirements.txt"
	@echo "  make frontend-install - Install frontend dependencies"
	@echo "  make frontend-dev     - Run frontend dev server"
	@echo "  make frontend-build   - Build frontend for production"

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(UVICORN) main:app --host 0.0.0.0 --port 8000

dev:
	$(UVICORN) main:app --reload

test:
	$(PYTEST) tests/ -v

lint:
	$(VENV)/bin/autopep8 --in-place --recursive .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

migrate:
	$(VENV)/bin/alembic upgrade head

migrate-new:
	$(VENV)/bin/alembic revision --autogenerate -m "$(msg)"

freeze:
	$(PIP) freeze > requirements.txt

frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

frontend-build:
	cd frontend && npm run build
