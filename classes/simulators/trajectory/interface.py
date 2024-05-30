from abc import ABC, abstractmethod

class TrajectoryInterface(ABC):

    @abstractmethod
    def calculate_position(self, current_time: int, milliseconds_per_iteration: int, current_x: float, current_y: float, min_x: float, max_x: float, min_y: float, max_y: float, speed: float) -> tuple:
        pass