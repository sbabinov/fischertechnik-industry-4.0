import pytest
import asyncio

class TestServerEndpoints:
    @pytest.mark.asyncio
    async def test_write_storage_endpoint(self, test_client, mock_factory, cargo_sample_data):
        response = test_client.post("/write_storage", json={"cargos": cargo_sample_data})

        assert response.status_code == 200
        assert response.json() == {"status": "queued", "task": "write_storage"}

    @pytest.mark.asyncio
    async def test_process_cargos_endpoint(self, test_client, mock_factory, coords_sample_data):
        response = test_client.post("/process_cargos", json={"coords": coords_sample_data})

        assert response.status_code == 200
        assert response.json() == {"status": "queued", "task": "process_cargos"}

    @pytest.mark.asyncio
    async def test_return_cargos_endpoint(self, test_client, mock_factory, cargo_sample_data):
        response = test_client.post("/return_cargos", json={"cargos": cargo_sample_data})

        assert response.status_code == 200
        assert response.json() == {"status": "queued", "task": "return_cargos"}

    @pytest.mark.asyncio
    async def test_sort_cargos_endpoint(self, test_client, mock_factory, cargo_sample_data):
        response = test_client.post("/sort_cargos", json={"cargos": cargo_sample_data})

        assert response.status_code == 200
        assert response.json() == {"status": "queued", "task": "sort_cargos"}

    def test_get_storage_endpoint(self, test_client, mock_factory):
        response = test_client.get("/get_storage")

        assert response.status_code == 200
        assert response.json() == [[4, 4, 4], [4, 4, 4], [4, 4, 4]]

    def test_get_status_endpoint(self, test_client, mock_factory):
        response = test_client.get("/get_status")

        assert response.status_code == 200
        assert response.json() == {
            "storage": "Ожидаю",
            "crane": "Ожидаю",
            "handle_center": "Ожидаю",
            "sort_center": "Ожидаю"
        }

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
