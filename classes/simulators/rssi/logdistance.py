# Copyright 2024 Alberto Ferrero López
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from classes.simulators.rssi.interface import RssiInterface
from classes.models.station import Station
from classes.lib.functionmodels import functionmodels
from math import sqrt
import numpy as np
import random

class LogDistancePathLossModel(RssiInterface):
    '''
    LogDistancePathLossModel is a class that implements the RssiInterface to calculate the Received Signal Strength Indicator (RSSI) using the Log-Distance Path Loss model.
    '''

    def calculate_rssi(self, station: Station, current_time: int, milliseconds_per_iteration: int, current_x: float, current_y: float, speed: float) -> int:
        """
        Calculate the Received Signal Strength Indicator (RSSI) for a given station and current position.
        Args:
            station (Station): The station object containing transmission parameters and position.
            current_time (int): The current time in milliseconds. Not used in this model.
            milliseconds_per_iteration (int): The time interval per iteration in milliseconds. Not used in this model.
            current_x (float): The current x-coordinate of the receiver.
            current_y (float): The current y-coordinate of the receiver.
            speed (float): The speed of the receiver. Not used in this model.
        Returns:
            int: The calculated RSSI value, rounded to the nearest integer. Returns None if the package should be missed or if the RSSI is less than -100.
        Raises:
            ValueError: If the Tx or n values are not available for the station.
        """
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
        elif function_model == 'lineal':
            param_a = function_params.get('a', None)
            param_b = function_params.get('b', None)
            if param_a is None or param_b is None:
                raise ValueError("Missing parameters 'a' and 'b' for the lineal function model.")
            miss_probability = functionmodels.lineal(distance, param_a, param_b)

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
