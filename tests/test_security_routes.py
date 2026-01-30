import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_for_access_token(client: AsyncClient, create_user):
    create_user(username="authuser", password="authpass", email="auth@example.com")
    response = await client.post("/security/token", params={
        "login": "authuser",
        "pwd": "authpass",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, create_user):
    create_user(username="badlogin", password="realpass", email="bad@example.com")
    response = await client.post("/security/token", params={
        "login": "badlogin",
        "pwd": "wrongpass",
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, create_user):
    create_user(username="meuser", password="mepass", email="me@example.com")
    # First, get a token
    token_resp = await client.post("/security/token", params={
        "login": "meuser",
        "pwd": "mepass",
    })
    assert token_resp.status_code == 200
    token = token_resp.json()["access_token"]

    # Use token to access /security/users/me
    response = await client.get("/security/users/me", headers={
        "Authorization": f"Bearer {token}",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "meuser"
