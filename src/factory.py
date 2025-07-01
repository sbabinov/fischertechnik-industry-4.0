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

class Factory:
    def __init__(self):
        self.__storageIp = '192.168.12.37'
        self.__craneIp = '192.168.12.162'
        self.__handleCenterIps = ('192.168.12.232', '192.168.12.182')
        self.__sortCenterIp = '192.168.12.187'

        self.__manager = multiprocessing.Manager()
        self.__storageData = self.__manager.dict()
        self.__processes = []
        self.__stop_event = multiprocessing.Event()

        default_storage = {
            (i, j): Cargo.EMPTY for i in range(3) for j in range(3)
        }
        self.__storageData.update(default_storage)

        self.__queues = {
            'storage_crane': self.__manager.Queue(),
            'crane_handle': self.__manager.Queue(),
            'handle_sort': self.__manager.Queue(),
            'sort_storage': self.__manager.Queue(),
            'sort_crane': self.__manager.Queue(),
            'crane_storage': self.__manager.Queue()
        }

    async def writeStorage(self, storage: list[list[int]]) -> None:
        self.__storageData.update(storage)

    async def getStorage(self, row: int, column: int) -> Cargo:
        return self.__storageData.get((row, column), Cargo.EMPTY)

    async def sort(self, storage) -> None:
        self.__clearQueues()
        self.__stop_event.clear()

        with ProcessPoolExecutor() as executor:
            loop = asyncio.get_event_loop()

            self.__processes = await asyncio.gather(
                loop.run_in_executor(executor, _run_process, self.__storageProcess,
                    ([], storage, self.__queues['crane_storage'], self.__queues['sort_storage'],
                     self.__queues['storage_crane'])))
            #     loop.run_in_executor(executor, _run_process, self.__craneProcess,
            #         (self.__queues['storage_crane'], self.__queues['sort_crane'],
            #          self.__queues['crane_storage'], self.__queues['crane_handle'])),
            #     loop.run_in_executor(executor, _run_process, self.__handleProcess,
            #         (self.__queues['crane_handle'], self.__queues['handle_sort'])),
            #     loop.run_in_executor(executor, _run_process, self.__sortProcess,
            #         (True, storage, self.__queues['handle_sort'], self.__queues['sort_storage'],
            #          self.__queues['sort_crane']))
            # )

    async def processCargo(self, arr) -> None:
        self.__clearQueues()
        self.__stop_event.clear()

        with ProcessPoolExecutor() as executor:
            loop = asyncio.get_event_loop()

            self.__processes = await asyncio.gather(
                loop.run_in_executor(executor, _run_process, self.__storageProcess,
                    ([], [[]], self.__queues['crane_storage'], self.__queues['sort_storage'],
                     self.__queues['storage_crane'])))
            #     loop.run_in_executor(executor, _run_process, self.__craneProcess,
            #         (self.__queues['storage_crane'], self.__queues['sort_crane'],
            #          self.__queues['crane_storage'], self.__queues['crane_handle'])),
            #     loop.run_in_executor(executor, _run_process, self.__handleProcess,
            #         (self.__queues['crane_handle'], self.__queues['handle_sort'])),
            #     loop.run_in_executor(executor, _run_process, self.__sortProcess,
            #         (False, [[]], self.__queues['handle_sort'], self.__queues['sort_storage'],
            #          self.__queues['sort_crane']))
            # )

    async def returnCargo(self, storage) -> None:
        self.__clearQueues()
        self.__stop_event.clear()

        with ProcessPoolExecutor() as executor:
            loop = asyncio.get_event_loop()

            self.__processes = await asyncio.gather(
                loop.run_in_executor(executor, _run_process, self.__storageProcess,
                    ([], storage, self.__queues['crane_storage'], self.__queues['sort_storage'],
                     self.__queues['storage_crane'])),
                loop.run_in_executor(executor, _run_process, self.__craneProcess,
                    (self.__queues['storage_crane'], self.__queues['sort_crane'],
                     self.__queues['crane_storage'], self.__queues['crane_handle'])),
                loop.run_in_executor(executor, _run_process, self.__returnProcess,
                    (storage, self.__queues['sort_storage'], self.__queues['sort_crane']))
            )

    def __calibrate(self):
        storageObj = Storage(self.__storageIp)
        craneObj = Crane(self.__craneIp)
        handleObj = HandleCenter(self.__handleCenterIps[0], self.__handleCenterIps[1])
        sortObj = SortCenter(self.__sortCenterIp)
        components = [
            storageObj,
            craneObj,
            handleObj,
            sortObj
        ]

        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(component.calibrate) for component in components]

            for future in concurrent.futures.as_completed(futures):
                future.result()

    async def stopProcesses(self):
        self.__stop_event.set()

        for q in self.__queues.values():
            q.put(None)

        for p in self.__processes:
            p.join(timeout=2.0)
            if p.is_alive():
                p.terminate()
        self.__processes = []

    def __clearQueues(self):
        for q in self.__queues.values():
            while not q.empty():
                try:
                    q.get_nowait()
                except:
                    break

    def __storageProcess(self, arr, storage, inputQ2, inputQ4, outputQ2):
        storageObj = Storage(self.__storageIp)
        storageObj.write_data(self.__storageData.get())

        for cell in arr:
            storageObj.getCargo(cell[0], cell[1])
            outputQ2.put(1)
            storageObj.putCargo(cell[0], cell[1], Cargo.EMPTY)
        outputQ2.put(None)

        while True:
            cargo = inputQ4.get()
            if cargo is None:
                break
            else:
                cell = []
                for i in range(3):
                    for j in range(3):
                        if storage[i][j] == cargo and storageObj.getData()[i][j] == Cargo.EMPTY:
                            cell = [i, j]
                            break
                storageObj.getCargo(cell[0], cell[1])
                outputQ2.put(1)
                while True:
                    item = inputQ2.get()
                    if item is None:
                        break
                    else:
                        storageObj.putCargo(cell[0], cell[1], cargo)

    def __craneProcess(self, inputQ1, inputQ4, outputQ1, outputQ3):
        craneObj = Crane(self.__craneIp)
        while True:
            item = inputQ1.get()
            if item is None:
                break
            else:
                craneObj.takeFromStorage()
                craneObj.putInPaintingCenter()
                outputQ3.put(item)
                craneObj.calibrate()
        outputQ3.put(None)

        while True:
            cargo = inputQ4.get()
            if cargo is None:
                break
            else:
                craneObj.takeFromSortingCenter(cargo)
                outputQ1.put(1)
                while True:
                    item = inputQ1()
                    if item is None:
                        break
                    else:
                        craneObj.putInStorage()
                        craneObj.calibrate()

    def __handleProcess(self, inputQ2, outputQ4):
        handleObj = HandleCenter(self.__handleCenterIps[0], self.__handleCenterIps[1])
        while True:
            item = inputQ2.get()
            if item is None:
                break
            else:
                handleObj.process()
                outputQ4.put(item)
        outputQ4.put(None)

    def __sortProcess(self, shouldReturn, inputQ3, outputQ1, outputQ2):
        sortObj = SortCenter(self.__sortCenterIp)
        while True:
            item = inputQ3.get()
            if item is None:
                break
            else:
                sortObj.sort()
                if shouldReturn:
                    if sortObj.getWhite() != 0:
                        sortObj.decWhite()
                        outputQ1.put(Cargo.WHITE)
                        outputQ2.put(Cargo.WHITE)
                    elif sortObj.getBlue() != 0:
                        sortObj.decBlue()
                        outputQ1.put(Cargo.BLUE)
                        outputQ2.put(Cargo.BLUE)
                    else:
                        sortObj.decRed()
                        outputQ1.put(Cargo.RED)
                        outputQ2.put(Cargo.RED)
        outputQ1.put(None)
        outputQ2.put(None)

    def __returnProcess(self, storage, outputQ1, outputQ2):
        for i in range(3):
            for j in range(3):
                outputQ1.put(storage[i][j])
                outputQ2.put(storage[i][j])
        outputQ1.put(None)
        outputQ2.put(None)
