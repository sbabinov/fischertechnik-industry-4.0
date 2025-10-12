import pytest
from fastapi.testclient import TestClient

class TestServerEndpoints:
    def test_write_storage_endpoint(self, test_client, test_factory, cargo_sample_data):
        response = test_client.post("/write_storage", json={"cargos": cargo_sample_data})

        assert response.status_code == 200
        assert response.json() == {"status": "queued", "task": "write_storage"}
        test_factory.write_storage.assert_called_once()

    def test_process_cargos_endpoint(self, test_client, test_factory, coords_sample_data):
        response = test_client.post("/process_cargos", json={"coords": coords_sample_data})

        assert response.status_code == 200
        assert response.json() == {"status": "queued", "task": "process_cargos"}
        test_factory.process_cargos.assert_called_once_with(coords=coords_sample_data)

    def test_return_cargos_endpoint(self, test_client, test_factory, cargo_sample_data):
        response = test_client.post("/return_cargos", json={"cargos": cargo_sample_data})

        assert response.status_code == 200
        assert response.json() == {"status": "queued", "task": "return_cargos"}
        test_factory.return_cargos.assert_called_once()

    def test_sort_cargos_endpoint(self, test_client, test_factory, cargo_sample_data):
        response = test_client.post("/sort_cargos", json={"cargos": cargo_sample_data})

        assert response.status_code == 200
        assert response.json() == {"status": "queued", "task": "sort_cargos"}
        test_factory.sort_cargos.assert_called_once()

    def test_get_storage_endpoint(self, test_client, test_factory):
        response = test_client.get("/get_storage")

        assert response.status_code == 200
        assert response.json() == [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
        test_factory.get_storage.assert_called_once()

    def test_get_status_endpoint(self, test_client, test_factory):
        response = test_client.get("/get_status")

        assert response.status_code == 200
        assert response.json() == {
            "storage": "Ожидаю",
            "crane": "Ожидаю",
            "handle_center": "Ожидаю",
            "sort_center": "Ожидаю"
        }
        test_factory.get_status.assert_called_once()

    def test_queue_status_endpoint(self, test_client):
        response = test_client.get("/queue_status")

        assert response.status_code == 200
        data = response.json()
        assert "queue_size" in data
        assert "tasks_in_progress" in data
        assert isinstance(data["queue_size"], int)
        assert isinstance(data["tasks_in_progress"], int)

    def test_invalid_payload_returns_error(self, test_client):
        response = test_client.post("/write_storage", json={"invalid": "data"})
        assert response.status_code == 422

class TestServerValidation:
    def test_cargo_list_request_validation(self):
        from src.models import CargoListRequest

        valid_data = {"cargos": [[1, 2, 3], [4, 5, 6]]}
        request = CargoListRequest(**valid_data)
        assert request.cargos == [[1, 2, 3], [4, 5, 6]]

        with pytest.raises(ValueError):
            invalid_data = {"cargos": "not_a_list"}
            CargoListRequest(**invalid_data)

    def test_coords_list_request_validation(self):
        from src.models import CoordsListRequest

        valid_data = {"coords": [[0, 0], [1, 1], [2, 2]]}
        request = CoordsListRequest(**valid_data)
        assert request.coords == [[0, 0], [1, 1], [2, 2]]

        with pytest.raises(ValueError):
            invalid_data = {"coords": [[0, 0, 0]]}
            CoordsListRequest(**invalid_data)
