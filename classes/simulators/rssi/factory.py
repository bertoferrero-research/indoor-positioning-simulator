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
