import time
from typing import Tuple
from .stage import Stage, Cargo, Motor

class Crane(Stage):
    def __init__(self, host: str, port: int = 65000):
        super().__init__(host, port)
        self.tower = Motor(self._stage, 1)
        self.arm_z = Motor(self._stage, 2)
        self.arm_x = Motor(self._stage, 3)
        self.generator = Motor(self._stage, 4)

    def __move(self, distances: Tuple) -> None:
        self.tower.move(distances[0])
        self.arm_x.move(distances[2])
        self.arm_z.move(distances[1])

    def __moveBack(self, distances: Tuple) -> None:
        self.arm_z.move(-distances[1])
        self.arm_x.move(-distances[2])
        self.tower.move(-distances[0])

    def calibrate(self) -> None:
        """ Calibrates all crane motors. """
        for motor_id in 2, 3, 1:
            Motor(self._stage, motor_id).calibrate()
        Motor(self._stage, 1).move(-925)
        Motor(self._stage, 2).move(-10)
        Motor(self._stage, 3).move(-10)

    def takeFromStorage(self) -> None:
        """ The crane takes a cargo from the storage and returns to the calibrated position. """
        distances = (-480, -250, -170)

        self.__move(distances)
        self.generator.move(wait=False)
        out = self._stage.output(8)
        out.setLevel(512)
        time.sleep(2)
        self.__moveBack(distances)

    def takeFromSortingCenter(self, color) -> None:
        """ The crane takes a cargo from the sorting center and returns to the calibrated position. """
        if color == Cargo.WHITE:
            distances = (460, -890, -375)
        elif color == Cargo.RED:
            distances = (542, -890, -420)
        else:
            distances = (610, -890, -585)

        self.__move(distances)
        self.generator.move(wait=False)
        out = self._stage.output(8)
        out.setLevel(512)
        time.sleep(2)
        self.__moveBack(distances)

    def putInStorage(self) -> None:
        """ The crane puts a cargo in the storage and returns to the calibrated position. """
        distances = (-475, -250, -195)

        self.__move(distances)
        self.generator.stop()
        self.__moveBack(distances)

    def putInPaintingCenter(self) -> None:
        """ The crane puts a cargo in the painting center and returns to the calibrated position. """
        distances = (1, -600, -870)

        self.__move(distances)
        self.generator.stop()
        self.__moveBack(distances)
