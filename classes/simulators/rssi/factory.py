from classes.simulators.rssi.interface import RssiInterface

class RssiFactory:
    """
    A factory class for creating RSSI simulators.
    """

    @staticmethod
    def create_rssi_simulator(simulator_name: str, constructor_params: dict = {}) -> RssiInterface:
        """
        Creates an RSSI simulator based on the given simulator name.

        Args:
            simulator_name (str): The name of the simulator.
            constructor_params (dict): Optional dictionary of constructor parameters.

        Returns:
            RssiInterface: An instance of the RSSI simulator.

        Raises:
            ValueError: If the simulator name is not available.
        """
        if simulator_name == 'dummy':
            from classes.simulators.rssi.dummy import DummyRssiModule
            return DummyRssiModule(**constructor_params)
        elif simulator_name == 'logdistance':
            from classes.simulators.rssi.logdistance import LogDistancePathLossModel
            return LogDistancePathLossModel(**constructor_params)
        else:
            raise ValueError(f"RSSI simulator {simulator_name} not available.")
