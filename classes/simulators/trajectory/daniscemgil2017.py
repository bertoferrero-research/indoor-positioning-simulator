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
import numpy as np
import random

class DanisCemgil2017(TrajectoryInterface):
    """
    A class to simulate the trajectory of a moving object based on the model proposed by Danis and Cemgil in 2017.

    Parameters:
        s (float): Standard deviation of the normal distribution used to randomize the angle. Default is 0.07.   
        
    Attributes:
        s (float): Standard deviation of the normal distribution used to randomize the angle. Default is 0.07.
        outbounds_ration (float): Additional value to manipulate sampled rotation values to prevent the virtual mobile device from leaving the area. Default is π/8.
         
    """

    def __init__(self, s: float = 0.07):
        # Inicialización de variables
        self.s = s                          # desviación estandar de la distribución normal usada para aleatorizar el ángulo. 0 = no hay varianza en el ángulo
        self.outbounds_ration = np.pi / 8   # To prevent our virtual mobile device from leaving the area, sampled rotation values are deliberately manipulated by an additional value of π8 according to the current orientation

    def calculate_position(self, current_time: int, milliseconds_per_iteration: int, last_angle: float, last_x: float, last_y: float, min_x: float, max_x: float, min_y: float, max_y: float, speed: float) -> tuple:
        """
        Calculate the new position and angle of a moving object based on its previous position, angle, and speed.
        Parameters:
        current_time (int): The current time in milliseconds.
        milliseconds_per_iteration (int): The time elapsed per iteration in milliseconds.
        last_angle (float): The last known angle of the object in radians.
        last_x (float): The last known x-coordinate of the object.
        last_y (float): The last known y-coordinate of the object.
        min_x (float): The minimum x-coordinate boundary.
        max_x (float): The maximum x-coordinate boundary.
        min_y (float): The minimum y-coordinate boundary.
        max_y (float): The maximum y-coordinate boundary.
        speed (float): The speed of the object in meters per second.
        Returns:
        tuple: A tuple containing the new x-coordinate, y-coordinate, and angle (in radians) of the object.
        """
        x = last_x
        y = last_y

        #Calculamos el angulo de avance               
        # Manipulación del valor de rotación para mantener al movil dentro del área
        delta_angle = 0
        if x < min_x or x > max_x or y < min_y or y > max_y:
            delta_angle = self.outbounds_ration
        else:
            # ̃δθ_t ∼ N(0, s)
            delta_angle = np.random.normal(0, self.s)

        angle = last_angle + delta_angle

        #Calculamos la distancia recorrida
        delta_l = speed * milliseconds_per_iteration / 1000 # velocidad en m/s * tiempo en segundos = distancia recorrida en metros

        #Incrementamos posiciones
        # x_t = x_(t−1) +  ̃δl_t cos(θ_(t−1) +  ̃δθ_t)
        x += delta_l * np.cos(angle)
        # y_t = y_(t−1) +  ̃δl_t sin(θ_(t−1) +  ̃δθ_t)
        y += delta_l * np.sin(angle)

        # Devolvemos
        return (x, y, angle)

