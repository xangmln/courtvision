import os
import sys


sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)

from fastapi import HTTPException, status
import pytest
from uuid import uuid4
from main import app
from unittest.mock import patch
from app.utils.dependencies import get_db
from app.service.court import court_service
from app.model.court import Court

mock_id = str(uuid4())


@pytest.fixture
def mock_court_service():
    with patch("app.service.court.court_service", autospec=True) as mock_court_service:
        yield mock_court_service


@pytest.fixture
def override_court_create():
    with patch(
        "app.service.court.CourtService.create_court", autospec=True
    ) as mock_court_create:
        mock_court_create.return_value = {
            "name": "testCourt",
            "location": "testLocation"
        }
        yield mock_court_create


@pytest.fixture
def mock_court_exists():
    with patch("app.service.court.CourtService.create_court") as mock_court_create:
        mock_court_create.side_effect = HTTPException(
            status.HTTP_400_BAD_REQUEST, "Court already exists"
        )

        yield mock_court_create



