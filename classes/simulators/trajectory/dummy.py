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

from classes.simulators.trajectory.interface import TrajectoryInterface
import random

class DummyPositionModule(TrajectoryInterface):
    """
    DummyPositionModule is a class that simulates the calculation of a random position within specified bounds.
    """
    
    def calculate_position(self, current_time: int, milliseconds_per_iteration: int, last_angle: float, last_x: float, last_y: float, min_x: float, max_x: float, min_y: float, max_y: float, speed: float) -> tuple:
        """
        Calculate a random position within the specified bounds.

        Args:
            current_time (int): The current time in milliseconds.
            milliseconds_per_iteration (int): The number of milliseconds per iteration.
            last_angle (float): The last angle of movement.
            last_x (float): The last x-coordinate.
            last_y (float): The last y-coordinate.
            min_x (float): The minimum x-coordinate boundary.
            max_x (float): The maximum x-coordinate boundary.
            min_y (float): The minimum y-coordinate boundary.
            max_y (float): The maximum y-coordinate boundary.
            speed (float): The speed of movement.

        Returns:
            tuple: A tuple containing the new x and y coordinates.
        """
        return (random.uniform(min_x, max_x), random.uniform(min_y, max_y))