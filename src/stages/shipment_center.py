import time
from .stage import Motor, Stage

class SensorCheck:
    def __init__(self):
        self.sensorCheck = False

class ShipmentCenter(Stage):
    def __init__(self, sensorCheck : SensorCheck, host: str, port: int = 65000):
        super().__init__(host, port)
        # Initialization of motors
        self.motorStand = Motor(self._stage, 1)

        # Initialization of sensors
        self.buttonCrane = self._stage.resistor(5)
        self.buttonStandPlus = self._stage.resistor(3)
        self.buttonStandDown = self._stage.resistor(2)
        self.buttonStandMinus = self._stage.resistor(1)
        self.sensorTape = self._stage.resistor(4)

        # Initialization of devices
        self.compressor = self._stage.output(8)
        self.polishing = self._stage.output(3)
        self.tape = self._stage.output(6)
        self.throwOut = self._stage.output(7)

        # Initialization of flag
        self.sensorCheck = sensorCheck

    def getCompressor(self):
        return self.compressor

    def setCompressor(self, value):
        self.compressor = value

    def getButtonCrane(self):
        return self.buttonCrane

    def setButtonCrane(self, value):
        self.buttonCrane = value

    def calibrate(self):
        self.motorStand.move(100, 300, False)
        while not self.motorStand.isFinished():
            self._stage.updateWait()
            if self.buttonStandMinus.value() != 15000:
                self.motorStand.stop()
                break

    def stand(self):
        while self.buttonCrane.value() != 15000 and self.sensorCheck.sensorCheck:

            self.motorStand.move(100, 300, False)
            while not self.motorStand.isFinished():
                self._stage.updateWait()
                if self.buttonStandMinus.value() != 15000:
                    self.motorStand.stop()
                    break

            self.motorStand.move(100, -300, False)
            while not self.motorStand.isFinished():
                self._stage.updateWait()
                if self.buttonStandDown.value() != 15000:
                    self.motorStand.stop()
                    self.polishing.setLevel(512)
                    time.sleep(3)
                    break
            self.polishing.setLevel(0)

            self.motorStand.move(100, -300, False)
            while not self.motorStand.isFinished():
                self._stage.updateWait()
                if self.buttonStandPlus.value() != 15000:
                    self.motorStand.stop()
                    self.compressor.setLevel(512)
                    self.throwOut.setLevel(512)
                    time.sleep(1)
                    break

            self.throwOut.setLevel(0)
            self.compressor.setLevel(0)
            self.tape.setLevel(512)
            while self.sensorTape.value() != 15000:
                pass
            time.sleep(2)
            self.tape.setLevel(0)
            self.calibrate()
            self.sensorCheck.sensorCheck = False

    def runShipmentCenter(self):
        self._isRunning = True
        self.stand()
        self._isRunning = False
