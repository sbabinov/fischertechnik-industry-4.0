from .stages import *
from .singleton import singleton

@singleton
class Factory:
    """ Class for controlling the Fischertechnik factory layout. """

    def __init__(self):
        self.storage = Storage()
        self.crane = Crane()
        self.paintCenter = PaintingCenter()
        self.shipmentCenter = ShipmentCenter()
        self.sortingCenter = SortingCenter()

    def calibrate(self) -> None:
        """ Calibrates all components. """
        ...
