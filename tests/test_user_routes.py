import pytest
from httpx import AsyncClient
from auth.security import verify_password


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, db_session):
    response = await client.post("/user/create", json={
        "username": "newuser",
        "password": "mypassword",
        "first_name": "New",
        "last_name": "User",
        "email": "newuser@example.com",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert "id" in data
    # Password in response should be the hash, not plaintext
    assert data["password"] != "mypassword"

    # Verify the password was actually hashed correctly
    from models import User
    db_user = db_session.query(User).filter(User.id == data["id"]).first()
    assert verify_password("mypassword", db_user.password)


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, create_user):
    u = create_user(username="getme", email="getme@example.com")
    response = await client.get(f"/user/read/{u.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == u.id
    assert data["username"] == "getme"


@pytest.mark.asyncio
async def test_find_user_by_username(client: AsyncClient, create_user):
    create_user(username="findable", email="findable@example.com")
    response = await client.get("/user/find/findable")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "findable"


@pytest.mark.asyncio
async def test_list_users(client: AsyncClient, create_user):
    create_user(username="lister1", email="l1@example.com")
    create_user(username="lister2", email="l2@example.com")
    response = await client.get("/user/list")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, create_user):
    u = create_user(username="deleteme", email="del@example.com")
    response = await client.delete(f"/user/delete/{u.id}")
    assert response.status_code == 204
