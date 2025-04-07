from .stage import Stage

import time

class ShipmentCenter(Stage):
    def __init__(self, host: str):
        super().__init__(host)
        self._init_components()

    def _init_components(self):
        self.motor_stand = Motor(self, 1)

        self.polishing = self.output(3) #полировка
        self.tape = self.output(6) #лента
