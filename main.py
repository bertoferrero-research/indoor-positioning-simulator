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
    def __init__(self, config_path, stations_path, output_dir):
        # Load settings and stations
        self.config = Config(config_path=config_path)
        self.loadStations(stations_path=stations_path)
        self.output_dir = output_dir 

    def loadStations(self, stations_path):
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
