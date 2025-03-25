from .stage import Stage

class SortingCenter(Stage):
    def __init__(self, host: str, port: int = 65000):
        super().__init__(host, port)
        self.__whiteCount = 0
        self.__blueCount = 0
        self.__redCount = 0

    def sort(self) -> None:
      """ Determine the color of the cargo and sort it """
      ...

    def decWhite(self) -> None:
      """ Reduce the number of white goods """
      self.__whiteCount -= 1

    def decBlue(self) -> None:
      """ Reduce the number of blue goods """
      self.__blueCount -= 1

    def decRed(self) -> None:
      """ Reduce the number of red goods """
      self.__redCount -= 1

    def getWhite(self) -> int:
      """ Return the number of white goods """
      return self.__whiteCount

    def getBlue(self) -> int:
      """ Return the number of blue goods """
      return self.__blueCount

    def getRed(self) -> int:
      """ Return the number of red goods """
      return self.__redCount
