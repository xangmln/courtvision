import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from unittest.mock import patch
from uuid import uuid4
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.service.user import UserService, user_service
from app.model.user import User
from main import app

client = TestClient(app)
endpoint = "auth/logout"


def test_logout_success(
    mock_db_session: Session,
    access_token,
    current_user,
):
    response = client.post(
        endpoint, headers={"Authorization": f"Bearer {access_token}"}
    )

    data = response.json()

    assert response.status_code == 200
    assert data["status_code"] == 200
    assert data["message"] == "User logged out successfully"