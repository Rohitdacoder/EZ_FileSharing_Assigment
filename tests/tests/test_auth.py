from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup_and_login():
    email = "testuser@example.com"
    password = "testpass123"

    # Signup
    response = client.post("/auth/signup", json={
        "email": email,
        "password": password,
        "role": "client"
    })
    assert response.status_code == 200
    assert "verify_url" in response.json()

    # Simulate email verification (normally, user clicks link)
    token = response.json()["verify_url"].split("=")[-1]
    verify_response = client.get(f"/auth/verify?token={token}")
    assert verify_response.status_code == 200

    # Login
    login_response = client.post("/auth/login", json={
        "email": email,
        "password": password
    })
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
