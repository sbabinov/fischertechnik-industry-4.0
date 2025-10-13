import pytest
from pydantic import ValidationError
from src import CargoListRequest, CoordsListRequest
from src import Cargo

class TestModels:
    def test_cargo_list_request_valid(self):
        data = {
            "cargos": [
                [Cargo.WHITE, Cargo.BLUE, Cargo.RED],
                [Cargo.EMPTY, Cargo.UNDEFINED, Cargo.WHITE]
            ]
        }
        request = CargoListRequest(**data)
        assert request.cargos == data["cargos"]

    def test_cargo_list_request_invalid(self):
        with pytest.raises(ValidationError):
            CargoListRequest(cargos="invalid")

    def test_coords_list_request_empty(self):
        data = {"coords": []}
        request = CoordsListRequest(**data)
        assert request.coords == []
