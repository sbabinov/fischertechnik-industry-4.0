import time
from .stage import Stage, Cargo, Motor

class Crane(Stage):
    def calibrate(self) -> None:
        """ Calibrates all crane motors. """
        for motor_id in 1, 2, 3:
            Motor(self._stage, motor_id).calibrate()
        Motor(self._stage, 1).move(-925)

    def takeFromStorage(self) -> None:
        """ The crane takes a cargo from the storage and returns to the calibrated position. """
        distances = (-475, -250, -195)

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

    def takeFromSortingCenter(self, color) -> None:
        """ The crane takes a cargo from the sorting center and returns to the calibrated position. """
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
        """ The crane puts a cargo in the storage and returns to the calibrated position. """
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
        """ The crane puts a cargo in the painting center and returns to the calibrated position. """
        distances = (5, -600, -835)

        tower = Motor(self._stage, 1)
        arm_z = Motor(self._stage, 2)
        arm_x = Motor(self._stage, 3)
        generator = Motor(self._stage, 4)

        tower.move(distances[0])
        arm_x.move(distances[2])
        arm_z.move(distances[1])
        generator.stop()

        arm_z.move(distances[1])
        arm_x.move(distances[2])
        tower.move(distances[0])
