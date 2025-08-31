import sys
import os
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.db.main import get_session
from src.db.models import Book
from src.main import app
from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import Mock
import pytest
import uuid

mock_session = Mock()
mock_user_service = Mock()
mock_book_service =Mock()

def get_mock_session():
    yield mock_session



app.dependency_overrides[get_session] = get_mock_session



@pytest.fixture
def fake_session():
    return mock_session


@pytest.fixture
def fake_user_service():
    return mock_user_service


@pytest.fixture
def fake_book_service():
    return mock_book_service

@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def test_book():
    return Book(
        uid=uuid.uuid4(),
        user_uid=uuid.uuid4(),
        title="sample title",
        description="sample description",
        page_count=200,
        language="English",
        published_date=datetime.now(),
        update_at=datetime.now()
    )