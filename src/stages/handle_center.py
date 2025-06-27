from .stage import Stage
import time


class ShipmentCenter(Stage):
    def __init__(self, id: str, port: int = 65000):
        super().__init__(id, port)
        self.__motorStand = self._stage.motor(1)

        # Initialization of sensors
        self.__buttonCrane = self._stage.resistor(5)
        self.__buttonStandPlus = self._stage.resistor(3)
        self.__buttonStandDown = self._stage.resistor(2)
        self.__buttonStandMinus = self._stage.resistor(1)
        self.__sensorTape = self._stage.resistor(4)

        # Initialization of devices
        self.__compressor = self._stage.output(8)
        self.__polishing = self._stage.output(3)
        self.__tape = self._stage.output(6)
        self.__throwOut = self._stage.output(7)

    def __rotate_forward(self):
        self.__motorStand.setDistance(100)
        self.__motorStand.setSpeed(300)
        while not self.__motorStand.finished() and self.__buttonStandMinus.value() == 15000:
            pass
        self.__motorStand.stop()

    def __rotate_backward(self):
        self.__motorStand.setDistance(100)
        self.__motorStand.setSpeed(-300)
        while not self.__motorStand.finished() and self.__buttonStandPlus.value() == 15000:
            pass
        self.__motorStand.stop()

    def calibrate(self):
        self.__rotate_forward()

    def stand(self):
        self.__rotate_forward()
        self.__rotate_backward()
        self.__polishing.setLevel(512)
        time.sleep(3)
        self.__polishing.setLevel(0)

        self.__rotate_backward()
        self.__compressor.setLevel(512)
        self.__throwOut.setLevel(512)

        time.sleep(0.5)

        self.__throwOut.setLevel(0)
        self.__compressor.setLevel(0)
        self.__rotate_forward()
        self.__tape.setLevel(512)
        while self.__sensorTape.value() != 15000:
            pass
        time.sleep(2)
        self.__tape.setLevel(0)

    def get_compressor(self):
        return self.__compressor

    def get_button(self):
        return self.__buttonCrane


class PaintingCenter(Stage):
    def __init__(self, ship, ip: str, port: int = 65000):
        super().__init__(ip, port)
        self.__shipment = ship
        self.__motorPainting = self._stage.motor(1)
        self.__motorCrane = self._stage.motor(2)

        self.__buttonPaintingUp = self._stage.resistor(1)
        self.__buttonPaintingDown = self._stage.resistor(2)
        self.__sensorOut = self._stage.resistor(5)
        self.__buttonCranePainting = self._stage.resistor(3)

        # Initialization of devices
        self.__compressor = self.__shipment.get_compressor()
        self.__gate = self._stage.output(7)
        self.__lighting = self._stage.output(8)
        self.__pump = self._stage.output(5)
        self.__outUp = self._stage.output(6)

    def __shift_backward(self):
        self.__motorPainting.setDistance(50)
        self.__motorPainting.setSpeed(-512)
        while self.__buttonPaintingUp.value() == 15000:
            pass
        self.__motorPainting.stop()

    def __shift_forward(self):
        self.__motorPainting.setDistance(50)
        self.__motorPainting.setSpeed(512)
        while self.__buttonPaintingDown.value() == 15000:
            pass
        self.__motorPainting.stop()

    def __slide_crane_near(self):
        self.__motorCrane.setDistance(100)
        self.__motorCrane.setSpeed(-512)
        while not self.__motorCrane.finished() and self.__buttonCranePainting.value() == 15000:
            pass
        self.__motorCrane.stop()

    def __slide_crane_furth(self):
        self.__motorCrane.setDistance(100)
        self.__motorCrane.setSpeed(512)
        button = self.__shipment.get_button()
        while not self.__motorCrane.finished() and button.value() == 15000:
            pass
        self.__motorCrane.stop()

    def __gate_open(self):
        self.__compressor.setLevel(512)
        self.__gate.setLevel(512)

    def __gate_close(self):
        self.__gate.setLevel(0)
        self.__compressor.setLevel(0)

    def paint(self):
        self.__gate_open()
        self.__shift_backward()
        self.__lighting.setLevel(512)

        self.__slide_crane_near()
        time.sleep(3)
        self.__lighting.setLevel(0)
        self.__shift_forward()
        self.__gate_close()


    def __calibratePainting(self):
        self.__gate_open()
        self.__motorPainting.move(100, -512, False)
        self.__shift_backward()
        self.__gate.setLevel(0)

        self.__gate.setLevel(512)
        self.__shift_forward()
        self.__gate_close()

    def calibrate(self):
        self.__slide_crane_furth()
        self.__gate_open()
        self.__shift_backward()
        self.__shift_forward()
        self.__gate_close()

    def deliver(self):
        self.__pick_up()
        self.__slide_crane_furth()
        self.__put_down()

    def __pick_up(self):
        self.__outUp.setLevel(512)
        self.__compressor.setLevel(512)
        time.sleep(1)
        self.__pump.setLevel(512)
        time.sleep(1.5)
        self.__outUp.setLevel(0)

    def __put_down(self):
        self.__outUp.setLevel(512)
        self.__compressor.setLevel(512)
        time.sleep(1.5)
        self.__pump.setLevel(0)
        time.sleep(0.5)
        self.__outUp.setLevel(0)
        self.__compressor.setLevel(0)


class HandleCenter():
    def __init__(self, ship_ip: str, paint_ip: str):
        self.__shipment = ShipmentCenter(ship_ip)
        self.__painting = PaintingCenter(self.__shipment, paint_ip)

    def calibrate(self):
        self.__shipment.calibrate()
        self.__painting.calibrate()

    def process(self):
        self.__painting.paint()
        self.__painting.deliver()
        self.__shipment.stand()