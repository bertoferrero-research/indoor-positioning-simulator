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

from abc import ABC, abstractmethod
from classes.models.station import Station

class RssiInterface(ABC):
    """
    RssiInterface is an abstract base class that defines the interface for calculating RSSI (Received Signal Strength Indicator).
    """

    @abstractmethod
    def calculate_rssi(self, station: Station, current_time: int, milliseconds_per_iteration: int, current_x: float, current_y: float, speed: float) -> int:
        """
        Calculate the Received Signal Strength Indicator (RSSI) for a given station at a specific time and position.

        Args:
            station (Station): The station for which the RSSI is being calculated.
            current_time (int): The current time in the simulation.
            milliseconds_per_iteration (int): The number of milliseconds per iteration in the simulation.
            current_x (float): The current x-coordinate of the station.
            current_y (float): The current y-coordinate of the station.
            speed (float): The speed of the station.

        Returns:
            int: The calculated RSSI value.
        """
        pass