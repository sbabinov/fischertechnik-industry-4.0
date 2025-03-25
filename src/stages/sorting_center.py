from .stage import Stage

class SortingCenter(Stage):
    def __init__(self, host: str, port: int = 65000):
        super().__init__(host, port)
        self.__whiteCount = 0
        self.__blueCount = 0
        self.__redCount = 0

    def sort(self) -> None:
      """ Determine the color of the cargo and sort it """
      sensorIn = self._stage.output(1)
      sensorOut = self._stage.output(2)
      colorSensor = self._stage.output(3)

      while sensorIn == 1000:
        pass

      conveyor = self._stage.motor(1)
      conveyor.setSpeed(-512)
      conveyor.setDistance(1000)

      minColorValue = 2000
      while sensorOut == 1000:
        minColorValue = min(minColorValue, colorSensor)

      compressor = self._stage.motor(4)
      compressor.setSpeed(-512)
      compressor.setDistance(1000)

      if minColorValue > 1600:
        ...
        self.__blueCount += 1
      elif minColorValue > 1200:
        ...
        self.__redCount += 1
      else:
        ...
        self.__whiteCount += 1

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
