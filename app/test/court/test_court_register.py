import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

from uuid import uuid4
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.service.court import CourtService
from main import app

client = TestClient(app)
endpoint = "court/register"
mock_id = str(uuid4())


def test_register_court_success(
    mock_db_session: Session, mock_court_service: CourtService, override_court_create: None
):
    data = {
        "name": "testCourt",
        "location": "testLocation",
    }

    response = client.post("court/register", json=data)

    assert response.status_code == 201
    assert response.json() == {
        "status_code": 201,
        "message": "Court created successfully",
        "data": {
            "name": "testCourt",
            "location": "testLocation",
        },
    }


def test_register_validation_error(
    mock_db_session: Session, mock_court_service: CourtService, override_court_create: None
):
    data = {"name": "testCourt",}

    response = client.post("court/register", json=data)

    assert response.status_code == 422
    assert response.json() == {
        "status_code": 422,
        "message": "Validation error",
        "errors": [{"field": "location", "message": "Field required"}],
    }


def test_user_already_exist(
    mock_db_session: Session,
    mock_court_service: CourtService,
    override_court_create: None,
    mock_court_exists,
):
    data = {
        "name": "testCourt",
        "location": "testLocation",
    }

    response = client.post("court/register", json=data)

    assert response.status_code == 400
    assert response.json() == {
        "status_code": 400,
        "message": "Court already exists",
    }