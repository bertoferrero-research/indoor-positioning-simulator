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

        # Add noise to the rssi
        if station.noise_std_dev > 0:
            noise = np.random.normal(0, station.noise_std_dev)
            rssi += noise

        if rssi < -100:
            return None
            
        return round(rssi)
    
    def should_miss_package(self, station: Station, distance: float) -> bool:

        # 1 - Determine if have all the requierd params
        if station.missing_packages_probability == None:
            return False
        
        function_model = station.missing_packages_probability.get('function_model', None)
        function_params = station.missing_packages_probability.get('params', None)
        if function_model == None or function_params == None:
            return False
        
        # 2 - Calculate the probability
        if function_model == 'sigmoid':
            return self.__linear_model(station, distance, function_params)
        elif function_model == 'exponential':
            return self.__exponential_model(station, distance, function_params)
        else:
            return False

        return random.random() < station.missing_packages_probability
