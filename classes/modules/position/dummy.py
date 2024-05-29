from positioninterface import PositionInterface

class DummyPositionModule(PositionInterface):

    def calculate_position(self, current_time: int, milliseconds_per_iteration: int, current_x: float, current_y: float, min_x: float, max_x: float, min_y: float, max_y: float, speed: float) -> tuple:
        return (random.uniform(min_x, max_x), random.uniform(min_y, max_y))