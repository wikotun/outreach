import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_participant(client: AsyncClient, create_event):
    ev = create_event()
    response = await client.post("/participant/create", json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "phone": "555-9999",
        "address": "456 Oak Ave",
        "city": "Chicago",
        "state": "IL",
        "zip_code": "60601",
        "event_id": ev.id,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Alice"
    assert data["event_id"] == ev.id
    assert "id" in data


@pytest.mark.asyncio
async def test_list_participants_by_event(client: AsyncClient, create_participant, create_event):
    ev = create_event(name="Participant Event")
    create_participant(first_name="Bob", email="bob@example.com", event_id=ev.id)
    response = await client.get(f"/participant/list/{ev.id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_get_participant(client: AsyncClient, create_participant):
    p = create_participant(first_name="Carol", email="carol@example.com")
    response = await client.get(f"/participant/read/{p.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == p.id
    assert data["first_name"] == "Carol"


@pytest.mark.asyncio
async def test_list_all_participants(client: AsyncClient, create_participant):
    create_participant(first_name="Dan", email="dan@example.com")
    response = await client.get("/participant/list")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_participant(client: AsyncClient, create_participant):
    p = create_participant(first_name="Eve", email="eve@example.com")
    response = await client.delete(f"/participant/delete/{p.id}")
    assert response.status_code == 204
