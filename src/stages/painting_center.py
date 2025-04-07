import time
from .stage import Motor, Stage

class PaintingCenter(Stage):
    def __init__(self, host1: str, host2: str):
        super().__init__(host1)
        self.txt2 = ftrobopy.ftrobopy(host2)
        self._init_components()

    def _init_components(self):
        # Моторы
        self.motor_paint = Motor(self, 1)
        self.motor_crane = Motor(self, 2)

        # Сенсоры
        self.button_in = self.resistor(1) #Кнопка внутри
        self.sensor_out = self.resistor(5) #Сенсор
        self.button_crane = self.txt2.resistor(5)  #Кнопка крана

        # Выходы
        self.out_compressor = self.txt2.output(8)  # компрессор
        self.out_gates = self.output(7)  # ворота
        self.out_light = self.output(8)  # лампочка
        self.out_pump = self.output(5)  # насос
        self.out_tape = self.txt2.output(6)  # лента

    def show_sensors(self):
        try:
            while True:
                sensor_values = [self.resistor(i).value() for i in range(1, 9)]
                print(sensor_values)
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Sensor monitoring stopped")

    def painting_process(self):
        # Ожидание появления детали
        while self.sensor_out.value() != 15000:
            self.updateWait()

        time.sleep(3)

        # Начало процесса покраски
        self.out_gates.setLevel(512)
        self.out_compressor.setLevel(512)
        self.motor_paint.move(-50, speed=300, wait=False)

        # Мониторинг процесса покраски
        while not self.motor_paint.isFinished():
            self.updateWait()
            if self.button_in.value() != 15000:
                self.out_gates.setLevel(0)
                self.motor_paint.stop()
                self.out_light.setLevel(512)
                break

        time.sleep(3)

        # Завершающая фаза
        self.out_gates.setLevel(512)
        self.motor_paint.move(100, speed=300)
        time.sleep(4)
        self.motor_paint.stop()

        # Выключение всех компонентов
        while not self.motor_paint.isFinished(): #а нужен ли он?
            self.out_light.setLevel(0)
            self.out_gates.setLevel(0)
            self.updateWait()

    def transfer_process(self):
        # Первая фаза движения крана
        self.motor_crane.move(100, speed=512, wait=False)

        while not self.motor_crane.isFinished():
            self.updateWait()
            if self.button_crane.value() != 15000:
                self.motor_crane.stop()
                break

        # Ожидание детали
        while self.sensor_out.value() != 15000:
            pass

        # Возврат крана
        self.motor_crane.move(-100, speed=512)
        time.sleep(20.5)
        self.motor_crane.stop()
        time.sleep(1)

        # Активация подъемника и насосов
        out_up = self.output(6)
        self.out_compressor.setLevel(512)
        self.out_pump.setLevel(512)
        time.sleep(2)
        out_up.setLevel(512)
        time.sleep(10)
        #Поднимает фишку и ждет