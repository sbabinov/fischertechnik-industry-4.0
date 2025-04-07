from .stages import *
from stages.stage import Cargo
from .singleton import singleton
import threading

@singleton
class Factory:
    """ Class for controlling the Fischertechnik factory layout. """

    def __init__(self):
        self.__storage = Storage('')
        self.__crane = Crane('')
        self.__paintingCenter = PaintingCenter('')
        self.__shipmentCenter = ShipmentCenter('')
        self.__sortingCenter = SortingCenter('')
        self.__storageLock = threading.Lock()
        self.__craneLock = threading.Lock()

    def calibrate(self) -> None:
        """ Calibrates all components. """
        self.__storage.calibrate()
        self.__crane.calibrate()
        self.__paintingCenter.calibrate()
        self.__shipmentCenter.calibrate()

    def sort(self) -> None:
        """ Sort storage cargo. """
        ...

    def getStorage(self, row, column) -> Cargo:
        """ Get information about cargo in storage cell:
            EMPTY - cell is empty;
            UNDEFINED - cargo inside, but color is undefined;
            WHITE, BLUE, RED - cargo of this color inside. """
        return self.__storage.getData()[row][column]