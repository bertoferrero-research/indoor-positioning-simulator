from classes.simulators.rssi.interface import RssiInterface

class RssiFactory:
    """
    A factory class for creating trajectory simulators.
    """

    @staticmethod
    def create_rssi_simulator(simulator_name: str) -> RssiInterface:
        """
        Creates a trajectory simulator based on the given simulator name.

        Args:
            simulator_name (str): The name of the simulator.

        Returns:
            TrajectoryInterface: An instance of the trajectory simulator.

        Raises:
            ValueError: If the simulator name is not available.
        """
        if simulator_name == 'dummy':
            from classes.simulators.rssi.dummy import DummyRssiModule
            return DummyRssiModule()
        else:
            raise ValueError(f"Rssi simulator {simulator_name} not available.")
