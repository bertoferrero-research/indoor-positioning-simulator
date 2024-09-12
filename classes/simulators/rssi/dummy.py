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
import random

class DummyRssiModule(RssiInterface):
    """
    DummyRssiModule is a class that implements the RssiInterface to simulate RSSI (Received Signal Strength Indicator) values.
    """

    def calculate_rssi(self, station: Station, current_time: int, milliseconds_per_iteration: int, current_x: float, current_y: float, speed: float) -> int:
        """
        Returns a random value between -100 and 0 as RSSI value.

        Args:
            station (Station): The station for which the RSSI is being calculated.
            current_time (int): The current time in milliseconds.
            milliseconds_per_iteration (int): The number of milliseconds per iteration.
            current_x (float): The current x-coordinate of the station.
            current_y (float): The current y-coordinate of the station.
            speed (float): The speed of the station.

        Returns:
            int: The calculated RSSI value, ranging from -100 to 0.
        """
        return random.randint(-100, 0)