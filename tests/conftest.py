import pytest
from fastapi.testclient import TestClient
from src import MockFactory

@pytest.fixture
def mock_factory():
    factory = MockFactory({})
    return factory

@pytest.fixture
def test_client(mock_factory):
    from src import create_app
    app, _, _ = create_app(mock_factory)
    return TestClient(app)

@pytest.fixture
def cargo_sample_data():
    return [[1, 1, 1], [2, 2, 2], [3, 3, 3]]

@pytest.fixture
def coords_sample_data():
    return [[0, 0], [1, 1], [2, 2]]
