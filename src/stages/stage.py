import ftrobopy

class Cargo:
    WHITE = 1
    BLUE = 2
    RED = 3
    UNDEFINED = 4
    EMPTY = 5

class Motor:
    def __init__(self, stage, motor_id):
        self.__stage = stage
        self.__motor_id = motor_id
        self.motor = self.__stage.motor(motor_id)

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

    def move(self, distance: int = 30000, speed: int = 512, wait: bool = True) -> None:
        speed = -speed if distance < 0 else speed
        self.motor.setDistance(abs(distance))
        self.motor.setSpeed(speed)
        if wait:
            self.wait()

    def isFinished(self) -> bool:
        return self.motor.finished()

    def stop(self) -> None:
        self.motor.setSpeed(0)
        self.motor.stop()
        self.motor.setDistance(0)

    def wait(self) -> None:
        while not self.motor.finished():
            self.__stage.updateWait()

class SensorCheck:
    def __init__(self):
        self.sensorCheck = None

def resetConfigCounter(f):
    def wrapper(*args):
        args[0]._stage._config_id[0] = 0
        args[0]._stage._config_id[1] = 0
        return f(*args)
    return wrapper

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


