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

class TrajectoryInterface(ABC):
    """
    An abstract base class for trajectory interfaces.

    This class defines the interface for calculating the position of an object
    based on various parameters.
    """

    @abstractmethod
    def calculate_position(self, current_time: int, milliseconds_per_iteration: int, last_angle: float, last_x: float, last_y: float, min_x: float, max_x: float, min_y: float, max_y: float, speed: float) -> tuple:
        """
        Calculates the position of the object based on the given parameters.

        Args:
            current_time (int): The current time in milliseconds.
            milliseconds_per_iteration (int): The number of milliseconds per iteration.
            last_angle (float): The last recorded angle of the object [0, 2pi].
            last_x (float): The last recorded x-coordinate of the object.
            last_y (float): The last recorded y-coordinate of the object.
            min_x (float): The minimum x-coordinate value.
            max_x (float): The maximum x-coordinate value.
            min_y (float): The minimum y-coordinate value.
            max_y (float): The maximum y-coordinate value.
            speed (float): The speed of the object defined in meters per second.

        Returns:
            tuple: A tuple containing the calculated x and y coordinates of the object.
        """
        pass