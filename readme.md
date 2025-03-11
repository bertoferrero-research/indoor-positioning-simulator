# Indoor Positioning Simulator

This is a simulator for trajectories and RSSI signals inside a room, developed for studying indoor positioning systems. The mobile node captures signals as it moves through a simulated environment, helping researchers analyze positioning techniques.

Please, cite one or both the following works for any use of the code or for a reference to the pusblished work:

```bibtex
@inproceedings{FerreroLopez2025simulator,
  author = {Ferrero-Lopez, Alberto and Gallego, Antonio Javier and Lozano, Miguel Angel},
  title = {Synthetic Data for Indoor Positioning Systems: Reducing Offline Collection Costs},
  booktitle = {Proceedings of the 2025 International Conference on Advanced Machine Learning and Data Science (AMLDS)},
  location = {Tokyo, Japan},
  month = {July 19--21},
  year = {2025}
}
```

```bibtex
@article{FerreroLopez2025ipsNetwork,
  author = {Ferrero-Lopez, Alberto and Gallego, Antonio Javier and Lozano, Miguel Angel},
  title = {Bluetooth Low Energy Indoor Positioning: A Fingerprinting Neural Network Approach},
  journal = {Internet Of Things},
  year = {2025}
}
```

## Installation

Clone this repository and install the required dependencies:

```bash
git clone https://github.com/bertoferrero-researches/indoor-positioning-simulator.git
cd indoor-positioning-simulator
pip install -r requirements.txt
```

## Usage

To run the simulator, you need to define three parameters:

- **`--config`**: Path to the simulation configuration file. By default, it will use `config.json` from `./config/danis2022`.
- **`--stations`**: Path to the BLE stations configuration file. By default, it will use `stations.json` from `./config/danis2022`.
- **`--outdir`**: Path to the output directory where the results will be saved. By default, the output will be saved in `./output`.

### Example of Execution:

```bash
python main.py --config ./myconfig/config.json --stations ./myconfig/stations.json --outdir ./myoutput
```

## Configuration

The execution of the simulator is based on two configuration files: one that contains the general execution settings, and another that describes the characteristics of each BLE transmitter. You can find examples of these files in the `config` folder.

### General Configuration (`config.json`)

This file defines the general simulation settings, including the environment and movement parameters.

#### Explanation of the Fields:
- **`simulation_duration_seconds`**: Total time of the simulation in seconds.
- **`room_dim_meters`**: The dimensions of the room, with:
  - `x`: Room length in meters.
  - `y`: Room width in meters.
- **`margin_meters`**: A buffer zone or margin to ensure the node stays within safe boundaries, specified in meters.
- **`speed_meters_seconds`**: Speed of the mobile node in meters per second.
- **`initial_position`**: The starting position of the mobile node, with:
  - `x`: Initial x-coordinate of the node.
  - `y`: Initial y-coordinate of the node.
- **`initial_angle_degrees`**: The initial movement angle of the mobile node, measured in degrees (0-360).
- **`output_trajectory`**: A boolean value (`true` or `false`), indicating whether the simulator should output a file with the trajectory data (`true`) or only output the RSSI simulation file (`false`).
- **`simulators`**: Contains the selection and configuration of the trajectory and RSSI simulation modules:
  - **`trajectory`**: Specifies the trajectory simulation model to use.
  - **`trajectory_parameters`**: Contains configuration parameters specific to the chosen trajectory model.
  - **`rssi`**: Specifies the RSSI simulation model to use.
  - **`rssi_parameters`**: Contains configuration parameters for the RSSI simulation model (left empty in the provided example).

#### Example of `config.json`:

```json
{
    "simulation_duration_seconds": 60,
    "room_dim_meters": {
        "x": 20.66,
        "y": 17.64
    },
    "margin_meters": 0.5,
    "speed_meters_second": 0.35,
    "initial_position": {
        "x": 18.031,
        "y": 8.465
    },
    "initial_angle_degrees": 180,
    "output_trajectory": true,
    "simulators": {
        "trajectory": "daniscemgil2017custom",
        "trajectory_parameters": {
            "daniscemgil2017custom": {
                "keep_angle_ms": 300
            }
        },
        "rssi": "logdistance",
        "rssi_parameters": {
        }
    }
}
```

### BLE Stations Configuration (`stations.json`)

This file contains a list of BLE (Bluetooth Low Energy) transmitters with their respective properties.

#### Explanation of the Fields:
- **`mac`**: The MAC address of the BLE transmitter (e.g., "b827eb4521b4").
- **`x`**: The x-coordinate of the BLE transmitter's position in the room, measured in meters.
- **`y`**: The y-coordinate of the BLE transmitter's position in the room, measured in meters.
- **`frequency`**: The frequency at which the BLE transmitter sends signals, in milliseconds.
- **`initial_timestamp`**: The starting time (in seconds) for the first signal transmission from the BLE transmitter.
- **`Tx`**: The transmission power of the BLE transmitter in decibel-milliwatts (dBm). This indicates the strength of the signal emitted by the transmitter.
- **`n`**: The path-loss exponent, which defines how the signal strength diminishes over distance. A higher value means faster signal degradation.
- **`noise_std_dev`**: The standard deviation of noise in the RSSI (Received Signal Strength Indicator) signal. This simulates random environmental noise affecting the signal.
- **`missing_packages_probability`**: Describes the probability of losing or missing signal packets.
  - **`function_model`**: The model used to calculate the probability of missing signal packets, it accepts "lineal", "sigmoid" and "exponential" models.
  - **`params`**: Parameters for the probability model


#### Example of `stations.json`:

```json
[
    {
        "mac": "b827eb4521b4",
        "x": 7.00,
        "y": 7.09,
        "frequency": 455,
        "initial_timestamp": 0,
        "Tx": -58.29111418190961,
        "n": 1.8961618351023355,
        "noise_std_dev": 5.373610075920007,
        "missing_packages_probability": {
            "function_model": "lineal",
            "params": {
                "a": 0.003939045455604084,
                "b": 0.025243145143738085
            }
        }
    },
]
```

## Implemented Simulators

### For Trajectory Simulation:
- **`dummy`**: A simple simulator for testing purposes. It returns a random position within the simulation area.
- **`daniscemgil2017`**: A trajectory simulator based on the work *"Model-Based Localization and Tracking Using Bluetooth Low-Energy Beacons"* by Daniş and Cemgil. 
  - **Parameters in `trajectory_parameters`:**
    - `s`: Specifies the standard deviation used to randomize the angle. Default: `0.07`.
- **`daniscemgil2017custom`**: An evolution of the previous simulator with an additional parameter to prevent the node from constantly turning.
  - **Parameters in `trajectory_parameters`:**
    - `s`: Specifies the standard deviation used to randomize the angle. Default: `0.07`.
    - `keep_angle_ms`: Specifies the number of milliseconds during which the node’s angle is locked (i.e., no turning). Default: `300`.

### For RSSI Simulation:
- **`dummy`**: A simple simulator for testing purposes. It returns a random RSSI value between -100 and 0.
- **`logdistance`**: Implements the path loss equation to estimate the RSSI value of each station based on the distance between the mobile node and the station.


## Output

The simulator generates two CSV files as output. These files are written in real-time, with data flushed to disk every 1000 rows.

- **`rssi.csv`**: Contains all RSSI (Received Signal Strength Indicator) readings received by the mobile node. The columns are:
  - `timestamp`: The time of the reading in seconds.
  - `position_x`: The x-coordinate of the mobile node at the time of the reading.
  - `position_y`: The y-coordinate of the mobile node at the time of the reading.
  - `station_mac`: The MAC address of the BLE station that transmitted the signal.
  - `rssi`: The strength of the received signal in dBm.

- **`trajectory.csv`**: Contains all the points the mobile node has passed through. This file only includes information about the simulated trajectory and will only be generated if the corresponding configuration option (`output_trajectory`) is set to `true`. The columns are:
  - `step`: The incremental step number.
  - `timestamp`: The time of the step in seconds.
  - `position_x`: The x-coordinate of the mobile node at this step.
  - `position_y`: The y-coordinate of the mobile node at this step.

These files will be saved to the directory specified in the `--outdir` parameter during execution.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](./LICENSE) file for details.
