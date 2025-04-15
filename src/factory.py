from .stages import *
from stages.stage import Cargo
from .singleton import singleton
import threading

@singleton
class Factory:
    """ Class for controlling the Fischertechnik factory layout. """

    def __init__(self):
        self.__storage = Storage('')
        self.__crane = Crane('')
        self.__paintingCenter = PaintingCenter('')
        self.__shipmentCenter = ShipmentCenter('')
        self.__sortingCenter = SortingCenter('')
        self.__storageLock = threading.Lock()
        self.__craneLock = threading.Lock()

    def calibrate(self) -> None:
        """ Calibrates all components. """
        t1 = threading.Thread(target = self.__storage.calibrate)
        t2 = threading.Thread(target = self.__crane.calibrate)
        t3 = threading.Thread(target = self.__paintingCenter.calibrate)
        t4 = threading.Thread(target = self.__shipmentCenter.calibrate)
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()

    def getStorage(self, row, column) -> Cargo:
        """ Get information about cargo in storage cell:
            EMPTY - cell is empty;
            UNDEFINED - cargo inside, but color is undefined;
            WHITE, BLUE, RED - cargo of this color inside. """
        return self.__storage.getData()[row][column]

    def sort(self) -> None:
        """ Sort storage cargo. """
        self.calibrate()

        takeFromStorageThread = threading.Thread(target = self.__takeFromStorage)
        processThread = threading.Thread(target = self.__process)
        takeFromSortingThread = threading.Thread(target = self.__takeFromSorting)

        takeFromStorageThread.start()
        processThread.start()
        takeFromSortingThread.start()

        takeFromStorageThread.join()
        processThread.join()
        takeFromSortingThread.join()

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

            thread = threading.Thread(target = self.__paintingCenter.run)
            thread.start()
            with self.__craneLock:
                self.__crane.putInPaintingCenter()
                self.__crane._isRunning = False
            thread.join()

            thread = threading.Thread(target = self.__sortingCenter.sort)
            thread.start()
            self.__shipmentCenter.run()
            thread.join()

            count += 1

    def __takeFromSorting(self) -> None:
        with self.__storageLock:
            while self.__sortingCenter.getWhite() != 0 or self.__sortingCenter.getBlue() != 0 or self.__sortingCenter.getRed() != 0:
                cargo = Cargo.RED
                if self.__sortingCenter.getWhite != 0:
                    cargo = Cargo.WHITE
                elif self.__sortingCenter.getBlue != 0:
                    cargo = Cargo.BLUE

                j = self.__findCell(cargo)
                self.__storage.getCargo(cargo, j)

                with self.__craneLock:
                    self.__crane.takeFromSortingCenter(cargo)
                    self.__crane.putInStorage()
                self.__storage.putCargo(cargo, j, cargo)
                self.__storage.getData()[cargo][j] = cargo

    def __findCell(self, cargo) -> int:
        for j in range(3):
            if self.__storage.getData()[cargo][j] == Cargo.EMPTY:
                return j
        return 0
