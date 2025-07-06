from .stages import *
from .stages.stage import Cargo
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor, wait

class Factory:
    def __init__(self, ips):
        self.__storage = Storage(ips['storage_ip'])
        self.__crane = Crane(ips['crane_ip'])
        self.__sort_center = SortCenter(ips['sort_center_ip'])
        self.__handle_center = HandleCenter(ips['shipment_center_ip'], ips['paint_center_ip'])

        self.__storage_lock = threading.Lock()
        self.__crane_lock = threading.Lock()
        self.__executor = ThreadPoolExecutor(max_workers=10)

    def get_storage(self) -> list[list[Cargo]]:
        return self.__storage.get_data()

    def get_status(self) -> dict[str: str]:
        return {
            "storage": self.__storage.status,
            "crane": self.__crane.status,
            "handle_center": self.__handle_center.status,
            "sort_center": self.__sort_center.status
        }

    async def write_storage(self, new_storage: list[list[Cargo]]) -> None:
        await asyncio.get_event_loop().run_in_executor(self.__executor, self.__storage.write_data, new_storage)

    async def process_cargos(self, coords: list[list[int]]) -> None:
        await asyncio.get_event_loop().run_in_executor(self.__executor, self.__calibrate)
        await asyncio.get_event_loop().run_in_executor(self.__executor, self.__process_cargos, coords)

    async def return_cargos(self, new_storage: list[list[Cargo]]) -> None:
        await asyncio.get_event_loop().run_in_executor(self.__executor, self.__calibrate)
        await asyncio.get_event_loop().run_in_executor(self.__executor, self.__return_cargos, new_storage)

    async def sort_cargos(self, new_storage: list[list[Cargo]]) -> None:
        await asyncio.get_event_loop().run_in_executor(self.__executor, self.__calibrate)
        await asyncio.get_event_loop().run_in_executor(self.__executor, self.__sort_cargos, new_storage)

    def __calibrate(self) -> None:
        futures = [
            self.__executor.submit(self.__storage.calibrate),
            self.__executor.submit(self.__crane.calibrate),
            self.__executor.submit(self.__handle_center.calibrate)
        ]
        wait(futures)

    def __process_cargos(self, arr: list[list[int]]):
        for coords in arr:
            self.__take_cargo(coords)
            self.__executor.submit(self.__return_empty_cargo, coords)
            self.__executor.submit(self.__process_cargo)

    def __return_cargos(self, new_storage: list[list[Cargo]]):
            for i in range(3):
                for j in range(3):
                    color = new_storage[i][j]
                    current_color = self.__storage.get_data()[i][j]
                    if current_color == color or current_color != Cargo.EMPTY:
                        continue
                    else:
                        self.__return_cargo(color, [i, j])

    def __sort_cargos(self, new_storage: list[list[Cargo]]):
        for i in range(3):
            for j in range(3):
                self.__take_cargo([i, j])
                self.__process_cargo()
                if self.__sort_center.get_color_count(new_storage[i][j]):
                    arr = [i, j]
                    self.__return_cargo(new_storage[i][j], arr)
                else:
                    self.__storage.put_cargo(i, j, Cargo.EMPTY)
        self.__return_cargos(new_storage)

    def __take_cargo(self, coords: list[int]):
        with self.__storage_lock:
            with self.__crane_lock:
                self.__storage.get_cargo(coords[0], coords[1])
                self.__crane.take_from_storage()

    def __process_cargo(self):
        with self.__crane_lock:
            self.__crane.put_in_handle_center()
            self.__executor.submit(self.__crane.calibrate)
        self.__handle_center.process()
        self.__sort_center.sort()

    def __return_empty_cargo(self, coords):
        with self.__storage_lock:
            self.__storage.put_cargo(coords[0], coords[1], Cargo.EMPTY)

    def __return_cargo(self, color: Cargo, coords: list[int]):
        with self.__storage_lock:
            future = self.__executor.submit(self.__storage.get_cargo, coords[0], coords[1])
            with self.__crane_lock:
                self.__crane.take_from_sort_center(color)
                future.result()
                self.__crane.put_in_storage()
                self.__executor.submit(self.__crane.calibrate)
            self.__storage.put_cargo(coords[0], coords[1], color)
