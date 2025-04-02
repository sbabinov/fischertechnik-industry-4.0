from .stages import *
from .singleton import singleton

@singleton
class Factory:
    """ Class for controlling the Fischertechnik factory layout. """

    def __init__(self):
        self.storage = Storage('')
        self.crane = Crane('')
        self.paintingCenter = PaintingCenter('')
        self.shipmentCenter = ShipmentCenter('')
        self.sortingCenter = SortingCenter('')

    def calibrate(self) -> None:
        """ Calibrates all components. """
        ...

    def sort(self) -> None:
        """ Sort storage cargo. """
        ...

    def unsort(self) -> None:
        """ Unsort storage cargo. """
        ...

    def getStorage(self, row, column) -> str:
        """ Get information about cargo in storage cell:
            empty - cell is empty;
            unknown - cargo inside, but color is undefined;
            white, blue, red - cargo of this color inside. """
        ...