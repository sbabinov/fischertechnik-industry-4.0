from .stage import Stage

class SortingCenter(Stage):
    def __init__(self, host: str, port: int = 65000):
        super().__init__(host, port)
        self.__whiteCount = 0
        self.__blueCount = 0
        self.__redCount = 0

    def sort(self) -> None:
      ...

    def decWhite(self) -> None:
      self.__whiteCount -= 1

    def decBlue(self) -> None:
      self.__blueCount -= 1

    def decRed(self) -> None:
      self.__redCount -= 1

    def getWhite(self) -> int:
      return self.__whiteCount

    def getBlue(self) -> int:
      return self.__blueCount

    def getRed(self) -> int:
      return self.__redCount
