import pytest
from fastapi.testclient import TestClient
from src.images.endpoints.app import app


@pytest.fixture(scope="session")
def test_app():
    return TestClient(app)
