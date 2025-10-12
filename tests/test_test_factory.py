import pytest
from tests.mock_factory import MockFactory
from src.core.stages.stage import Cargo

class TestMockFactory:
    @pytest.fixture
    def test_factory(self):
        return MockFactory({})

    def test_initial_state(self, test_factory):
        storage = test_factory.get_storage()

        assert len(storage) == 3
        assert all(len(row) == 3 for row in storage)
        assert all(cargo == Cargo.UNDEFINED for row in storage for cargo in row)

    def test_initial_status(self, test_factory):
        status = test_factory.get_status()

        expected_status = {
            "storage": "Ожидаю",
            "crane": "Ожидаю",
            "handle_center": "Ожидаю",
            "sort_center": "Ожидаю"
        }
        assert status == expected_status

    @pytest.mark.asyncio
    async def test_write_storage(self, test_factory):
        new_storage = [
            [Cargo.WHITE, Cargo.BLUE, Cargo.RED],
            [Cargo.EMPTY, Cargo.WHITE, Cargo.BLUE],
            [Cargo.RED, Cargo.EMPTY, Cargo.WHITE]
        ]

        await test_factory.write_storage(new_storage)

        result_storage = test_factory.get_storage()
        assert result_storage == new_storage

    @pytest.mark.asyncio
    async def test_process_cargos(self, test_factory):
        initial_storage = [
            [Cargo.WHITE, Cargo.BLUE, Cargo.RED],
            [Cargo.EMPTY, Cargo.WHITE, Cargo.BLUE],
            [Cargo.RED, Cargo.EMPTY, Cargo.WHITE]
        ]
        await test_factory.write_storage(initial_storage)

        coords_to_process = [[0, 0], [1, 1], [2, 2]]
        await test_factory.process_cargos(coords_to_process)

        result_storage = test_factory.get_storage()

        assert result_storage[0][0] == Cargo.EMPTY
        assert result_storage[1][1] == Cargo.EMPTY
        assert result_storage[2][2] == Cargo.EMPTY
        assert result_storage[0][1] == Cargo.BLUE
        assert result_storage[0][2] == Cargo.RED
        assert result_storage[1][0] == Cargo.EMPTY
        assert result_storage[1][2] == Cargo.BLUE
        assert result_storage[2][0] == Cargo.RED
        assert result_storage[2][1] == Cargo.EMPTY

    @pytest.mark.asyncio
    async def test_return_cargos(self, test_factory):
        new_storage = [
            [Cargo.WHITE, Cargo.BLUE, Cargo.RED],
            [Cargo.EMPTY, Cargo.WHITE, Cargo.BLUE],
            [Cargo.RED, Cargo.EMPTY, Cargo.WHITE]
        ]

        await test_factory.return_cargos(new_storage)

        result_storage = test_factory.get_storage()
        assert result_storage == new_storage

    @pytest.mark.asyncio
    async def test_sort_cargos(self, test_factory):
        initial_storage = [
            [Cargo.WHITE, Cargo.BLUE, Cargo.RED],
            [Cargo.EMPTY, Cargo.WHITE, Cargo.BLUE],
            [Cargo.RED, Cargo.EMPTY, Cargo.WHITE]
        ]
        await test_factory.write_storage(initial_storage)

        new_storage = [
            [Cargo.BLUE, Cargo.BLUE, Cargo.BLUE],
            [Cargo.WHITE, Cargo.WHITE, Cargo.WHITE],
            [Cargo.RED, Cargo.RED, Cargo.RED]
        ]

        await test_factory.sort_cargos(new_storage)

        result_storage = test_factory.get_storage()
        assert result_storage == new_storage

    @pytest.mark.asyncio
    async def test_status_during_operation(self, test_factory):
        status_before = test_factory.get_status()
        assert all(status == "Ожидаю" for status in status_before.values())

        await test_factory.process_cargos([[0, 0]])

        status_after = test_factory.get_status()
        assert all(status == "Ожидаю" for status in status_after.values())
