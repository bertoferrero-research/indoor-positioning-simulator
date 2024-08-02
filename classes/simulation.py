import datetime
import math
import os
from typing import List

from classes.lib.bufferedcsvfilewriter import BufferedCsvFileWriter
from classes.simulators.rssi.factory import RssiFactory
from classes.simulators.trajectory.factory import TrajectoryFactory
from classes.config import Config
from classes.models.station import Station


class Simulation:
    """
    Class representing an indoor positioning simulation.

    Attributes:
        config (Config): The configuration object for the simulation.
        stations (List[Station]): The list of stations in the simulation.
        output_dir (str): The output directory for the simulation results.
        position_rounding (int): The number of decimal places to round the position coordinates.

    Methods:
        start(): Starts the simulation.
        _plot_trajectory(): Plot the trajectory of a mobile device in a given scenario.
    """

    def __init__(self, config: Config, stations: List[Station], output_dir):
        """
        Initialize a Simulation object.

        Args:
            config (Config): The configuration object for the simulation.
            stations (List[Station]): The list of stations in the simulation.
            output_dir (str): The output directory for the simulation results.
        """
        self.config = config
        self.stations = stations
        self.output_dir = output_dir
        self.position_rounding = 9

    def start(self):
        """
        Starts the simulation.

        This method initializes the main variables, creates output file writers,
        initializes simulator modules, and runs the main loop of the simulation.

        Returns:
            None
        """
        
        #region Variables initialization

        # Initialize main variables
        max_time_milliseconds = self.config.simulation_duration_seconds * 1000
        current_time = 0
        iteration = 0
        # min([station.frequency for station in self.stations])
        milliseconds_per_iteration = 1
        # if milliseconds_per_iteration < 10:
        #    raise ValueError("Minimum frequency is 10 millisecond.")

        # Define maximal and minimal x and y coordinates
        dim_x = self.config.room_dim_meters['x']
        dim_y = self.config.room_dim_meters['y']
        dim_margins = self.config.margin_meters
        min_x = dim_margins
        max_x = dim_x - dim_margins
        min_y = dim_margins
        max_y = dim_y - dim_margins
        pos_x = round(self.config.initial_position
                        ['x'], ndigits=self.position_rounding)
        pos_y = round(self.config.initial_position
                        ['y'], ndigits=self.position_rounding)
        speed = self.config.speed_meters_second
        angle = math.radians(self.config.initial_angle_degrees)

        # Create output file writers
        # Concatenate date and time to the file names
        current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Define output prefix filename
        output_prefix = f"{current_datetime}_{self.config.simulation_duration_seconds}"

        # Create output file writers with updated file names
        rssi_writer = BufferedCsvFileWriter(
            os.path.join(self.output_dir, f"{output_prefix}_rssi.csv"))
        rssi_writer.write(['timestamp', 'position_x',
                            'position_y', 'station_mac', 'rssi'])

        trajectory_writer = BufferedCsvFileWriter(
            os.path.join(self.output_dir, f"{output_prefix}_trajectory.csv"))
        trajectory_writer.write(
            ['step', 'timestamp', 'position_x', 'position_y'])

        # Initialize simulators modules
        position_simulator_module = TrajectoryFactory.create_trajectory_simulator(
            self.config.trajectory_simulator_module,
            self.config.trajectory_simulator_module_parameters)
        rssi_simulator_module = RssiFactory.create_rssi_simulator(
            self.config.rssi_simulator_module,
            self.config.rssi_simulator_module_parameters)

        #endregion

        #region main loop
        try:
            # Main loop
            while True:
                # Increase counters
                iteration += 1

                # Write the current position to the output file
                trajectory_writer.write(
                    [iteration, current_time/1000, pos_x, pos_y])

                # For each required station, generate the static RSSI value
                for station in [station for station in self.stations if station.next_transmission_timestamp <= current_time]:
                    # Calculate the RSSI value
                    rssi = rssi_simulator_module.calculate_rssi(
                        station=station, current_time=current_time, milliseconds_per_iteration=milliseconds_per_iteration, current_x=pos_x, current_y=pos_y, speed=speed)
                    # Set the last transmission timestamp
                    station.last_transmission_timestamp = current_time
                    # Check if the signal is valid
                    if rssi is None:
                        continue
                    # Write the RSSI value to the output file
                    rssi_writer.write(
                        [current_time/1000, pos_x, pos_y, station.mac, rssi])

                # Check if we achieved the maximum execution time
                current_time += milliseconds_per_iteration
                if current_time >= max_time_milliseconds:
                    break                

                # Calculate the next position of the mobile device
                pos_x, pos_y, angle = position_simulator_module.calculate_position(current_time=current_time, milliseconds_per_iteration=milliseconds_per_iteration,
                                                                                    last_angle=angle, last_x=pos_x, last_y=pos_y, min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y, speed=speed)
                pos_x = round(pos_x,
                                ndigits=self.position_rounding)
                pos_y = round(pos_y,
                                ndigits=self.position_rounding)
                
        finally:
            # Close the output file writers
            rssi_writer.close()
            trajectory_writer.close()

        #endregion

        # Plot the trajectory data
        self._plot_trajectory(trajectory_csv_file=trajectory_writer.filename, dim_x=dim_x, dim_y=dim_y, min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y, output_name=f'{output_prefix}_trajectory_plot')
    

    def _plot_trajectory(self, trajectory_csv_file: str, dim_x: float, dim_y: float, min_x: float, max_x: float, min_y: float, max_y: float, output_name: str):
        """
        Plot the trajectory of a mobile device in a given scenario.

        Args:
            trajectory_csv_file (str): The file path of the trajectory data in CSV format.
            dim_x (float): The dimension of the scenario in the X-axis.
            dim_y (float): The dimension of the scenario in the Y-axis.
            min_x (float): The minimum value of the X-axis range.
            max_x (float): The maximum value of the X-axis range.
            min_y (float): The minimum value of the Y-axis range.
            max_y (float): The maximum value of the Y-axis range.
            output_name (str): The name of the output file.

        Returns:
            None
        """
        import matplotlib.pyplot as plt
        import pandas as pd

        # Load the trajectory data file
        trajectory_data = pd.read_csv(trajectory_csv_file)

        # Plot the scenario
        plt.figure(figsize=(10, 10))
        # Draw the room and margins
        plt.plot([0, dim_y,  dim_y, 0, 0], [
                 0, 0, dim_x, dim_x, 0], 'k-', label='Room')
        plt.plot([min_y, max_y, max_y, min_y, min_y], [
            min_x, min_x, max_x, max_x, min_x], 'g-', label='Margins')
        # Draw the trajectory
        plt.plot(trajectory_data['position_y'],
                 trajectory_data['position_x'], 'b-')
        plt.scatter(trajectory_data['position_y'], trajectory_data['position_x'],
                    c=trajectory_data['timestamp']/1000, cmap='viridis')
        plt.colorbar(label='Time (sec.)')
        plt.xlabel('Y (m)')
        plt.ylabel('X (m)')
        plt.title('Mobile device Trajectory')
        plt.grid(True)

        # Draw the stations
        for station in self.stations:
            plt.plot(station.y, station.x, 'ro', label=f"Station {station.mac}")

        # Invert Y axis
        plt.gca().invert_yaxis()

        # Save as PNG and EPS
        plt.savefig(os.path.join(self.output_dir, f"{output_name}.png"))
        plt.savefig(os.path.join(self.output_dir, f"{output_name}.eps"))
