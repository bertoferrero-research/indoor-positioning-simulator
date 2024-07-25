from typing import Union


class Station:
    '''
    Class representing an access point station.
    '''

    def __init__(self, mac: str, x: float, y: float, frequency: int, Tx: float = None, n: float = None, noise_std_dev: float = 0, missing_packages_probability: dict = None, initial_timestamp: int = 0):
        """
        Constructor for the Station class.

        Args:
            mac (str): The MAC address of the access point station.
            x (float): The x-coordinate of the access point station's location.
            y (float): The y-coordinate of the access point station's location.
            frequency (int): The transmission frequency of the access point station in milliseconds.
            Tx (float, optional): The Tx parameter of the access point station, used for the RSSI to Distance formula. Defaults to None.
            n (float, optional): The n parameter of the access point station, used for the RSSI to Distance formula. Defaults to None.
            noise_std_dev (float, optional): The standard deviation of the noise of the access point station to add to RSSI simulation results. Defaults to 0.
            missing_packages_probability (dict, optional): A dictionary representing the probability of missing packages for different distances. Defaults to None. It should contain a key "function_model" with the value "sigmoid" or "exponential" and a key "parameters" with the parameters of the model.
            initial_timestamp (int, optional): The initial timestamp of the access point station. Defaults to 0.
        """
        self._mac = mac
        self._x = x
        self._y = y
        self._frequency = frequency
        self._Tx = Tx
        self._n = n
        self._noise_std_dev = noise_std_dev
        self._missing_packages_probability = missing_packages_probability
        self._last_transmission_timestamp = initial_timestamp
        self._next_transmission_timestamp = initial_timestamp + frequency

    @property
    def mac(self) -> str:
        """
        str: The MAC address of the access point station.
        """
        return self._mac

    @property
    def x(self) -> float:
        """
        float: The x-coordinate of the access point station's location.
        """
        return self._x

    @property
    def y(self) -> float:
        """
        float: The y-coordinate of the access point station's location.
        """
        return self._y

    @property
    def frequency(self) -> int:
        """
        int: The transmission frequency of the access point station in milliseconds.
        """
        return self._frequency

    @property
    def Tx(self) -> float | None:
        """
        Returns the Tx parameter of the access point station.

        Returns:
            float | None: The Tx parameter of the access point station.
        """
        return self._Tx

    @property
    def n(self) -> float | None:
        """
        Returns the n parameter of the access point station.

        Returns:
            float | None: The n parameter of the access point station.
        """
        return self._n
    
    @property
    def noise_std_dev(self) -> float:
        """
        float: The standard deviation of the noise of the access point station to add to RSSI simulation results.
        """
        return self._noise_std_dev
    
    @property
    def missing_packages_probability(self) -> dict | None:
        """
        Get the probability of missing packages for the station.

        Returns:
            dict | None: A dictionary representing the probability of missing packages for the station.
                            If the probability is not available, None is returned.
        """
        return self._missing_packages_probability

    @property
    def last_transmission_timestamp(self) -> int:
        """
        int: The timestamp of the last transmission made by the access point station.
        """
        return self._last_transmission_timestamp

    @last_transmission_timestamp.setter
    def last_transmission_timestamp(self, timestamp: int):
        """
        Setter for the last transmission timestamp.

        Args:
            timestamp (int): The timestamp of the last transmission made by the access point station.
        """
        self._last_transmission_timestamp = timestamp
        self._next_transmission_timestamp = self._last_transmission_timestamp + self._frequency

    @property
    def next_transmission_timestamp(self) -> int:
        """
        int: The timestamp of the next scheduled transmission by the access point station.
        """
        return self._next_transmission_timestamp
