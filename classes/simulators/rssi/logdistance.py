from classes.simulators.rssi.interface import RssiInterface
from classes.models.station import Station
from math import sqrt
import numpy as np
import random

class LogDistancePathLossModel(RssiInterface):

    def calculate_rssi(self, station: Station, current_time: int, milliseconds_per_iteration: int, current_x: float, current_y: float, speed: float) -> int:
        # Get Tx and n from station, if not available throw exception
        Tx = station.Tx
        n = station.n
        if(Tx == None or n == None):
            raise ValueError(f"Tx and n values are not available for the station with MAC {station.mac}.")

        # Calculate distance between the station and the current location
        distance = sqrt((station.x - current_x) ** 2 + (station.y - current_y) ** 2)
        
        # Calculate the rssi
        if distance != 0:
            rssi = Tx - (10 * n * np.log10(distance))
        else:
            rssi = Tx

        if rssi < -100:
            return None
            
        return round(rssi)
