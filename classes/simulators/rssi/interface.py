from abc import ABC, abstractmethod
from classes.station import Station

class RssiInterface(ABC):

    @abstractmethod
    def calculate_rssi(self, station: Station, current_time: int, milliseconds_per_iteration: int, current_x: float, current_y: float, speed: float) -> int:
        pass