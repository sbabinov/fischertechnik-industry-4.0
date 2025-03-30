from .stage import Stage

import ftrobopy

def reset_sensors():
    for i in range(1, 10):
        iteration = list()
        for i in range (1, 9):
            sensor = txt.resistor(i)
            iteration.append(sensor.value())

def should_horizont_backward_stop():
    sensor_backward = txt.resistor(6)
    if sensor_backward.value() != 15000:
        return True

def should_horizont_forward_stop():
    sensor_forward = txt.resistor(7)
    if sensor_forward.value() != 15000:
        return True

def should_vertical_stop():
    sensor = txt.resistor(8)
    if sensor.value() != 15000:
        return True

def should_rail_stop():
    sensor = txt.resistor(5)
    if sensor.value() != 15000:
        return True

txt = ftrobopy.ftrobopy('192.168.4.76')

reset_sensors()

horizont_speed = 512
horizont_motor = txt.motor(3)
horizont_motor.setSpeed(horizont_speed)
horizont_motor.setDistance(1)

while not should_horizont_backward_stop():
    pass

horizont_motor.stop()

vertical_speed = 400
vertical_motor = txt.motor(0)
vertical_motor.setSpeed(vertical_speed)
vertical_motor.setDistance(2000)

rail_speed = 400
rail_motor = txt.motor(2)
rail_motor.setSpeed(rail_speed)
rail_motor.setDistance(20000)

is_calibrated = False

while not is_calibrated:
    cond_first = should_vertical_stop()
    cond_second = should_rail_stop()
    if cond_first:
        vertical_motor.stop()
    if cond_second:
        rail_motor.stop()
    is_calibrated = cond_first and cond_second

txt = ftrobopy.ftrobopy('192.168.4.76')

reset_sensors()

speed = -512
motor = txt.motor(2)
motor.setSpeed(speed)
motor.setDistance(780)
while not motor.finished():
    txt.updateWait()
vert_motor = txt.motor(0)
vert_motor.setSpeed(-512)
vert_motor.setDistance(100)
while not vert_motor.finished():
    txt.updateWait()

horiz_motor = txt.motor(3)
horiz_motor.setSpeed(-200)
horiz_motor.setDistance(1)
while not should_horizont_forward_stop():
    pass

class Storage(Stage):
    ...
