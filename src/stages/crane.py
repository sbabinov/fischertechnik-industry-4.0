from .stage import Stage

class Crane(Stage):
    def calibrate(self) -> None:
        """ Calibrates all crane motors. """
        for i in 1, 2, 3:
            sensor = self._stage.resistor(i)
            while sensor.value() == 0:
                sensor = self._stage.resistor(i)
            motor = self._stage.motor(i)
            motor.setSpeed(512)
            motor.setDistance(10000)

            while not motor.finished():
                if sensor.value() != 15000:
                    motor.stop()
                    break
                sensor = self._stage.resistor(i)
                self._stage.updateWait()

        motor = self._stage.motor(1)
        motor.setSpeed(-512)
        motor.setDistance(925)
        self._stage.wait(motor)

    def takeFromStorage(self) -> None:
        motor1 = self._stage.motor(1)
        motor1.setSpeed(-512)
        motor1.setDistance(475)
        self.wait(motor1)

        motor3 = self._stage.motor(3)
        motor3.setSpeed(-512)
        motor3.setDistance(200)
        self.wait(motor3)

        motor2 = self._stage.motor(2)
        motor2.setSpeed(-512)
        motor2.setDistance(190)
        self.wait(motor2)

        motor4 = self._stage.motor(4)
        motor4.setSpeed(512)
        motor4.setDistance(1024)
        out = self._stage.output(8)
        out.setLevel(512)
        self.wait(motor4)

    def takeFromPaintingCenter(self) -> None:
        ...

    def takeFromSortingCenter(self) -> None:
        ...

    def putInStorage(self) -> None:
        ...

    def putInPaintingCenter(self) -> None:
        ...
