from .stages import *
from .stages.stage import Cargo
from .singleton import singleton
import threading

@singleton
class Factory:
    """ Class for controlling the Fischertechnik factory layout. """
    def __init__(self):
        self.__storage = Storage('192.168.12.37')
        self.__crane = Crane('192.168.12.162')
        self.__shipmentCenter = ShipmentCenter('192.168.12.232')
        self.__paintingCenter = PaintingCenter(self.__shipmentCenter, '192.168.12.182')
        self.__sortingCenter = SortingCenter('192.168.12.137')
        self.__storageLock = threading.Lock()
        self.__craneLock = threading.Lock()
        self.__threadPool = []

    def calibrate(self) -> None:
        """ Calibrates all components. """
        self.__threadPool.clear()
        self.__threadPool.append(threading.Thread(target=self.__storage.calibrate))
        self.__threadPool.append(threading.Thread(target=self.__crane.calibrate))
        self.__threadPool.append(threading.Thread(target=self.__paintingCenter.calibrate))
        self.__threadPool.append(threading.Thread(target=self.__shipmentCenter.calibrate))
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

    def writeStorage(self, storage: list[list[int]]) -> None:
        self.__storage._data = storage

    def getStorage(self, row: int, column: int) -> Cargo:
        """ Get information about cargo in storage cell:
            EMPTY - cell is empty;
            UNDEFINED - cargo inside, but color is undefined;
            WHITE, BLUE, RED - cargo of this color inside. """
        return self.__storage.getData()[row][column]

    def getStatus(self, id: bool) -> bool:
        """ Return information about factory running status:
            id 0 - Storage
            id 1 - Crane
            id 2 - Painting center
            id 3 - Shipment center
            id 4 - Sorting center """
        if id == 0:
            return self.__storage.isRunning()
        elif id == 1:
            return self.__crane.isRunning()
        elif id == 2:
            return self.__paintingCenter.isRunning()
        elif id == 3:
            return self.__shipmentCenter.isRunning()
        elif id == 4:
            return self.__sortingCenter.isRunning()
        else:
            return False

    def processCargo(self, row: int, column: int, wait: bool = True) -> None:
        """ Proces one cargo from storage and put it back. """
        self.calibrate()
        self.__threadPool.append(threading.Thread(target=self.__processCargo, args=[row, column], daemon=True))
        self.__startAll()
        if wait:
            self.__waitAll()

    def sort(self, wait: bool = True) -> None:
        """ Sort storage cargo. """
        self.calibrate()
        self.__threadPool.append(threading.Thread(target=self.__takeFromStorage, daemon=True))
        self.__threadPool.append(threading.Thread(target=self.__takeFromSorting, daemon=True))
        self.__startAll()
        if wait:
            self.__waitAll()

    def __processCargo(self, row: int, column: int) -> None:
        self.__storage._isRunning = True
        self.__storage.getCargo(column + 1, row + 1)
        self.__storage._isRunning = False
        self.__crane._isRunning = True
        self.__crane.takeFromStorage()

        thread = threading.Thread(target=self.__storage.putCargo, args=[column + 1, row + 1, Cargo.EMPTY], daemon=True)
        self.__storage._isRunning = True
        thread.start()
        thread1 = threading.Thread(target=self.__paintingCenter.run, daemon=True)
        self.__paintingCenter._isRunning = True
        thread1.start()
        self.__crane.putInPaintingCenter()
        thread2 = threading.Thread(target=self.__crane.calibrate, daemon=True)
        thread2.start()
        thread1.join()
        self.__crane._isRunning = False
        self.__paintingCenter._isRunning = False

        thread1 = threading.Thread(target=self.__sortingCenter.sort, daemon=True)
        thread1.start()
        self.__shipmentCenter._isRunning = True
        self.__shipmentCenter.run()
        thread.join()
        self.__storage._isRunning = False
        self.__shipmentCenter._isRunning = False
        self.__sortingCenter._isRunning = True
        thread.join()
        self.__sortingCenter._isRunning = False

    def __takeFromStorage(self) -> None:
        with self.__storageLock:
            for i in range(1, 4):
                for j in range(1, 4):
                    self.__storage.getCargo(i, j)
                    with self.__craneLock:
                        self.__crane.takeFromStorage()
                        self.__crane._isRunning = True
                    thread = threading.Thread(target=self.__process, daemon=True)
                    thread.start()

                    cargo = Cargo.UNDEFINED
                    if j == Cargo.WHITE and self.__sortingCenter.getWhite():
                        cargo = Cargo.WHITE
                        self.__sortingCenter.decWhite()
                    elif j == Cargo.BLUE and self.__sortingCenter.getBlue():
                        cargo = Cargo.BLUE
                        self.__sortingCenter.decBlue()
                    elif j == Cargo.RED and self.__sortingCenter.getRed():
                        cargo = Cargo.RED
                        self.__sortingCenter.decRed()

                    if cargo != Cargo.UNDEFINED:
                        with self.__craneLock:
                            self.__crane.takeFromSortingCenter(cargo)
                            self.__crane.putInStorage()
                            thread = threading.Thread(target=self.__crane.calibrate, daemon=True)
                            thread.start()
                            self.__storage.putCargo(i, j, cargo)
                    else:
                        self.__storage.putCargo(i, j, Cargo.EMPTY)

    def __process(self) -> None:
        thread = {}
        with self.__craneLock:
            thread = threading.Thread(target=self.__paintingCenter.run, daemon=True)
            thread.start()
            self.__crane.putInPaintingCenter()
            thread1 = threading.Thread(target=self.__crane.calibrate, daemon=True)
            thread1.start()
            self.__crane._isRunning = False
            thread1.join()
        thread.join()

        thread = threading.Thread(target=self.__sortingCenter.sort, daemon=True)
        thread.start()
        self.__shipmentCenter.run()
        thread.join()

    def __takeFromSorting(self) -> None:
        with self.__storageLock:
            while (self.__sortingCenter.getWhite() or self.__sortingCenter.getBlue() or
                self.__sortingCenter.getRed()):
                cargo = Cargo.UNDEFINED
                if self.__sortingCenter.getWhite():
                    cargo = Cargo.WHITE
                    self.__sortingCenter.decWhite()
                elif self.__sortingCenter.getBlue():
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

    def __findCell(self, cargo: Cargo) -> int:
        for j in range(3):
            if self.__storage.getData()[j][cargo - 1] == Cargo.EMPTY:
                return j
        return 0
