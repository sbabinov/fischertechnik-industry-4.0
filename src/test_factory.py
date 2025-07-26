from time import sleep

from stages import *
from stages.stage import Cargo
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor, wait

class Factory:
    def __init__(self, ips):
        self.__data = [[Cargo.UNDEFINED for _ in range(3)] for _ in range(3)]
        self.__storage_status = "Ожидаю"
        self.__crane_status = "Ожидаю"
        self.__handle_center_status = "Ожидаю"
        self.__sort_center_status = "Ожидаю"
        self.__executor = ThreadPoolExecutor(max_workers=10)

    def get_storage(self) -> list[list[Cargo]]:
        return self.__data

    def get_status(self) -> dict[str: str]:
        return {
            "storage": self.__storage_status,
            "crane": self.__crane_status,
            "handle_center": self.__handle_center_status,
            "sort_center": self.__sort_center_status
        }
    def __write_data(self, new_storage):
        self.__data = new_storage

    def __imitate_process(self, arr):
        for coords in arr:
            self.__data[coords[0]][coords[1]] = Cargo.EMPTY

    def __imitate(self):
        self.__storage_status = "Работаю"
        self.__crane_status = "Работаю"
        self.__handle_center_status = "Работаю"
        self.__sort_center_status = "Работаю"
        sleep(10)
        self.__storage_status = "Ожидаю"
        self.__crane_status = "Ожидаю"
        self.__handle_center_status = "Ожидаю"
        self.__sort_center_status = "Ожидаю"

    async def write_storage(self, new_storage: list[list[Cargo]]) -> None:
        await asyncio.get_event_loop().run_in_executor(self.__executor, self.__write_data, new_storage)

    async def process_cargos(self, coords: list[list[int]]) -> None:
        await asyncio.get_event_loop().run_in_executor(self.__executor, self.__imitate)
        await asyncio.get_event_loop().run_in_executor(self.__executor, self.__imitate_process, coords)

    async def return_cargos(self, new_storage: list[list[Cargo]]) -> None:
        await asyncio.get_event_loop().run_in_executor(self.__executor, self.__imitate)
        await asyncio.get_event_loop().run_in_executor(self.__executor, self.__write_data, new_storage)

    async def sort_cargos(self, new_storage: list[list[Cargo]]) -> None:
        await asyncio.get_event_loop().run_in_executor(self.__executor, self.__imitate)
        await asyncio.get_event_loop().run_in_executor(self.__executor, self.__write_data, new_storage)
