from anyio import sleep

from .stage import Stage, Cargo, resetConfigCounter

class Storage(Stage):
    def __init__(self, host: str, port: int = 65000):
        super().__init__(host, port)
        self._x = 2500
        self._y = 2500
        self._horiz_motor = self._stage.motor(3)
        self._vert_motor = self._stage.motor(4)
        self._rail_motor = self._stage.motor(2)
        self._delivery_motor = self._stage.motor(1)
        self._coords_map = dict()
        self._coords_map.update({(1, 1): (780, 0)})
        self._coords_map.update({(2, 1): (1380, 0)})
        self._coords_map.update({(3, 1): (1990, 0)})
        self._coords_map.update({(1, 2): (780, 380)})
        self._coords_map.update({(2, 2): (1380, 380)})
        self._coords_map.update({(3, 2): (1990, 380)})
        self._coords_map.update({(1, 3): (780, 780)})
        self._coords_map.update({(2, 3): (1380, 780)})
        self._coords_map.update({(3, 3): (1990, 780)})
        self._data = [[Cargo.UNDEFINED for _ in range(3)] for _ in range(3)]
        self.__reset_sensors()
        self.status = "Ожидаю"

    def __reset_sensors(self):
        for i in range(1, 10):
            iteration = list()
            for i in range(1, 9):
                sensor = self.__safety_resistor(i)
                iteration.append(sensor.value())

    def __safety_resistor(self, num: int):
        return self._stage.resistor(num)

    def __should_horizont_backward_stop(self):
        sensor_backward = self.__safety_resistor(6)
        if sensor_backward.value() != 15000:
            return True

    def __should_horizont_forward_stop(self):
        sensor_forward = self.__safety_resistor(7)
        if sensor_forward.value() != 15000:
            return True

    def __should_vertical_stop(self):
        sensor = self.__safety_resistor(8)
        if sensor.value() != 15000:
            return True

    def __should_rail_stop(self):
        sensor = self.__safety_resistor(5)
        if sensor.value() != 15000:
            return True

    def __push_manipulator(self):
        if self.__should_horizont_forward_stop():
            return
        self._horiz_motor.setSpeed(-512)
        self._horiz_motor.setDistance(512)
        while not self.__should_horizont_forward_stop():
            pass
        self._horiz_motor.stop()

    def __pull_manipulator(self):
        if self.__should_horizont_backward_stop():
            return
        self._horiz_motor.setSpeed(512)
        self._horiz_motor.setDistance(512)
        while not self.__should_horizont_backward_stop():
            pass
        self._horiz_motor.stop()

    @resetConfigCounter
    def __move_delta(self, x: int, y: int, z: int):
        rail_speed = -512
        vert_speed = -512
        conveyer_speed = -512
        if x < 0:
            rail_speed = 512
        if y < 0:
            vert_speed = 512
        if z < 0:
            conveyer_speed = 512

        rail_stopped = True
        vert_stopped = True
        conveyer_stopped = True
        if x != 0:
            self._rail_motor.setSpeed(rail_speed)
            self._rail_motor.setDistance(abs(x))
            rail_stopped = False
        if y != 0:
            self._vert_motor.setSpeed(vert_speed)
            self._vert_motor.setDistance(abs(y))
            vert_stopped = False

        if z != 0:
            self._delivery_motor.setSpeed(conveyer_speed)
            self._delivery_motor.setDistance(1000)
            sleep(10)
            conveyer_stopped = False

        motors_stopped = rail_stopped and vert_stopped and conveyer_stopped
        while not motors_stopped:
            if x < 0 and self.__should_rail_stop():
                self._rail_motor.stop()
                rail_stopped = True
            if y < 0 and self.__should_vertical_stop():
                self._vert_motor.stop()
                vert_stopped = True
            if z > 0 and self.__safety_resistor(1).value() == 15000:
                self._delivery_motor.stop()
                conveyer_stopped = True

            if z < 0 and self.__safety_resistor(4).value() == 15000:
                self._delivery_motor.stop()
                conveyer_stopped = True
            rail_stopped = rail_stopped or self._rail_motor.finished()
            vert_stopped = vert_stopped or self._vert_motor.finished()
            motors_stopped = rail_stopped and vert_stopped and conveyer_stopped

        self._x += x
        self._y += y

    def __move_to(self, x: int, y: int, z = 0):
        self.__move_delta(x - self._x, y - self._y, z)

    def __pick_up_cargo(self):
        self.__move_delta(0, 50, 0)
        self.__push_manipulator()
        self.__move_delta(0, -50, 0)
        self.__pull_manipulator()

    def __drop_cargo(self):
        self.__push_manipulator()
        self.__move_delta(0, 50, 0)
        self.__pull_manipulator()
        self.__move_delta(0, -50, 0)

    def get_cargo(self, x: int, y: int) -> None:
        self.status = f"Беру заготовку из ячейки [{x}, {y}]"
        coords = self._coords_map.get((x + 1, y + 1))
        self.__move_to(coords[0], coords[1])
        self.__pick_up_cargo()
        self.__move_to(0, 650)
        self.__drop_cargo()
        self.__move_to(0, 0, 1)
        self.calibrate()
        self._data[x][y] = Cargo.EMPTY
        self.status = "Ожидаю"

    def put_cargo(self, x: int, y: int, color: Cargo) -> None:
        self.status = f"Кладу {color} заготовку в ячейку [{x}, {y}]"
        self.__move_to(0, 650)
        coords = self._coords_map.get((x + 1, y + 1))
        self.__move_to(0, 650, -1)
        self.__pick_up_cargo()
        self.__move_to(coords[0], coords[1])
        self.__drop_cargo()
        self._data[x][y] = color
        self.status = "Ожидаю"

    def get_data(self) -> list[list[Cargo]]:
        transposed = [[self._data[j][i] for j in range(len(self._data))] for i in range(len(self._data[0]))]
        return transposed

    def write_data(self, matrix: list[list[Cargo]]) -> None:
        self._data = matrix

    def calibrate(self) -> None:
        self.status = "Калибруюсь"
        self.__pull_manipulator()
        self.__move_delta(-2500, -2500, 0)
        self._x = 0
        self._y = 0
        self.status = "Ожидаю"
