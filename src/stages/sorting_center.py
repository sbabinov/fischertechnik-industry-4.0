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
      ...

    def decBlue(self) -> None:
      ...

    def decRed(self) -> None:
      ...

    def getWhite(self) -> int:
      ...

    def getBlue(self) -> int:
      ...

    def getRed(self) -> int:
      ...
