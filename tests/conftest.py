import pytest
from unittest.mock import Mock, AsyncMock
from fastapi.testclient import TestClient

@pytest.fixture
def mock_factory():
    factory = Mock()
    factory.write_storage = AsyncMock()
    factory.process_cargos = AsyncMock()
    factory.return_cargos = AsyncMock()
    factory.sort_cargos = AsyncMock()
    factory.get_storage = Mock(return_value=[[1, 1, 1], [2, 2, 2], [3, 3, 3]])
    factory.get_status = Mock(return_value={
        "storage": "Ожидаю",
        "crane": "Ожидаю", 
        "handle_center": "Ожидаю",
        "sort_center": "Ожидаю"
    })
    return factory

@pytest.fixture
def test_client(mock_factory):
    from ..src.api.server import create_app
    app, _, _ = create_app(mock_factory)
    return TestClient(app)

@pytest.fixture
def cargo_sample_data():
    return [[1, 1, 1], [2, 2, 2], [3, 3, 3]]

@pytest.fixture
def coords_sample_data():
    return [[0, 0], [1, 1], [2, 2]]
