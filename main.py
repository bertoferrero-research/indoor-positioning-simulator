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

import argparse
import math
import os
import json
import random
from classes.models.station import Station
from classes.lib.bufferedcsvfilewriter import BufferedCsvFileWriter
from classes.simulators.trajectory.factory import TrajectoryFactory
from classes.simulators.rssi.factory import RssiFactory
from classes.config import Config
from classes.simulation import Simulation
import datetime
import numpy as np


class App:
    """
    App class for initializing and running the indoor positioning simulator.

    Attributes:
        config (Config): Configuration settings loaded from the config file.
        output_dir (str): Directory where output files will be saved.
    """
    def __init__(self, config_path, stations_path, output_dir):
        """
        Initializes the simulator with the given configuration and station data.

        Args:
            config_path (str): Path to the configuration file.
            stations_path (str): Path to the file containing station data.
            output_dir (str): Directory where output files will be saved.
        """
        # Load settings and stations
        self.config = Config(config_path=config_path)
        self.loadStations(stations_path=stations_path)
        self.output_dir = output_dir 

    def loadStations(self, stations_path):
        """
        Load station configurations from a JSON file.
        Args:
            stations_path (str): The file path to the JSON file containing station definitions.
        Raises:
            FileNotFoundError: If the stations definition file does not exist.
            ValueError: If the stations definition file format is invalid or if required fields are missing.
        The JSON file should contain a list of station definitions, where each station is a dictionary
        with, at least, the following keys:
            - mac (str): The MAC address of the station.
            - x (float): The x-coordinate of the station.
            - y (float): The y-coordinate of the station.
            - frequency (float): The frequency of the station.
        Example of a valid JSON file content:
        [
            {
            "mac": "001122334455",
            "x": 10.0,
            "y": 20.0,
            "frequency": 250
            },
            ...
        ]
        """
        # First check if the config file exists
        if not os.path.exists(stations_path):
            raise FileNotFoundError(
                f"Stations definition file {stations_path} not found")

        # Load the config file as json file
        with open(stations_path, 'r') as file:
            stationsConfig = json.load(file)

        # Check if setationsConfig is a list
        if not isinstance(stationsConfig, list):
            raise ValueError("Invalid stations definition file format.")

        # Lets go, load all the stations
        self.stations = []
        for station in stationsConfig:
            # Check if all the required fields are present
            if not all([field in station for field in ['mac', 'x', 'y', 'frequency']]):
                raise ValueError("Invalid station definition format.")
            self.stations.append(Station(**station))

    def run_simulation(self):
        """
        Runs the indoor positioning simulation.

        This method initializes a Simulation object with the provided configuration,
        stations, and output directory, and then starts the simulation process.

        Returns:
            None
        """
        simulation = Simulation(self.config, self.stations, self.output_dir)
        simulation.start()


def main():
    # Set default config dir
    default_config_dir = os.path.join(os.path.dirname(__file__), 'config', 'danis2022')
    # Load arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config', default=os.path.join(default_config_dir, 'config.json'))
    parser.add_argument(
        '--stations', default=os.path.join(default_config_dir, 'stations.json'))
    parser.add_argument(
        '--outdir', default=os.path.join(os.path.dirname(__file__), 'output/'))
    args = parser.parse_args()

    app = App(args.config, args.stations, args.outdir)
    app.run_simulation()


if __name__ == "__main__":
    main()
