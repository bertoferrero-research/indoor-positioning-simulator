from classes.simulators.rssi.interface import RssiInterface
from classes.models.station import Station
import random

class DummyRssiModule(RssiInterface):

    def calculate_rssi(self, station: Station, current_time: int, milliseconds_per_iteration: int, current_x: float, current_y: float, speed: float) -> int:
        return random.randint(-100, 0)