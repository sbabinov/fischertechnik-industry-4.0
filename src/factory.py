from .stages import *
from .stages.stage import Cargo
import asyncio
import concurrent
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

def _run_process(target, args):
    process = multiprocessing.Process(target=target, args=args)
    process.start()
    return process

def _storage_process(storage_ip, arr, new_storage, input_q2, input_q4, output_q2):
    storage_obj = Storage(storage_ip)
    for cell in arr:
        storage_obj.get_cargo(cell[0], cell[1])
        output_q2.put(1)
        storage_obj.put_cargo(cell[0], cell[1], Cargo.EMPTY)
    output_q2.put(None)

    while True:
        cargo = input_q4.get()
        if cargo is None:
            break
        else:
            cell = []
            for i in range(3):
                for j in range(3):
                    if new_storage[i][j] == cargo and storage_obj.get_data()[i][j] == Cargo.EMPTY:
                        cell = [i, j]
                        break
            storage_obj.get_cargo(cell[0], cell[1])
            output_q2.put(1)
            while True:
                item = input_q2.get()
                if item is None:
                    break
                else:
                    storage_obj.put_cargo(cell[0], cell[1], cargo)

def _crane_process(crane_ip, input_q1, input_q4, output_q1, output_q3):
    crane_obj = Crane(crane_ip)
    while True:
        item = input_q1.get()
        if item is None:
            break
        else:
            crane_obj.takeFromStorage()
            crane_obj.putInPaintingCenter()
            output_q3.put(item)
            crane_obj.calibrate()
    output_q3.put(None)

    while True:
        cargo = input_q4.get()
        if cargo is None:
            break
        else:
            crane_obj.takeFromSortingCenter(cargo)
            output_q1.put(1)
            while True:
                item = input_q1.get()
                if item is None:
                    break
                else:
                    crane_obj.putInStorage()
                    crane_obj.calibrate()

def _handle_process(handle_ips, input_q2, output_q4):
    handle_obj = HandleCenter(handle_ips[0], handle_ips[1])
    while True:
        item = input_q2.get()
        if item is None:
            break
        else:
            handle_obj.process()
            output_q4.put(item)
    output_q4.put(None)

def _sort_process(sort_ip, should_return, input_q3, output_q1, output_q2):
    sort_obj = SortCenter(sort_ip)
    while True:
        item = input_q3.get()
        if item is None:
            break
        else:
            sort_obj.sort()
            if should_return:
                if sort_obj.getWhite() != 0:
                    sort_obj.decWhite()
                    output_q1.put(Cargo.WHITE)
                    output_q2.put(Cargo.WHITE)
                elif sort_obj.getBlue() != 0:
                    sort_obj.decBlue()
                    output_q1.put(Cargo.BLUE)
                    output_q2.put(Cargo.BLUE)
                else:
                    sort_obj.decRed()
                    output_q1.put(Cargo.RED)
                    output_q2.put(Cargo.RED)
    output_q1.put(None)
    output_q2.put(None)

def _return_process(new_storage, output_q1, output_q2):
    for i in range(3):
        for j in range(3):
            output_q1.put(new_storage[i][j])
            output_q2.put(new_storage[i][j])
    output_q1.put(None)
    output_q2.put(None)

class Factory:
    def __init__(self):
        self.__storage_ip = '192.168.12.37'
        self.__crane_ip = '192.168.12.162'
        self.__handle_ips = ('192.168.12.232', '192.168.12.182')
        self.__sort_ip = '192.168.12.187'

        self.__manager = multiprocessing.Manager()
        self.__storage_data = self.__manager.dict()
        self.__processes = []
        self.__stop_event = multiprocessing.Event()

        default_storage = {
            (i, j): Cargo.EMPTY for i in range(3) for j in range(3)
        }
        self.__storage_data.update(default_storage)

        self.__queues = {
            'storage_crane': self.__manager.Queue(),
            'crane_handle': self.__manager.Queue(),
            'handle_sort': self.__manager.Queue(),
            'sort_storage': self.__manager.Queue(),
            'sort_crane': self.__manager.Queue(),
            'crane_storage': self.__manager.Queue()
        }

    async def write_storage(self, new_storage: list[list[int]]) -> None:
        self.__storage_data.update(new_storage)

    async def get_storage(self, row: int, column: int) -> Cargo:
        return self.__storage_data.get((row, column), Cargo.EMPTY)

    async def sort(self, new_storage) -> None:
        self.__clear_queues()
        self.__stop_event.clear()
        self.__calibrate()

        with ProcessPoolExecutor() as executor:
            self.__processes = [
                executor.submit(
                    _storage_process,
                    self.__storage_ip, [[1, 1], [1, 2], [1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3]], new_storage,
                    self.__queues['crane_storage'], self.__queues['sort_storage'],
                    self.__queues['storage_crane']
                ),
                executor.submit(
                    _crane_process,
                    self.__crane_ip, self.__queues['storage_crane'],
                    self.__queues['sort_crane'], self.__queues['crane_storage'],
                    self.__queues['crane_handle']
                ),
                executor.submit(
                    _handle_process,
                    self.__handle_ips, self.__queues['crane_handle'],
                    self.__queues['handle_sort']
                ),
                executor.submit(
                    _sort_process,
                    self.__sort_ip, True, self.__queues['handle_sort'],
                    self.__queues['sort_storage'], self.__queues['sort_crane']
                )
            ]

    async def process_cargo(self, arr) -> None:
        self.__clear_queues()
        self.__stop_event.clear()

        with ProcessPoolExecutor() as executor:
            loop = asyncio.get_event_loop()

            self.__processes = await asyncio.gather(
                loop.run_in_executor(executor, _run_process, _storage_process,
                    (self.__storage_ip, arr, [[]], self.__queues['crane_storage'], self.__queues['sort_storage'],
                     self.__queues['storage_crane'])),
                loop.run_in_executor(executor, _run_process, _crane_process,
                    (self.__crane_ip, self.__queues['storage_crane'], self.__queues['sort_crane'],
                     self.__queues['crane_storage'], self.__queues['crane_handle'])),
                loop.run_in_executor(executor, _run_process, _handle_process,
                    (self.__handle_ips, self.__queues['crane_handle'], self.__queues['handle_sort'])),
                loop.run_in_executor(executor, _run_process, _sort_process,
                    (self.__sort_ip, False, self.__queues['handle_sort'], self.__queues['sort_storage'],
                     self.__queues['sort_crane']))
            )

    async def return_cargo(self, new_storage) -> None:
        self.__clear_queues()
        self.__stop_event.clear()

        with ProcessPoolExecutor() as executor:
            loop = asyncio.get_event_loop()

            self.__processes = await asyncio.gather(
                loop.run_in_executor(executor, _run_process, _storage_process,
                    (self.__storage_ip, [], new_storage, self.__queues['crane_storage'], self.__queues['sort_storage'],
                     self.__queues['storage_crane'])),
                loop.run_in_executor(executor, _run_process, _crane_process,
                    (self.__crane_ip, self.__queues['storage_crane'], self.__queues['sort_crane'],
                     self.__queues['crane_storage'], self.__queues['crane_handle'])),
                loop.run_in_executor(executor, _run_process, _return_process,
                    (new_storage, self.__queues['sort_storage'], self.__queues['sort_crane']))
            )

    def __calibrate(self):
        storage_obj = Storage(self.__storage_ip)
        crane_obj = Crane(self.__crane_ip)
        handle_obj = HandleCenter(self.__handle_ips[0], self.__handle_ips[1])

        storage_obj.calibrate()
        crane_obj.calibrate()
        handle_obj.calibrate()

    async def stop_processes(self):
        self.__stop_event.set()

        for q in self.__queues.values():
            q.put(None)

        for p in self.__processes:
            p.join(timeout=2.0)
            if p.is_alive():
                p.terminate()
        self.__processes = []

    def __clear_queues(self):
        for q in self.__queues.values():
            while not q.empty():
                try:
                    q.get_nowait()
                except:
                    break