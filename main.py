import argparse
import os
import json
import random
from classes.station import Station
from classes.bufferedcsvfilewriter import BufferedCsvFileWriter
from classes.simulators.trajectory.dummy import DummyPositionModule
import datetime


class App:
    def __init__(self, config_path, stations_path, output_dir):
        # Load settings and stations
        self.loadSettings(config_path=config_path)
        self.loadStations(stations_path=stations_path)
        self.output_dir = output_dir
        self.position_rounding = 9

    def loadSettings(self, config_path):
        # First check if the config file exists
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file {config_path} not found")

        # Load the config file as json file
        with open(config_path, 'r') as file:
            self.config = json.load(file)

        # Check if the config file was loaded correctly
        if not isinstance(self.config, dict):
            raise ValueError("Invalid config file format.")

        # Verify coherence
        if self.config['initial_position']['x'] < self.config['margin_meters'] or self.config['initial_position']['x'] > self.config['room_dim_meters']['x'] - self.config['margin_meters']:
            raise ValueError("Initial x position is out of bounds.")
        if self.config['initial_position']['y'] < self.config['margin_meters'] or self.config['initial_position']['y'] > self.config['room_dim_meters']['y'] - self.config['margin_meters']:
            raise ValueError("Initial y position is out of bounds.")

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

    def start(self):
        # Initialize main variables
        max_time_milliseconds = self.config['simulation_duration_seconds'] * 1000
        current_time = 0
        iteration = 0
        milliseconds_per_iteration = min(
            [station.frequency for station in self.stations])
        if milliseconds_per_iteration < 10:
            raise ValueError("Minimum frequency is 10 millisecond.")
        pos_x = round(self.config['initial_position']
                      ['x'], ndigits=self.position_rounding)
        pos_y = round(self.config['initial_position']
                      ['y'], ndigits=self.position_rounding)
        speed = self.config['speed_meters_second']['min']

        # Define maximal and minimal x and y coordinates
        min_x = self.config['margin_meters']
        max_x = self.config['room_dim_meters']['x'] - \
            self.config['margin_meters']
        min_y = self.config['margin_meters']
        max_y = self.config['room_dim_meters']['y'] - \
            self.config['margin_meters']

        # Create output file writers
        # Concatenate date and time to the file names
        current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create output file writers with updated file names
        rssi_writer = BufferedCsvFileWriter(
            os.path.join(self.output_dir, f"rssi_{current_datetime}.csv"))
        rssi_writer.write(['timestamp', 'position_x',
                          'position_y', 'station_mac', 'rssi'])

        trajectory_writer = BufferedCsvFileWriter(
            os.path.join(self.output_dir, f"trajectory_{current_datetime}.csv"))
        trajectory_writer.write(
            ['step', 'timestamp', 'position_x', 'position_y'])

        # Write the initial position
        trajectory_writer.write(
            [iteration, current_time, pos_x, pos_y])

        # Initialize modules
        # TODO: use a Factory
        # TODO: Define the attributes of the constructor
        position_module = DummyPositionModule()

        try:
            # Main loop
            while True:
                # Increase counters
                iteration += 1
                current_time += milliseconds_per_iteration

                # Calculate the new position of the stations
                # TODO: Implement the logic to calculate the new position of the stations
                pos_x, pos_y = position_module.calculate_position(current_time=current_time, milliseconds_per_iteration=milliseconds_per_iteration,
                                                                  current_x=pos_x, current_y=pos_y, min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y, speed=speed)
                pos_x = round(pos_x,
                              ndigits=self.position_rounding)
                pos_y = round(pos_y,
                              ndigits=self.position_rounding)

                # Write the new position to the output file
                trajectory_writer.write(
                    [iteration, current_time, pos_x, pos_y])

                # For each required station, generate the static RSSI value
                for station in [station for station in self.stations if station.next_transmission_timestamp <= current_time]:
                    # TODO: Implement the logic to calculate the RSSI value
                    rssi = random.randint(-100, 0)
                    # Set the last transmission timestamp
                    station.last_transmission_timestamp = current_time
                    # Write the RSSI value to the output file
                    rssi_writer.write(
                        [current_time, pos_x, pos_y, station.mac, rssi])

                # Check we achieved the maximum execution time
                if current_time >= max_time_milliseconds:
                    break
        finally:
            # Close the output file writers
            rssi_writer.close()
            trajectory_writer.close()


def main():
    # Load arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config', default=os.path.join(os.path.dirname(__file__), 'config.json'))
    parser.add_argument(
        '--stations', default=os.path.join(os.path.dirname(__file__), 'stations.json'))
    parser.add_argument(
        '--outdir', default=os.path.join(os.path.dirname(__file__), 'output/'))
    args = parser.parse_args()

    app = App(args.config, args.stations, args.outdir)
    app.start()


if __name__ == "__main__":
    main()
