from classes.simulators.trajectory.interface import TrajectoryInterface
import numpy as np
import random

class DanisCemgil2017Custom(TrajectoryInterface):
    '''
    Clase que implementa el modelo de trayectoria de Danis Cemgil 2017
    This variation retains the path angle for a random time between 1 and 5 seconds before changing it. This is done to simulate a less chaotic movement pattern.
    '''
    def __init__(self):
        # Inicialización de variables
        self.s = 1                          # desviación estandar de la distribución normal usada para aleatorizar el ángulo. 0 = no hay varianza en el ángulo
        self.outbounds_ration = np.pi / 8   # Giro forzado para mantener al robot dentro del área. To prevent our virtual robot from leaving the area, sampled rotation values are deliberately manipulated by an additional value of π8 according to the current orientation
        self._action = 1 # Acción actual. 0 = mantener el ángulo, 1 = cambiar el ángulo
        self._next_action_time = self.get_random_next_action_time() # Tiempo de la siguiente acción

    def get_random_next_action_time(self) -> int:
        if self._action == 0: #Andando recto simulamos un tiempo mayor
            return random.randint(2000, 5000)
        else: #Cambiando de dirección simulamos un tiempo menor
            return random.randint(100, 1000)

    def calculate_position(self, current_time: int, milliseconds_per_iteration: int, last_angle: float, last_x: float, last_y: float, min_x: float, max_x: float, min_y: float, max_y: float, speed: float) -> tuple:
        x = last_x
        y = last_y

        # Determinamos la acción
        if current_time > self._next_action_time:
            self._action = 1 - self._action
            self._next_action_time = current_time + self.get_random_next_action_time()

        #Calculamos el angulo de avance               
        # Manipulación del valor de rotación para mantener al robot dentro del área
        delta_angle = 0
        if x < min_x or x > max_x or y < min_y or y > max_y:
            delta_angle = self.outbounds_ration
        elif self._action == 1:
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

