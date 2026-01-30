import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from fastapi import status, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from unittest.mock import patch, MagicMock
from main import app


# Test client fixture
@pytest_asyncio.fixture
async def ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# Test startup event
@pytest.mark.asyncio
async def test_startup_event():
    with patch('main.init_db') as mock_init_db:
        # Call the startup event
        await app.router.startup()

        # Verify init_db was called
        mock_init_db.assert_called_once()


# Test HTTP exception handler
@pytest.mark.asyncio
async def test_http_exception_handler():
    # Create a test request
    request = MagicMock()
    exc = StarletteHTTPException(status_code=404, detail="Not found")

    # Call the exception handler
    response = await app.exception_handlers[StarletteHTTPException](request, exc)

    # Verify the response
    assert response.status_code == 404
    assert response.body == b"Not found"


# Test validation exception handler
@pytest.mark.asyncio
async def test_validation_exception_handler():
    # Create a test request
    request = MagicMock()
    exc = RequestValidationError(
        errors=[{"loc": ("query", "test"), "msg": "field required", "type": "value_error.missing"}])

    # Call the exception handler
    response = await app.exception_handlers[RequestValidationError](request, exc)

    # Verify the response
    assert response.status_code == 400


# Test health check endpoint
@pytest.mark.asyncio
async def test_health_check(ac: AsyncClient):
    # Add a health check endpoint for testing
    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    # Make the request
    response = await ac.get("/health")

    # Verify the response
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}


# Test router inclusion
@pytest.mark.asyncio
async def test_routers_included():
    # Check if all expected routers are included
    expected_routes = {
        "/type",
        "/event",
        "/participant",
        "/user"
    }

    # Get all registered routes
    registered_routes = {route.path.split("/")[1] for route in app.routes if
                         hasattr(route, 'path') and len(route.path.split("/")) > 1}

    # Verify all expected routes are registered
    for route in expected_routes:
        assert route.lstrip("/") in registered_routes
