import argparse
import os
import json
from classes.station import Station

class App:
    def __init__(self, config_path, stations_path):
        # Load settings and stations
        self.loadSettings(config_path=config_path)
        self.loadStations(stations_path=stations_path)

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
        if self.config['initial_position']['x'] < self.config['initial_position']['margin_meters'] or self.config['initial_position']['x'] > self.config['initial_position']['x'] - self.config['initial_position']['margin_meters']:
            raise ValueError("Initial x position is out of bounds.")
        if self.config['initial_position']['y'] < self.config['initial_position']['margin_meters'] or self.config['initial_position']['y'] > self.config['initial_position']['y'] - self.config['initial_position']['margin_meters']:
            raise ValueError("Initial y position is out of bounds.")
    
    def loadStations(self, stations_path):
        # First check if the config file exists
        if not os.path.exists(stations_path):
            raise FileNotFoundError(f"Stations definition file {stations_path} not found")

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
        # Initialize the simulation
        max_time_milliseconds = self.config['simulation_duration_seconds'] * 1000
        current_time = 0
        iteration = 0
        milliseconds_per_iteration = min([station.frequency for station in self.stations])
        if milliseconds_per_iteration < 10:
            raise ValueError("Minimum frequency is 10 millisecond.")
        pos_x = self.config['initial_position']['x']
        pos_y = self.config['initial_position']['y']

        # Define maximal and minimal x and y coordinates
        min_x = self.config['initial_position']['margin_meters']
        max_x = self.config['initial_position']['x'] - self.config['initial_position']['margin_meters']
        min_y = self.config['initial_position']['margin_meters']
        max_y = self.config['initial_position']['y'] - self.config['initial_position']['margin_meters']

        # Main loop
        while True:
            # Increase counters
            iteration += 1
            current_time += milliseconds_per_iteration
    
            # Calculate the new position of the stations
            # TODO: Implement the logic to calculate the new position of the stations
            pos_x = random.uniform(min_x, max_x)
            pos_y = random.uniform(min_y, max_y)

            # For each required station, generate the static RSSI value
            for station in [station for station in self.stations if station.next_transmission_timestamp <= current_time]:
                # TODO: Implement the logic to calculate the RSSI value
                rssi = random.randint(-100, 0)
                # Set the last transmission timestamp
                station.last_transmission_timestamp = current_time

            # Check we achieved the maximum execution time
            if self.current_time >= max_time_milliseconds:
                break
        pass

def main():
    #Load arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default=os.path.join(os.path.dirname(__file__), 'config.json'))
    parser.add_argument('--stations', default=os.path.join(os.path.dirname(__file__), 'stations.json'))
    args = parser.parse_args()

    app = App(args.config, args.stations)
    app.start()

if __name__ == "__main__":
    main()