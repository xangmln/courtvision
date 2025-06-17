from fastapi import HTTPException
import pytest
from unittest.mock import patch

from app.model.user import User
from app.service.user import user_service
from main import app

@pytest.fixture
def mock_get_users():
    with patch("app.service.user.user_service.fetch_all") as fetch_users:
        fetch_users.return_value = [
            {"id": 1, "username": "sam"},
            {"id": 2, "username": "test"},
            {"id": 3, "username": "john"},
        ]

        yield fetch_users

@pytest.fixture
def mock_user_detail():
    with patch("app.service.user.user_service.get_user_detail") as user_detail:
        user_detail.return_value = {
            "id": "12345",
            "username": "test",
            "email": "test@test.com",
        }

        yield user_detail
@pytest.fixture
def mock_delete_user():
    with patch(
        "app.service.user.user_service.delete_user_profile"
    ) as delete_user_profile:
        yield delete_user_profile


@pytest.fixture
def mock_delete_user_effect():
    with patch(
        "app.service.user.user_service.delete_user_profile"
    ) as delete_user_profile:
        delete_user_profile.side_effect = HTTPException(
            403, "You do not have permission to delete this user"
        )

        yield delete_user_profile

@pytest.fixture
def mock_user_update():
    with patch(
        "app.service.user.user_service.update_user_profile"
    ) as update_user_profile:
        update_user_profile.return_value = {
            "id": "12345",
            "username": "test",
            "email": "test@test.com",
        }

        yield update_user_profile


@pytest.fixture
def mock_user_update_effect():
    with patch(
        "app.service.user.user_service.get_user_detail"
    ) as user_detail_effect:
        user_detail_effect.side_effect = HTTPException(
            403, "You do not have permission to update this profile"
        )

        yield user_detail_effect
