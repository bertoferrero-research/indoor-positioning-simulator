
# Definimos los paths generales
import json
import os
import sys
import numpy as np
import pandas as pd

# Definimos los paths generales
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(script_dir, "..", "..")
test_files_dir = os.path.join(script_dir, "test_files")

# Import the necessary modules
sys.path.append(root_dir)
from classes.simulators.rssi.factory import RssiFactory

# Define useful variables
testing_file_name = "rectangular_without_rotation_all_sensors.mbd"
testing_file_path = os.path.join(test_files_dir, testing_file_name)
testing_data_header = ['timestamp', 'mac_sensor', 'mac_beacon', 'rssi', 'pos_x', 'pos_y', 'pos_z', 'aruco_pos_1', 'aruco_pos_2', 'aruco_pos_3', 'aruco_pos_4', 'aruco_pos_5', 'aruco_pos_6', 'aruco_pos_7', 'aruco_pos_8', 'aruco_pos_9'] 
testing_data_dtype = {'timestamp': float, 'mac_sensor': str, 'mac_beacon': str, 'rssi': int, 'pos_x': float, 'pos_y': float, 'pos_z': float, 'pos_z': float}   

# General variables
speed = 0
milliseconds_per_iteration = 0

# In order to get the most accurate results, we use the same App class
from main import App
app = App(os.path.join(test_files_dir, "config.json"), os.path.join(
    test_files_dir, "stations.json"), os.path.join(test_files_dir, "output/"))

# Init the simulator module
rssi_simulator_module = RssiFactory.create_rssi_simulator(
    app.config['simulators']['rssi'])

# Load the testing file
test_data = pd.read_csv(testing_file_path, sep=',', names=testing_data_header, dtype=testing_data_dtype)

# Get the stations and index them by their MAC
stations = app.stations
stations_by_mac = {station.mac: station for station in app.stations}

# iterate each test_data line
final_data = []
for index, row in test_data.iterrows():
    # Extract required information
    station_mac = row['mac_sensor']
    current_x = row['pos_x']
    current_y = row['pos_y']
    timestamp = int(row['timestamp'])

    # Get the station
    station = stations_by_mac[station_mac]

    # Estimate the RSSI
    simulated_rssi = rssi_simulator_module.calculate_rssi(
        station=station,
        current_time=timestamp,
        milliseconds_per_iteration=milliseconds_per_iteration,
        current_x=current_x,
        current_y=current_y,
        speed=speed
    )
    # If there is not a valid estimation, we get the limit value
    if simulated_rssi is None:
        simulated_rssi = -100

    # Append the data
    final_data.append({
        'timestamp': timestamp,
        'mac_sensor': station_mac,
        'pos_x': current_x,
        'pos_y': current_y,
        'actual_rssi': row['rssi'],
        'simulated_rssi': simulated_rssi
    })

# Transform final_data to dataframe
final_data = pd.DataFrame(final_data)

# Calculamos RMSE y MAE
# First of all, we get the difference between calculated and real values
differences = final_data['actual_rssi'] - final_data['simulated_rssi']
# Calsculate the RMSE
rmse = np.sqrt((differences ** 2).mean())
# Now the mae
mae = differences.abs().mean()


# Outputs
# RSSI
output_file_path = os.path.join(script_dir, 'test_rssi_logdistance_rssi_output.csv')
if os.path.exists(output_file_path):
    os.remove(output_file_path)
final_data.to_csv(output_file_path, index=False)  
# Metrics
output_file_path = os.path.join(script_dir, 'test_rssi_logdistance_rssi_metrics.json')
if os.path.exists(output_file_path):
    os.remove(output_file_path)
with open(output_file_path, 'w') as f:
    json.dump({
        'samples': len(final_data),
        'rmse': rmse,
        'mae': mae
    }, f, indent=4)





