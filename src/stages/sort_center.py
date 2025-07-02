from .stage import Stage, Cargo
import time

class SortCenter(Stage):
    def __init__(self, host: str, port: int = 65000):
        super().__init__(host, port)
        self.__colors_count = [0, 0, 0]

    def sort(self) -> None:
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
            self.__colors_count[1] += 1
        elif minColorValue > 1000:
            out = self._stage.output(5)
            conveyor.setDistance(13)
            self.__colors_count[2] += 1
        else:
            out = self._stage.output(4)
            conveyor.setDistance(3)
            self.__colors_count[0] += 1

        self._wait(conveyor)

        compressor = self._stage.motor(4)
        compressor.setSpeed(-512)
        compressor.setDistance(1000)

        out.setLevel(512)
        time.sleep(0.25)
        out.setLevel(0)
        compressor.stop()

    def dec_color_count(self, cargo: Cargo) -> None:
        if cargo == Cargo.WHITE:
            self.__colors_count[0] -= 1
        elif cargo == Cargo.BLUE:
            self.__colors_count[1] -= 1
        else:
            self.__colors_count[2] -= 1

    def get_color_count(self, cargo: Cargo) -> int:
        if cargo == Cargo.WHITE:
            return self.__colors_count[0]
        elif cargo == Cargo.BLUE:
            return self.__colors_count[1]
        else:
            return self.__colors_count[2]
