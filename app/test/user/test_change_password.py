import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app

client = TestClient(app)
endpoint = "user/123/password"

def test_change_password(
    mock_db_session: Session,
    access_token,
    current_user,
    mock_change_password,
):
    body = {
        "password": "test0000",
        "new_password": "test5678"
    }

    response = client.patch(
        endpoint,
        headers={"authorization": f"Bearer {access_token}"},
        json=body
    )

    data = response.json()

    assert response.status_code == 200
    assert data["status_code"] == 200
    assert data["message"] == "User password changed successfully"

def test_change_password_side_effect(
    mock_db_session: Session,
    access_token,
    current_user,
    mock_change_password_effect,
):
    body = {
        "password": "test0000",
        "new_password": "test5678"
    }

    response = client.patch(
        endpoint,
        headers={"authorization": f"Bearer {access_token}"},
        json=body
    )

    data = response.json()

    
    assert response.status_code == 403
    assert data["status_code"] == 403
    assert data["message"] == "You do not have permission to update this profile"

def test_wrong_password(
        mock_db_session: Session,
        access_token,
        current_user,
        mock_wrong_password_effect
):
    body = {
        "password": "test0000",
        "new_password": "test5678"
    }

    response = client.patch(
        endpoint,
        headers={"authorization": f"Bearer {access_token}"},
        json=body
    )

    data = response.json()

    
    assert response.status_code == 400
    assert data["status_code"] == 400
    assert data["message"] == "Incorrect Password"