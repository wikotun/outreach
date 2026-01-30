import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_event(client: AsyncClient, create_event_type):
    et = create_event_type()
    response = await client.post("/event/create", json={
        "name": "Spring Gala",
        "event_date": "2025-06-20",
        "description": "Annual spring event",
        "location": "Grand Hall",
        "event_type_id": et.id,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Spring Gala"
    assert data["event_type_id"] == et.id
    assert "id" in data


@pytest.mark.asyncio
async def test_get_events_list(client: AsyncClient, create_event):
    create_event(name="Event One")
    create_event(name="Event Two")
    response = await client.get("/event/list")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_event(client: AsyncClient, create_event):
    ev = create_event(name="Findable Event")
    response = await client.get(f"/event/read/{ev.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == ev.id
    assert data["name"] == "Findable Event"


@pytest.mark.asyncio
async def test_get_event_not_found(client: AsyncClient):
    response = await client.get("/event/read/999999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_find_events_by_date(client: AsyncClient, create_event):
    create_event(name="June Event", event_date="2025-06-15")
    response = await client.get("/event/list/2025-06-01/2025-06-30")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_event(client: AsyncClient, create_event, create_event_type):
    et = create_event_type(name="Updated Type")
    ev = create_event(name="Old Event", event_type_id=et.id)
    response = await client.put(f"/event/update/{ev.id}", json={
        "name": "Updated Event",
        "event_date": "2025-07-01",
        "description": "Updated desc",
        "location": "New Venue",
        "event_type_id": et.id,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Event"
    assert data["location"] == "New Venue"


@pytest.mark.asyncio
async def test_delete_event(client: AsyncClient, create_event):
    ev = create_event(name="To Delete")
    response = await client.delete(f"/event/delete/{ev.id}")
    assert response.status_code == 204
