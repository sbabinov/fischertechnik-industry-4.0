import ftrobopy

class Stage:
    """ Abstract class for stages. """
    def __init__(self, host: str, port: int = 65000):
        self.__stage = ftrobopy.ftrobopy(host, port)
        self.__isRunning = False

    def isRunning(self) -> bool:
        return self.__isRunning
