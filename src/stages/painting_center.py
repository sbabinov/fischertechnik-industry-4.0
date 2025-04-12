import time
import ftrobopy
from .stage import Motor, Stage
from shipment_center import ShipmentCenter

class SensorCheck():
    def __init__(self):
        self.sensorCheck = None

class PaintingCenter:
    def __init__(self, host: str, port: int = 65000):
        super().__init__(host, port)
        # Initialization of motors
        self.motorPainting = Motor(self._stage, 1)
        self.motorCrane = Motor(self._stage, 2)

        # Initialization of sensors
        self.buttonCrane = ShipmentCenter.buttonCrane
        self.buttonPainting = self._stage.resistor(1)
        self.sensorOut = self._stage.resistor(5)

        # Initialization of devices
        self.compressor = ShipmentCenter.compressor
        self.gate = self._stage.output(7)
        self.lighting = self._stage.output(8)
        self.pump = self._stage.output(5)
        self.outUp = self._stage.output(6)

    def painting(self):
        while self.sensorOut.value() != 15000:
            pass

        SensorCheck.sensorCheck = True
        time.sleep(3)
        self.gate.setLevel(512)
        self.compressor.setLevel(512)
        self.motorPainting.move(50, -300, False)
        while not self.motorPainting.finished():
            self._stage.updateWait()
            if self.buttonPainting.value() != 15000:
                self.gate.setLevel(0)
                self.motorPainting.stop()
                self.lighting.setLevel(512)
                break

        time.sleep(3)
        self.gate.setLevel(512)
        self.motorPainting.move(100, 300, False)
        time.sleep(4)
        self.motorPainting.stop()

        while not self.motorPainting.finished():
            self.lighting.setLevel(0)
            self.gate.setLevel(0)
            self._stage.updateWait()

    def goToPainting(self):
        self.motorCrane.move(100, -512, True)
        time.sleep(23)
        self.motorCrane.stop()

    def goFromPainting(self):
        self.goToPainting()
        self.suckItUp()

        self.motorCrane.move(100, 512, False)
        while not self.motorCrane.finished():
            self._stage.updateWait()
            if self.buttonCrane.value() != 15000:
                self.motorCrane.stop()
                self.outUp.setLevel(512)
                self.compressor.setLevel(512)
                time.sleep(1)
                self.outUp.setLevel(0)
                time.sleep(0.5)
                self.pump.setLevel(0)
                self.compressor.setLevel(0)
                break

    def suckItUp(self):
        self.outUp.setLevel(512)
        self.compressor.setLevel(512)
        time.sleep(1)
        self.pump.setLevel(512)
        time.sleep(0.5)
        self.outUp.setLevel(0)