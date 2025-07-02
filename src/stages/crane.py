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
        for motor_id in 2, 3, 1:
            Motor(self._stage, motor_id).calibrate()
        Motor(self._stage, 1).move(-925)
        Motor(self._stage, 2).move(-10)
        Motor(self._stage, 3).move(-10)

    def take_from_storage(self) -> None:
        distances = (-480, -250, -170)

        self.__move(distances)
        self.generator.move(wait=False)
        out = self._stage.output(8)
        out.setLevel(512)
        time.sleep(2)
        self.__moveBack(distances)

    def take_from_sort_center(self, color: Cargo) -> None:
        if color == Cargo.WHITE:
            distances = (460, -890, -375)
        elif color == Cargo.RED:
            distances = (610, -890, -585)
        else:
            distances = (542, -890, -420)

        self.__move(distances)
        self.generator.move(wait=False)
        out = self._stage.output(8)
        out.setLevel(512)
        time.sleep(2)
        self.__moveBack(distances)

    def put_in_storage(self) -> None:
        distances = (-475, -250, -195)

        self.__move(distances)
        self.generator.stop()
        self.__moveBack(distances)

    def put_in_handle_center(self) -> None:
        distances = (1, -600, -870)

        self.__move(distances)
        self.generator.stop()
        self.__moveBack(distances)
