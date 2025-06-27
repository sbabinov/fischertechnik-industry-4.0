from .stages import *
from .stages.stage import Cargo
import asyncio
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

class Factory:
    """ Class for controlling the Fischertechnik factory layout. """
    def __init__(self):
        self.__storage = Storage('192.168.12.37')
        self.__crane = Crane('192.168.12.162')
        self.__handleCenter = HandleCenter('192.168.12.232', '192.168.12.182')
        self.__sortCenter = SortCenter('192.168.12.187')

        self.__manager = multiprocessing.Manager()
        self.__storageData = self.__manager.dict()
        self.__processes = []
        self.__stop_event = multiprocessing.Event()

        self.__queues = {
            'storage-crane': self.__manager.Queue(),  # storage -> crane
            'crane-handle': self.__manager.Queue(),  # crane -> handle
            'handle-sort': self.__manager.Queue(),  # handle -> sort
            'sort-storage': self.__manager.Queue(),  # sort -> storage
            'sort-crane': self.__manager.Queue(),  # sort-> crane
            'crane-storage': self.__manager.Queue()  # crane -> storage
        }

    async def writeStorage(self, storage: list[list[int]]) -> None:
        self.__storage._data = storage
        self.__storageData = storage

    async def getStorage(self, row: int, column: int) -> Cargo:
        """ Get information about cargo in storage cell:
            EMPTY - cell is empty;
            UNDEFINED - cargo inside, but color is undefined;
            WHITE, BLUE, RED - cargo of this color inside. """
        return self.__storageData.get(row, column)

    async def __runProcess(self, target, args):
        """Запускает процесс и добавляет его в список."""
        process = multiprocessing.Process(target=target, args=args)
        process.start()
        self.__processes.append(process)
        return process

    async def sort(self, storage) -> None:
        """ Sort storage cargo. """
        self.__clearQueues()
        self.__stop_event.clear()

        with ProcessPoolExecutor() as executor:
            loop = asyncio.get_event_loop()

            self.__processes = await asyncio.gather(
                loop.run_in_executor(executor, self.__runProcess, self.__storageProcess,
                    ([], storage, self.__queues['crane-storage'], self.__queues['sort-storage'],
                     self.__queues['storage-crane'])),
                loop.run_in_executor(executor, self.__runProcess, self.__craneProcess,
                    (self.__queues['storage-crane'], self.__queues['sort-crane'],
                     self.__queues['crane-storage'], self.__queues['crane-handle'])),
                loop.run_in_executor(executor, self.__runProcess, self.__handleProcess,
                    (self.__queues['crane-handle'], self.__queues['handle-sort'])),
                loop.run_in_executor(executor, self.__runProcess, self.__sortProcess,
                    (True, storage, self.__queues['handle-sort'], self.__queues['sort-storage'],
                     self.__queues['sort-crane']))
            )

    async def processCargo(self, arr) -> None:
        self.__clearQueues()
        self.__stop_event.clear()

        with ProcessPoolExecutor() as executor:
            loop = asyncio.get_event_loop()

            self.__processes = await asyncio.gather(
                loop.run_in_executor(executor, self.__runProcess, self.__storageProcess,
                    ([], [[]], self.__queues['crane-storage'], self.__queues['sort-storage'],
                     self.__queues['storage-crane'])),
                loop.run_in_executor(executor, self.__runProcess, self.__craneProcess,
                    (self.__queues['storage-crane'], self.__queues['sort-crane'],
                     self.__queues['crane-storage'], self.__queues['crane-handle'])),
                loop.run_in_executor(executor, self.__runProcess, self.__handleProcess,
                    (self.__queues['crane-handle'], self.__queues['handle-sort'])),
                loop.run_in_executor(executor, self.__runProcess, self.__sortProcess,
                    (False, [[]], self.__queues['handle-sort'], self.__queues['sort-storage'],
                     self.__queues['sort-crane']))
            )

    async def returnCargo(self, storage) -> None:
        self.__clearQueues()
        self.__stop_event.clear()

        with ProcessPoolExecutor() as executor:
            loop = asyncio.get_event_loop()

            self.__processes = await asyncio.gather(
                loop.run_in_executor(executor, self.__runProcess, self.__storageProcess,
                    ([], storage, self.__queues['crane-storage'], self.__queues['sort-storage'],
                     self.__queues['storage-crane'])),
                loop.run_in_executor(executor, self.__runProcess, self.__craneProcess,
                    (self.__queues['storage-crane'], self.__queues['sort-crane'],
                     self.__queues['crane-storage'], self.__queues['crane-handle'])),
                loop.run_in_executor(executor, self.__runProcess, self.__returnProcess,
                    (storage, self.__queues['sort-storage'], self.__queues['sort-crane']))
            )

    async def stop_processes(self):
        """Безопасно останавливает все процессы."""
        self.__stop_event.set()

        for q in self.__queues.values():
            q.put(None)

        for p in self.__processes:
            p.join(timeout=2.0)
            if p.is_alive():
                p.terminate()

        self.__processes = []

    def __clearQueues(self):
        """Очищает все очереди перед новым запуском процессов."""
        for q in self.__queues.values():
            while not q.empty():
                try:
                    q.get_nowait()
                except:
                    break

    def __storageProcess(self, arr, storage, inputQ2, inputQ4, outputQ2):
        for cell in arr:
            self.__storage.getCargo(cell[0], cell[1])
            outputQ2.put(1)
            self.__storage.putCargo(cell[0], cell[1], Cargo.EMPTY)
        outputQ2.put(None)

        while True:
            cargo = inputQ4.get()
            if cargo is None:
                break
            else:
                cell = []
                for i in range(3):
                    for j in range(3):
                        if storage[i][j] == cargo and self.__storage.getData()[i][j] == Cargo.EMPTY:
                            cell = [i, j]
                            break
                self.__storage.getCargo(cell[0], cell[1])
                outputQ2.put(1)
                while True:
                    item = inputQ2.get()
                    if item is None:
                        break
                    else:
                        self.__storage.putCargo(cell[0], cell[1], cargo)

    def __craneProcess(self, inputQ1, inputQ4, outputQ1, outputQ3):
        while True:
            item = inputQ1.get()
            if item is None:
                break
            else:
                self.__crane.takeFromStorage()
                self.__crane.putInPaintingCenter()
                outputQ3.put(item)
                self.__crane.calibrate()
        outputQ3.put(None)

        while True:
            cargo = inputQ4.get()
            if cargo is None:
                break
            else:
                self.__crane.takeFromSortingCenter(cargo)
                outputQ1.put(1)
                while True:
                    item = inputQ1()
                    if item is None:
                        break
                    else:
                        self.__crane.putInStorage()
                        self.__crane.calibrate()

    def __handleProcess(self, inputQ2, outputQ4):
        while True:
            item = inputQ2.get()
            if item is None:
                break
            else:
                self.__handleCenter.run()
                outputQ4.put(item)
        outputQ4.put(None)

    def __sortProcess(self, shouldReturn, inputQ3, outputQ1, outputQ2):
        while True:
            item = inputQ3.get()
            if item is None:
                break
            else:
                self.__sortCenter.sort()
                if shouldReturn:
                    if self.__sortCenter.getWhite() != 0:
                        self.__sortCenter.decWhite()
                        outputQ1.put(Cargo.WHITE)
                        outputQ2.put(Cargo.WHITE)
                    elif self.__sortCenter.getBlue() != 0:
                        self.__sortCenter.decBlue()
                        outputQ1.put(Cargo.BLUE)
                        outputQ2.put(Cargo.BLUE)
                    else:
                        self.__sortCenter.decRed()
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
