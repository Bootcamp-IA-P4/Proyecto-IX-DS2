import pytest
from fast_api.main import app
from fastapi.testclient import TestClient

@pytest.fixture(scope="module")
def client():
    return TestClient(app)
