import time
from .stage import Stage, Cargo, Motor

class Crane(Stage):
    def calibrate(self) -> None:
        """ Calibrates all crane motors. """
        for motor_id in 1, 2, 3:
            Motor(self._stage, motor_id).calibrate()
        Motor(self._stage, 1).move(-925)

    def takeFromStorage(self) -> None:
        motor1 = self._stage.motor(1)
        motor1.setSpeed(-512)
        motor1.setDistance(475)
        self.wait(motor1)

        motor3 = self._stage.motor(3)
        motor3.setSpeed(-512)
        motor3.setDistance(200)
        self.wait(motor3)

        motor2 = self._stage.motor(2)
        motor2.setSpeed(-512)
        motor2.setDistance(190)
        self.wait(motor2)

        motor4 = self._stage.motor(4)
        motor4.setSpeed(512)
        motor4.setDistance(1024)
        out = self._stage.output(8)
        out.setLevel(512)
        self.wait(motor4)

    def takeFromPaintingCenter(self) -> None:
        ...

    def takeFromSortingCenter(self, color) -> None:
        if color == Cargo.WHITE:
            distances = (465, -855, -375)
        elif color == Cargo.RED:
            distances = (545, -855, -420)
        else:
            distances = (615, -855, -600)

        tower = Motor(self._stage, 1)
        arm_z = Motor(self._stage, 2)
        arm_x = Motor(self._stage, 3)
        generator = Motor(self._stage, 4)

        tower.move(distances[0])
        arm_x.move(distances[2])
        arm_z.move(distances[1])
        generator.move(wait=False)
        out = self._stage.output(8)
        out.setLevel(512)
        time.sleep(2)

        arm_z.move(-distances[1])
        arm_x.move(-distances[2])
        tower.move(-distances[0])

    def putInStorage(self) -> None:
        distances = (-475, -250, -195)

        tower = Motor(self._stage, 1)
        arm_z = Motor(self._stage, 2)
        arm_x = Motor(self._stage, 3)
        generator = Motor(self._stage, 4)

        tower.move(distances[0])
        arm_x.move(distances[2])
        arm_z.move(distances[1])
        generator.stop()

        arm_z.move(-distances[1])
        arm_x.move(-distances[2])
        tower.move(-distances[0])


    def putInPaintingCenter(self) -> None:
        ...
