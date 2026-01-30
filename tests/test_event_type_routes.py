import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_event_type(client: AsyncClient):
    response = await client.post("/type/create", json={
        "name": "Conference",
        "description": "A large conference",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Conference"
    assert data["description"] == "A large conference"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_event_type(client: AsyncClient, create_event_type):
    et = create_event_type(name="Seminar", description="A seminar event")
    response = await client.get(f"/type/read/{et.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == et.id
    assert data["name"] == "Seminar"


@pytest.mark.asyncio
async def test_get_event_types_list(client: AsyncClient, create_event_type):
    create_event_type(name="Type A")
    create_event_type(name="Type B")
    response = await client.get("/type/list")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


@pytest.mark.asyncio
async def test_update_event_type(client: AsyncClient, create_event_type):
    et = create_event_type(name="Old Name", description="Old desc")
    response = await client.put(f"/type/update/{et.id}", json={
        "name": "New Name",
        "description": "New desc",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"
    assert data["description"] == "New desc"


@pytest.mark.asyncio
async def test_delete_event_type(client: AsyncClient, create_event_type):
    et = create_event_type(name="To Delete")
    response = await client.delete(f"/type/delete/{et.id}")
    assert response.status_code == 204
