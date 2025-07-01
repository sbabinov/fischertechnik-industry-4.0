from .stage import Stage
import time

class SortingCenter(Stage):
    def __init__(self, host: str, port: int = 65000):
        super().__init__(host, port)
        self.__white_count = 0
        self.__blue_count = 0
        self.__red_count = 0

    def sort(self) -> None:
        """ Determine the color of the cargo and sort it. """
        sensorIn = self._stage.resistor(1)
        sensorOut = self._stage.resistor(3)
        colorSensor = self._stage.colorsensor(2)

        while sensorIn.value() < 1000:
            pass

        conveyor = self._stage.motor(1)
        conveyor.setSpeed(-512)
        conveyor.setDistance(1000)

        minColorValue = 2000
        while sensorOut.value() < 5000:
            minColorValue = min(minColorValue, colorSensor.value())

        out = self._stage.output(5)

        if minColorValue > 1400:
            out = self._stage.output(6)
            conveyor.setDistance(8)
            self.__blue_count += 1
        elif minColorValue > 1000:
            out = self._stage.output(5)
            conveyor.setDistance(13)
            self.__red_count += 1
        else:
            out = self._stage.output(4)
            conveyor.setDistance(3)
            self.__white_count += 1

        self._wait(conveyor)

        compressor = self._stage.motor(4)
        compressor.setSpeed(-512)
        compressor.setDistance(1000)

        out.setLevel(512)
        time.sleep(0.25)
        out.setLevel(0)
        compressor.stop()

    def dec_white(self) -> None:
        """ Reduce the number of white goods. """
        self.__white_count -= 1

    def dec_blue(self) -> None:
        """ Reduce the number of blue goods. """
        self.__blue_count -= 1

    def dec_red(self) -> None:
        """ Reduce the number of red goods. """
        self.__red_count -= 1

    def get_white(self) -> int:
        """ Return the number of white goods. """
        return self.__white_count

    def get_blue(self) -> int:
        """ Return the number of blue goods. """
        return self.__blue_count

    def get_red(self) -> int:
        """ Return the number of red goods. """
        return self.__red_count
