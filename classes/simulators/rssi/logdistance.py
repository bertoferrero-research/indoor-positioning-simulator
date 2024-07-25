from classes.simulators.rssi.interface import RssiInterface
from classes.models.station import Station
from classes.lib.functionmodels import functionmodels
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
        
        # Check if the package should be missed
        if self.should_miss_package(station, distance):
            return None

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
        """
        Determines whether a package should be missed based on the given station and distance.

        Args:
            station (Station): The station object representing the transmitter.
            distance (float): The distance between the transmitter and receiver.

        Returns:
            bool: True if the package should be missed, False otherwise.
        """

        # 1 - Determine if have all the required params
        if station.missing_packages_probability is None:
            return False
        
        function_model = station.missing_packages_probability.get('function_model', None)
        function_params = station.missing_packages_probability.get('params', None)
        if function_model is None or function_params is None:
            return False
        
        # 2 - Calculate the probability
        miss_probability = 0
        if function_model == 'sigmoid':
            param_a = function_params.get('a', None)
            param_b = function_params.get('b', None)
            if param_a is None or param_b is None:
                raise ValueError("Missing parameters 'a' and 'b' for the sigmoid function model.")
            miss_probability = functionmodels.sigmoid(distance, param_a, param_b)
        elif function_model == 'exponential':
            param_a = function_params.get('a', None)
            param_b = function_params.get('b', None)
            if param_a is None or param_b is None:
                raise ValueError("Missing parameters 'a' and 'b' for the exponential function model.")
            miss_probability = functionmodels.exponential(distance, param_a, param_b)
        else:
            return False
        
        # Limit probability to 0-100
        miss_probability = miss_probability * 100
        miss_probability = max(0, min(100, miss_probability))

        # 3 - Determine if the package should be missed
        if miss_probability == 0:
            return False
        elif miss_probability == 100:
            return True
        
        random_number = random.randint(0, 100)
        return random_number <= miss_probability
