from xmlrpc.client import boolean
import ftrobopy
import time


class PaintingCenter:
    def __init__(self):
        # Инициализация подключений к TXT
        self.txt1 = ftrobopy.ftrobopy('192.168.137.77')
        self.txt2 = ftrobopy.ftrobopy('192.168.137.201')

        # Инициализация моторов для txt1
        self.motorPainting = self.txt1.motor(1)
        self.motorCrane = self.txt1.motor(2)

        self.buttonPainting = self.txt1.resistor(1)
        self.sensorOut = self.txt1.resistor(5)

        self.gate = self.txt1.output(7)
        self.lighting = self.txt1.output(8)
        self.pump = self.txt1.output(5)
        self.outUp = self.txt1.output(6)

        self.buttonCrane = self.txt2.resistor(5) #сделать get
        self.compressor = self.txt2.output(8)

        self.sensorStandPlus = self.txt2.resistor(3)
        self.sensorStandDown = self.txt2.resistor(2)
        self.sensorStandMinus = self.txt2.resistor(1)
        self.sensorTape = self.txt2.resistor(4)
        self.motorStand = self.txt2.motor(1)
        self.polishing = self.txt2.output(3)
        self.tape = self.txt2.output(6)
        self.throwOut = self.txt2.output(7)

        self.flag = None

    def goToPainting(self):
        self.motorCrane.setSpeed(-512)
        self.motorCrane.setDistance(100)
        time.sleep(23)
        self.motorCrane.stop()

    def painting(self):
        while self.sensorOut.value() != 15000:
            pass

        self.flag = True
        time.sleep(3)
        self.gate.setLevel(512)
        self.compressor.setLevel(512)
        self.motorPainting.setSpeed(-300)
        self.motorPainting.setDistance(50)

        while not self.motorPainting.finished():
            self.txt1.updateWait()
            if self.buttonPainting.value() != 15000:
                self.gate.setLevel(0)
                self.motorPainting.stop()
                self.lighting.setLevel(512)
                break

        time.sleep(3)
        self.gate.setLevel(512)
        self.motorPainting.setSpeed(300)
        self.motorPainting.setDistance(100)
        time.sleep(4)
        self.motorPainting.stop()

        while not self.motorPainting.finished():
            self.lighting.setLevel(0)
            self.gate.setLevel(0)
            self.txt1.updateWait()

    def perem(self):
        self.goToPainting()
        self.sosat()

        self.motorCrane.setSpeed(512)
        self.motorCrane.setDistance(100)
        while not self.motorCrane.finished():
            self.txt1.updateWait()
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

    def calibrate(self):
        self.motorStand.setDistance(100)
        self.motorStand.setSpeed(300)
        while not self.motorStand.finished():
            self.txt2.updateWait()
            if self.sensorStandMinus.value() != 15000:
                print("ALAAARM")
                self.motorStand.stop()
                break

    def stand(self):  # - по часовой, + против
        while self.buttonCrane.value() != 15000 and self.flag:
            self.motorStand.setDistance(100)
            self.motorStand.setSpeed(300)
            while not self.motorStand.finished():
                self.txt2.updateWait()
                if self.sensorStandMinus.value() != 15000:
                    self.motorStand.stop()
                    break

            self.motorStand.setDistance(100)
            self.motorStand.setSpeed(-300)
            while not self.motorStand.finished():
                self.txt2.updateWait()
                if self.sensorStandDown.value() != 15000:
                    self.motorStand.stop()
                    self.polishing.setLevel(512)
                    time.sleep(3)
                    break

            self.polishing.setLevel(0)
            self.motorStand.setDistance(100)
            self.motorStand.setSpeed(-300)
            while not self.motorStand.finished():
                self.txt2.updateWait()
                if self.sensorStandPlus.value() != 15000:
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
            self.flag = False

    def run(self):
        while True:
            self.painting()
            self.perem()
            time.sleep(2)
            self.stand()

pc = PaintingCenter()
pc.run()