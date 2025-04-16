from .stages import *
from .stages.stage import Cargo
from .singleton import singleton
import threading

@singleton
class Factory:
    """ Class for controlling the Fischertechnik factory layout. """

    def __init__(self):
        self.__storage = Storage('192.168.137.247')
        self.__crane = Crane('192.168.137.74')
        self.__shipmentCenter = ShipmentCenter('192.168.137.201')
        self.__paintingCenter = PaintingCenter(self.__shipmentCenter, '192.168.137.77')
        self.__sortingCenter = SortingCenter('192.168.137.138')
        self.__storageLock = threading.Lock()
        self.__craneLock = threading.Lock()
        self.__threadPool = []

    def calibrate(self) -> None:
        """ Calibrates all components. """
        self.__threadPool.append(threading.Thread(target=self.__storage.calibrate, daemon=True))
        self.__threadPool.append(threading.Thread(target=self.__crane.calibrate, daemon=True))
        self.__threadPool.append(threading.Thread(target=self.__paintingCenter.calibrate, daemon=True))
        self.__threadPool.append(threading.Thread(target=self.__shipmentCenter.calibrate, daemon=True))
        self.__startAll()
        self.__waitAll()

    def __waitAll(self):
        for thread in self.__threadPool:
            thread.join()
        self.__threadPool.clear()

    def __startAll(self):
        for thread in self.__threadPool:
            thread.start()

    def wait(self):
        self.__waitAll()

    def getStorage(self, row, column) -> Cargo:
        """ Get information about cargo in storage cell:
            EMPTY - cell is empty;
            UNDEFINED - cargo inside, but color is undefined;
            WHITE, BLUE, RED - cargo of this color inside. """
        return self.__storage.getData()[row][column]

    def sort(self, wait: bool = True) -> None:
        """ Sort storage cargo. """
        self.calibrate()
        self.__threadPool.append(threading.Thread(target=self.__takeFromStorage, daemon=True))
        self.__threadPool.append(threading.Thread(target=self.__process, daemon=True))
        self.__threadPool.append(threading.Thread(target=self.__takeFromSorting, daemon=True))
        self.__startAll()
        if wait:
            self.__waitAll()

    def __takeFromStorage(self) -> None:
        with self.__storageLock:
            for i in range(1, 4):
                for j in range(1, 4):
                    self.__storage.getCargo(i, j)
                    with self.__craneLock:
                        self.__crane.takeFromStorage()
                        self.__crane._isRunning = True
                    self.__storage.putCargo(i, j, Cargo.EMPTY)

    def __process(self) -> None:
        count = 0
        while count != 9:
            while not self.__crane.isRunning():
                pass

            thread = threading.Thread(target=self.__paintingCenter.run, daemon=True)
            thread.start()
            with self.__craneLock:
                self.__crane.putInPaintingCenter()
                thread1 = threading.Thread(target=self.__crane.calibrate(), daemon=True)
                thread1.start()
                self.__crane._isRunning = False
            thread.join()

            thread = threading.Thread(target=self.__sortingCenter.sort, daemon=True)
            thread.start()
            self.__shipmentCenter.run()
            thread.join()

            count += 1

    def __takeFromSorting(self) -> None:
        with self.__storageLock:
            while self.__sortingCenter.getWhite() != 0 or self.__sortingCenter.getBlue() != 0 or self.__sortingCenter.getRed() != 0:
                cargo = Cargo.UNDEFINED
                if self.__sortingCenter.getWhite() != 0:
                    cargo = Cargo.WHITE
                    self.__sortingCenter.decWhite()
                elif self.__sortingCenter.getBlue() != 0:
                    cargo = Cargo.BLUE
                    self.__sortingCenter.decBlue()
                else:
                    cargo = Cargo.RED
                    self.__sortingCenter.decRed()

                j = self.__findCell(cargo)

                with self.__craneLock:
                    thread = threading.Thread(target=self.__crane.takeFromSortingCenter, args=[cargo], daemon=True)
                    thread.start()
                    self.__storage.getCargo(j + 1, cargo)
                    thread.join()
                    self.__crane.putInStorage()
                    thread = threading.Thread(target=self.__crane.calibrate, daemon=True)
                    thread.start()
                self.__storage.putCargo(j + 1, cargo, cargo)

    def __findCell(self, cargo) -> int:
        for j in range(3):
            if self.__storage.getData()[j][cargo - 1] == Cargo.EMPTY:
                return j
        return 0
