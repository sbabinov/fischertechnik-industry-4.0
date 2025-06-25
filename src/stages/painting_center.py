import time
from .stage import Motor, Stage
from .shipment_center import ShipmentCenter

class PaintingCenter(Stage):
    def __init__(self, shipmentCenter: ShipmentCenter, host: str, port: int = 65000):
        super().__init__(host, port)
        # Initialization of motors
        self.motorPainting = Motor(self._stage, 1)
        self.motorCrane = Motor(self._stage, 2)

        # Initialization of sensors
        self.shipment = shipmentCenter
        self.buttonCrane = self.shipment.getButtonCrane()
        self.buttonPainting = self._stage.resistor(1)
        self.buttonPaintingDown = self._stage.resistor(2)
        self.sensorOut = self._stage.resistor(5)
        self.buttonCranePainting = self._stage.resistor(3)

        # Initialization of devices
        self.compressor = self.shipment.getCompressor()
        self.gate = self._stage.output(7)
        self.lighting = self._stage.output(8)
        self.pump = self._stage.output(5)
        self.outUp = self._stage.output(6)

    def painting(self):
        while self.sensorOut.value() != 15000:
            pass

        time.sleep(3)
        self.gate.setLevel(512)
        self.compressor.setLevel(512)
        self.motorPainting.move(50, -512, False)
        while not self.motorPainting.isFinished():
            self._stage.updateWait()
            if self.buttonPainting.value() != 15000:
                self.gate.setLevel(0)
                self.motorPainting.stop()
                self.lighting.setLevel(512)
                break

        self.motorCrane.move(100, -512, False)
        time.sleep(3)
        self.gate.setLevel(512)
        self.lighting.setLevel(0)
        self.motorPainting.move(100, 512, False)
        while not self.motorPainting.isFinished():
            self._stage.updateWait()
            if self.buttonPaintingDown.value() != 15000:
                self.motorPainting.stop()
                self.gate.setLevel(0)
                break

        while not self.motorCrane.isFinished():
            self._stage.updateWait()
            if self.buttonCranePainting.value() != 15000:
                self.motorCrane.stop()
                break

    def _calibrateCrane(self):
        self.motorCrane.move(100, 512, False)
        while not self.motorCrane.isFinished():
            self._stage.updateWait()
            if self.buttonCrane.value() != 15000:
                self.motorCrane.stop()
                break

    def _calibratePainting(self):
        self.gate.setLevel(512)
        self.compressor.setLevel(512)
        self.motorPainting.move(100, -512, False)
        while not self.motorPainting.isFinished():
            self._stage.updateWait()
            if self.buttonPainting.value() != 15000:
                self.gate.setLevel(0)
                self.motorPainting.stop()
                break

        self.motorPainting.stop()
        self.gate.setLevel(512)
        self.motorPainting.move(1, 512, False)
        while not self.motorPainting.isFinished():
            self._stage.updateWait()
            if self.buttonPaintingDown.value() != 15000:
                self.motorPainting.stop()
                self.gate.setLevel(0)
                self.compressor.setLevel(0)
                break

    def calibrate(self):
        self._calibrateCrane()
        self._calibratePainting()

    def goFromPainting(self):
        self.motorCrane.move(100, 512, False)
        while not self.motorCrane.isFinished():
            self._stage.updateWait()
            if self.buttonCrane.value() != 15000:
                self.motorCrane.stop()
                self.outUp.setLevel(512)
                self.compressor.setLevel(512)
                time.sleep(1.5)
                self.pump.setLevel(0)
                time.sleep(0.5)
                self.outUp.setLevel(0)
                self.compressor.setLevel(0)
                break

    def runCrane(self):
        self.suckItUp()
        self.goFromPainting()

    def suckItUp(self):
        self.outUp.setLevel(512)
        self.compressor.setLevel(512)
        time.sleep(1)
        self.pump.setLevel(512)
        time.sleep(1.5)
        self.outUp.setLevel(0)

    def run(self):
        self._isRunning = True
        self.painting()
        self.runCrane()
        self._isRunning = False