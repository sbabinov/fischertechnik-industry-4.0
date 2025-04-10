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
        self.arm_z.move(-distances[1] + (1 if distances[1] > 0 else -1))
        self.arm_x.move(-distances[2] + (1 if distances[2] > 0 else -1))
        self.tower.move(-distances[0] + (1 if distances[0] > 0 else -1))

    def calibrate(self) -> None:
        """ Calibrates all crane motors. """
        for motor_id in 2, 3, 1:
            Motor(self._stage, motor_id).calibrate()
        Motor(self._stage, 1).move(-925)

    def takeFromStorage(self) -> None:
        """ The crane takes a cargo from the storage and returns to the calibrated position. """
        distances = (-475, -250, -195)

        self.__move(distances)
        self.generator.move(wait=False)
        out = self._stage.output(8)
        out.setLevel(512)
        time.sleep(2)
        self.__moveBack(distances)

    def takeFromSortingCenter(self, color) -> None:
        """ The crane takes a cargo from the sorting center and returns to the calibrated position. """
        if color == Cargo.WHITE:
            distances = (465, -860, -375)
        elif color == Cargo.RED:
            distances = (545, -860, -420)
        else:
            distances = (615, -860, -600)

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
        distances = (5, -600, -870)

        self.__move(distances)
        self.generator.stop()
        self.__moveBack(distances)
