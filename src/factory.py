from .stages import *
from .stages.stage import Cargo
import threading

class Factory:
    def __init__(self):
        self.__storage = Storage('192.168.12.37')
        self.__crane = Crane('192.168.12.162')
        self.__shipmentCenter = ShipmentCenter('192.168.12.232')
        self.__paintingCenter = PaintingCenter(self.__shipmentCenter, '192.168.12.182')
        self.__sortCenter = SortCenter('192.168.12.187')
        self.__storageLock = threading.Lock()
        self.__craneLock = threading.Lock()
        self.__threadPool = []

    def __calibrate(self) -> None:
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

    def write_storage(self, new_storage: list[list[int]]) -> None:
        self.__storage.write_data(new_storage)

    def get_storage(self, row: int, column: int) -> Cargo:
        return self.__storage.get_data()[row][column]

    def getStatus(self, id: bool) -> bool:
        if id == 0:
            return self.__storage.isRunning()
        elif id == 1:
            return self.__crane.isRunning()
        elif id == 2:
            return self.__paintingCenter.isRunning()
        elif id == 3:
            return self.__shipmentCenter.isRunning()
        elif id == 4:
            return self.__sortCenter.isRunning()
        else:
            return False

    def processCargo(self, row: int, column: int, wait: bool = True) -> None:
        """ Proces one cargo from storage and put it back. """
        self.__calibrate()
        self.__threadPool.append(threading.Thread(target=self.__processCargo, args=[row, column], daemon=True))
        self.__startAll()
        if wait:
            self.__waitAll()

    def sort(self, wait: bool = True) -> None:
        """ Sort storage cargo. """
        self.__calibrate()
        self.__threadPool.append(threading.Thread(target=self.__takeFromStorage, daemon=True))
        self.__threadPool.append(threading.Thread(target=self.__takeFromSorting, daemon=True))
        self.__startAll()
        if wait:
            self.__waitAll()

    def __processCargo(self, row: int, column: int) -> None:
        self.__storage._isRunning = True
        self.__storage.get_cargo(column + 1, row + 1)
        self.__storage._isRunning = False
        self.__crane._isRunning = True
        self.__crane.take_from_storage()

        thread = threading.Thread(target=self.__storage.put_cargo, args=[column + 1, row + 1, Cargo.EMPTY], daemon=True)
        self.__storage._isRunning = True
        thread.start()
        thread1 = threading.Thread(target=self.__paintingCenter.run, daemon=True)
        self.__paintingCenter._isRunning = True
        thread1.start()
        self.__crane.put_in_painting_center()
        thread2 = threading.Thread(target=self.__crane.calibrate, daemon=True)
        thread2.start()
        thread1.join()
        self.__crane._isRunning = False
        self.__paintingCenter._isRunning = False

        thread1 = threading.Thread(target=self.__sortCenter.sort, daemon=True)
        thread1.start()
        self.__shipmentCenter._isRunning = True
        self.__shipmentCenter.run()
        thread.join()
        self.__storage._isRunning = False
        self.__shipmentCenter._isRunning = False
        self.__sortCenter._isRunning = True
        thread.join()
        self.__sortCenter._isRunning = False

    def __takeFromStorage(self) -> None:
        with self.__storageLock:
            for i in range(1, 4):
                for j in range(1, 4):
                    self.__storage.get_cargo(i, j)
                    with self.__craneLock:
                        self.__crane.take_from_storage()
                        self.__crane._isRunning = True
                    thread = threading.Thread(target=self.__process, daemon=True)
                    thread.start()

                    cargo = Cargo.UNDEFINED
                    if j == Cargo.WHITE and self.__sortCenter.get_color_count(Cargo.WHITE):
                        cargo = Cargo.WHITE
                        self.__sortCenter.dec_color_count(cargo)
                    elif j == Cargo.BLUE and self.__sortCenter.get_color_count(Cargo.BLUE):
                        cargo = Cargo.BLUE
                        self.__sortCenter.dec_color_count(cargo)
                    elif j == Cargo.RED and self.__sortCenter.get_color_count(Cargo.RED):
                        cargo = Cargo.RED
                        self.__sortCenter.dec_color_count(cargo)


                    if cargo != Cargo.UNDEFINED:
                        with self.__craneLock:
                            self.__crane.take_from_sorting_center(cargo)
                            self.__crane.put_in_storage()
                            thread = threading.Thread(target=self.__crane.calibrate, daemon=True)
                            thread.start()
                            self.__storage.put_cargo(i, j, cargo)
                    else:
                        self.__storage.put_cargo(i, j, Cargo.EMPTY)

    def __process(self) -> None:
        thread = {}
        with self.__craneLock:
            thread = threading.Thread(target=self.__paintingCenter.run, daemon=True)
            thread.start()
            self.__crane.put_in_painting_center()
            thread1 = threading.Thread(target=self.__crane.calibrate, daemon=True)
            thread1.start()
            self.__crane._isRunning = False
            thread1.join()
        thread.join()

        thread = threading.Thread(target=self.__sortCenter.sort, daemon=True)
        thread.start()
        self.__shipmentCenter.run()
        thread.join()

    def __takeFromSorting(self) -> None:
        with self.__storageLock:
            while (self.__sortCenter.get_color_count(Cargo.WHITE) or self.__sortCenter.get_color_count(Cargo.BLUE) or
                self.__sortCenter.get_color_count(Cargo.RED)):
                cargo = Cargo.UNDEFINED
                if self.__sortCenter.get_color_count(Cargo.WHITE):
                    cargo = Cargo.WHITE
                    self.__sortCenter.dec_color_count(Cargo.WHITE)
                elif self.__sortCenter.get_color_count(Cargo.BLUE):
                    cargo = Cargo.BLUE
                    self.__sortCenter.dec_color_count(Cargo.BLUE)
                else:
                    cargo = Cargo.RED
                    self.__sortCenter.dec_color_count(Cargo.RED)

                j = self.__findCell(cargo)

                with self.__craneLock:
                    thread = threading.Thread(target=self.__crane.take_from_sorting_center, args=[cargo], daemon=True)
                    thread.start()
                    self.__storage.get_cargo(j + 1, cargo)
                    thread.join()
                    self.__crane.put_in_storage()
                    thread = threading.Thread(target=self.__crane.calibrate, daemon=True)
                    thread.start()
                self.__storage.put_cargo(j + 1, cargo, cargo)

    def __findCell(self, cargo: Cargo) -> int:
        for j in range(3):
            if self.__storage.get_data()[j][cargo - 1] == Cargo.EMPTY:
                return j
        return 0
