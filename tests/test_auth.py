import json
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_user_register():
    response = client.post("/auth/register", json={
        "email": "userr22@example.com", "hashed_password": "123456",
        "username": "userr22"
    })

    assert response.status_code == 200
    assert response.json()["email"] == "userr22@example.com"
    assert "Confirmation email has been sent" in response.json()["detail"]


def test_user_login(client):
    register_response = client.post("/auth/register", json={
            "email": "loginuser@example.com",
            "username": "loginuser",
            "hashed_password": "123456"
        })
    assert register_response.status_code == 200

    login_response = client.post("/auth/login", json={
            "email": "loginuser@example.com",
            "hashed_password": "123456"
        })
    assert login_response.status_code == 200
    tokens = login_response.json()

    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"