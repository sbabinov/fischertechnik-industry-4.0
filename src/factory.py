from .stages import *
from .stages.stage import Cargo
import threading
from concurrent.futures import ThreadPoolExecutor, wait

class Factory:
    def __init__(self):
        self.__storage = Storage('192.168.12.37')
        self.__crane = Crane('192.168.12.162')
        self.__shipment_center = ShipmentCenter('192.168.12.232')
        self.__painting_center = PaintingCenter(self.__shipment_center, '192.168.12.182')
        self.__sort_center = SortCenter('192.168.12.187')
        self.__storage_lock = threading.Lock()
        self.__crane_lock = threading.Lock()
        self.__executor = ThreadPoolExecutor(max_workers=10)

    def __calibrate(self) -> None:
        futures = [
            self.__executor.submit(self.__storage.calibrate),
            self.__executor.submit(self.__crane.calibrate),
            self.__executor.submit(self.__painting_center.calibrate),
            self.__executor.submit(self.__shipment_center.calibrate)
        ]
        wait(futures)

    def write_storage(self, new_storage: list[list[int]]) -> None:
        self.__storage.write_data(new_storage)

    def get_storage(self) -> list[list[int]]:
        return self.__storage.get_data()

    def getStatus(self, id: bool) -> bool:
        if id == 0:
            return self.__storage.isRunning()
        elif id == 1:
            return self.__crane.isRunning()
        elif id == 2:
            return self.__painting_center.isRunning()
        elif id == 3:
            return self.__shipment_center.isRunning()
        elif id == 4:
            return self.__sort_center.isRunning()
        else:
            return False

    def process_cargo(self, row: int, column: int, wait_for_sorting: bool = True) -> None:
        """ Proces one cargo from storage and put it back. """
        self.__calibrate()
        future = self.__executor.submit(self.__process_cargo, row, column)
        if wait_for_sorting:
            future.result()

    def sort(self, wait_for_ending: bool = True) -> None:
        """ Sort storage cargo. """
        self.__calibrate()
        futures = [
            self.__executor.submit(self.__take_from_storage),
            self.__executor.submit(self.__take_from_sorting)
        ]
        if wait_for_ending:
            wait(futures)

    def __process_cargo(self, row: int, column: int) -> None:
        """Process single cargo item using ThreadPoolExecutor."""
        # Set initial statuses
        self.__storage._isRunning = True
        self.__storage.get_cargo(column + 1, row + 1)
        self.__storage._isRunning = False

        self.__crane._isRunning = True
        self.__crane.take_from_storage()

        # Start parallel operations
        storage_future = self.__executor.submit(
            self.__storage.put_cargo, column + 1, row + 1, Cargo.EMPTY
        )
        self.__storage._isRunning = True

        painting_future = self.__executor.submit(self.__painting_center.run)
        self.__painting_center._isRunning = True

        self.__crane.put_in_painting_center()
        crane_calibrate_future = self.__executor.submit(self.__crane.calibrate)

        # Wait for necessary operations
        painting_future.result()
        self.__crane._isRunning = False
        self.__painting_center._isRunning = False

        sort_future = self.__executor.submit(self.__sort_center.sort)
        self.__shipment_center._isRunning = True
        self.__shipment_center.run()

        storage_future.result()
        self.__storage._isRunning = False
        self.__shipment_center._isRunning = False

        sort_future.result()
        self.__sort_center._isRunning = False

    def __take_from_storage(self) -> None:
        """Process all cargo from storage using ThreadPoolExecutor."""
        with self.__storage_lock:
            futures = []
            for i in range(1, 4):
                for j in range(1, 4):
                    self.__storage.get_cargo(i, j)

                    with self.__crane_lock:
                        self.__crane.take_from_storage()
                        self.__crane._isRunning = True

                    # Submit processing task
                    future = self.__executor.submit(self.__process_cargo_task, i, j)
                    futures.append(future)

            # Wait for all tasks to complete
            for future in futures:
                future.result()

    def __process_cargo_task(self, i: int, j: int) -> None:
        """Helper method for processing cargo in parallel."""
        cargo = Cargo.UNDEFINED
        if j == Cargo.WHITE and self.__sort_center.get_color_count(Cargo.WHITE):
            cargo = Cargo.WHITE
            self.__sort_center.dec_color_count(cargo)
        elif j == Cargo.BLUE and self.__sort_center.get_color_count(Cargo.BLUE):
            cargo = Cargo.BLUE
            self.__sort_center.dec_color_count(cargo)
        elif j == Cargo.RED and self.__sort_center.get_color_count(Cargo.RED):
            cargo = Cargo.RED
            self.__sort_center.dec_color_count(cargo)

        if cargo != Cargo.UNDEFINED:
            with self.__crane_lock:
                self.__crane.take_from_sorting_center(cargo)
                self.__crane.put_in_storage()
                self.__executor.submit(self.__crane.calibrate)
                self.__storage.put_cargo(i, j, cargo)
        else:
            self.__storage.put_cargo(i, j, Cargo.EMPTY)

    def __process(self) -> None:
        """Process cargo through painting and sorting centers."""
        with self.__crane_lock:
            painting_future = self.__executor.submit(self.__painting_center.run)
            self.__crane.put_in_painting_center()
            calibrate_future = self.__executor.submit(self.__crane.calibrate)
            self.__crane._isRunning = False
            calibrate_future.result()

        painting_future.result()

        sort_future = self.__executor.submit(self.__sort_center.sort)
        self.__shipment_center.run()
        sort_future.result()

    def __take_from_sorting(self) -> None:
        """Process cargo from sorting center back to storage."""
        with self.__storage_lock:
            while (self.__sort_center.get_color_count(Cargo.WHITE) or
                   self.__sort_center.get_color_count(Cargo.BLUE) or
                   self.__sort_center.get_color_count(Cargo.RED)):

                cargo = Cargo.UNDEFINED
                if self.__sort_center.get_color_count(Cargo.WHITE):
                    cargo = Cargo.WHITE
                    self.__sort_center.dec_color_count(Cargo.WHITE)
                elif self.__sort_center.get_color_count(Cargo.BLUE):
                    cargo = Cargo.BLUE
                    self.__sort_center.dec_color_count(Cargo.BLUE)
                else:
                    cargo = Cargo.RED
                    self.__sort_center.dec_color_count(Cargo.RED)

                j = self.__find_cell(cargo)

                with self.__crane_lock:
                    take_future = self.__executor.submit(
                        self.__crane.take_from_sorting_center, cargo
                    )
                    self.__storage.get_cargo(j + 1, cargo)
                    take_future.result()

                    self.__crane.put_in_storage()
                    self.__executor.submit(self.__crane.calibrate)

                self.__storage.put_cargo(j + 1, cargo, cargo)

    def __find_cell(self, cargo: Cargo) -> int:
        for j in range(3):
            if self.__storage.get_data()[j][cargo - 1] == Cargo.EMPTY:
                return j
        return 0
