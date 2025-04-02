import ftrobopy

class Cargo:
    WHITE = 1
    RED = 2
    BLUE = 3

class Motor:
    def __init__(self, stage, motor_id):
        self.__stage = stage
        self.__motor_id = motor_id
        self.__motor = self.__stage.motor(motor_id)

    def calibrate(self) -> None:
        sensor = self.__stage.resistor(self.__motor_id)
        while sensor.value() == 0:
            sensor = self.__stage.resistor(self.__motor_id)
        self.move(10000, wait=False)

        while not self.isFinished():
            if sensor.value() != 15000:
                self.stop()
                break
            sensor = self.__stage.resistor(self.__motor_id)
            self.__stage.updateWait()

    def move(self, distance: int = 100_000, speed: int = 512, wait: bool = True) -> None:
        speed = -speed if distance < 0 else speed
        self.__motor.setSpeed(speed)
        self.__motor.setDistance(distance)
        if wait:
            self.__stage._wait(self.__motor)

    def isFinished(self) -> bool:
        return self.__motor.finished()

    def stop(self) -> None:
        self.__motor.stop()

class Stage:
    """ Abstract class for stages. """
    def __init__(self, host: str, port: int = 65000):
        self._stage = ftrobopy.ftrobopy(host, port)
        self._isRunning = False

    def isRunning(self) -> bool:
        """ Returns True if stage is in process, otherwise False. """
        return self._isRunning

    def _wait(self, motor) -> None:
        """ Wait until motor is finished. """
        while not motor.finished():
            self._stage.updateWait()
