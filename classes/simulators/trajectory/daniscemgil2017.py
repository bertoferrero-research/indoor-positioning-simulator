from classes.simulators.trajectory.interface import TrajectoryInterface
import numpy as np
import random

class DanisCemgil2017(TrajectoryInterface):

    def __init__(self, s: float = 0.07):
        # Inicialización de variables
        self.s = s                          # desviación estandar de la distribución normal usada para aleatorizar el ángulo. 0 = no hay varianza en el ángulo
        self.outbounds_ration = np.pi / 8   # To prevent our virtual mobile device from leaving the area, sampled rotation values are deliberately manipulated by an additional value of π8 according to the current orientation

    def calculate_position(self, current_time: int, milliseconds_per_iteration: int, last_angle: float, last_x: float, last_y: float, min_x: float, max_x: float, min_y: float, max_y: float, speed: float) -> tuple:
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

