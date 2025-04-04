from .stage import Stage

speed = -512
motor = txt.motor(2)
motor.setSpeed(speed)
motor.setDistance(780)
while not motor.finished():
    txt.updateWait()
vert_motor = txt.motor(0)
vert_motor.setSpeed(-512)
vert_motor.setDistance(100)
while not vert_motor.finished():
    txt.updateWait()


class Storage(Stage):
    def __init__(self, host: str, port: int = 65000):
        super().__init__(host, port)
        self._horiz_motor = self._stage.motor(3)
        self._vert_motor = self._stage.motor(0)
        self._rail_motor = self._stage.motor(2)

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
        self._horiz_motor.setDistance(1)
        while not self.__should_horizont_forward_stop():
            pass
        self._horiz_motor.stop()

    def __pull_manipulator(self):
        self._horiz_motor.setSpeed(512)
        self._horiz_motor.setDistance(1)
        while not self.__should_horizont_backward_stop():
            pass
        self._horiz_motor.stop()

    def calibrate(self):
        self.__reset_sensors()
        vertical_speed = 400
        rail_speed = 400

        self.__pull_manipulator()

        self._vert_motor.setSpeed(vertical_speed)
        self._vert_motor.setDistance(2000)

        self._rail_motor.setSpeed(rail_speed)
        self._rail_motor.setDistance(20000)

        is_calibrated = False

        while not is_calibrated:
            cond_first = self.__should_vertical_stop()
            cond_second = self.__should_rail_stop()
            if cond_first:
                self._vert_motor.stop()
            if cond_second:
                self._rail_motor.stop()
            is_calibrated = cond_first and cond_second
