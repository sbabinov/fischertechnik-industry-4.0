import ftrobopy

class Stage:
    """ Abstract class for stages. """
    def __init__(self, host: str, port: int = 65000):
        self._stage = ftrobopy.ftrobopy(host, port)
        self._isRunning = False

    def isRunning(self) -> bool:
        """ Returns True if stage is in process, otherwise False. """
        return self._isRunning

    def wait(self, motor) -> None:
        """ Wait until motor is finished. """
        while not motor.finished():
            self._stage.updateWait()
