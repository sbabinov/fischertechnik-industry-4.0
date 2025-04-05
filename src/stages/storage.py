import time

from .stage import Stage

# speed = -512
# motor = txt.motor(2)
# motor.setSpeed(speed)
# motor.setDistance(780)
# while not motor.finished():
#     txt.updateWait()
# vert_motor = txt.motor(0)
# vert_motor.setSpeed(-512)
# vert_motor.setDistance(100)
# while not vert_motor.finished():
#     txt.updateWait()


class Storage(Stage):
    def __init__(self, host: str, port: int = 65000):
        super().__init__(host, port)
        self._horiz_motor = self._stage.motor(3)
        self._vert_motor = self._stage.motor(4)
        self._rail_motor = self._stage.motor(2)
        self._delivery_motor = self._stage.motor(1)
        self._coords_map = dict()
        self._coords_map.update({(1, 1): (780, 0)})
        self._coords_map.update({(2, 1): (1370, 0)})
        self._coords_map.update({(3, 1): (1985, 0)})
        self._coords_map.update({(1, 2): (780, 380)})
        self._coords_map.update({(2, 2): (1370, 380)})
        self._coords_map.update({(3, 2): (1985, 380)})
        self._coords_map.update({(1, 3): (780, 770)})
        self._coords_map.update({(2, 3): (1370, 770)})
        self._coords_map.update({(3, 3): (1985, 770)})
        self.__reset_sensors()

    def __reset_sensors(self):
        for i in range(1, 10):
            iteration = list()
            for i in range(1, 9):
                sensor = self._stage.resistor(i)
                iteration.append(sensor.value())

    def __should_horizont_backward_stop(self):
        sensor_backward = self._stage.resistor(6)
        if sensor_backward.value() != 15000:
            return True

    def __should_horizont_forward_stop(self):
        sensor_forward = self._stage.resistor(7)
        if sensor_forward.value() != 15000:
            return True

    def __should_vertical_stop(self):
        sensor = self._stage.resistor(8)
        if sensor.value() != 15000:
            return True

    def __should_rail_stop(self):
        sensor = self._stage.resistor(5)
        if sensor.value() != 15000:
            return True

    def __push_manipulator(self):
        self._horiz_motor.setSpeed(-512)
        self._horiz_motor.setDistance(512)
        while not self.__should_horizont_forward_stop():
            pass
        self._horiz_motor.stop()

    def __pull_manipulator(self):
        self._horiz_motor.setSpeed(512)
        self._horiz_motor.setDistance(512)
        while not self.__should_horizont_backward_stop():
            pass
        self._horiz_motor.stop()

    def __move_rail(self, distance: int):
        if distance == 0:
            return
        speed = -512
        if distance < 0:
            speed = 512
        self._rail_motor.setSpeed(speed)
        self._rail_motor.setDistance(abs(distance))
        while not self._rail_motor.finished():
            if distance < 0 and self.__should_rail_stop():
                break
        self._rail_motor.stop()

    def __move_vert(self, distance: int):
        if distance == 0:
            return
        speed = -512
        if distance < 0:
            speed = 512

        self._vert_motor.setSpeed(speed)
        self._vert_motor.setDistance(abs(distance))
        while not self._vert_motor.finished():
            if distance < 0 and self.__should_vertical_stop():
                break
        self._vert_motor.stop()

    def __deliver_cargo(self):
        if self._stage.resistor(4).value() != 15000:
            return

        self._delivery_motor.setSpeed(-512)
        self._delivery_motor.setDistance(1)
        while not self._stage.resistor(1).value() == 15000:
            pass
        self._delivery_motor.stop()

    def get_cargo(self, x: int, y: int):
        coords = self._coords_map.get((x, y))
        self.__move_rail(coords[0])
        self.__move_vert(coords[1])
        self.__move_vert(100)
        self.__push_manipulator()
        self.__move_vert(-100)
        self.calibrate()
        self.__push_manipulator()
        self.__move_vert(800)
        self.__deliver_cargo()
        self.calibrate()

    def calibrate(self):
        self.__pull_manipulator()

        self.__move_rail(-2000)
        self.__move_vert(-2000)
