from abc import ABC, abstractmethod

from abc import ABC, abstractmethod

class TrajectoryInterface(ABC):
    """
    An abstract base class for trajectory interfaces.

    This class defines the interface for calculating the position of an object
    based on various parameters.

    Methods:
        calculate_position: Calculates the position of the object based on the given parameters.
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