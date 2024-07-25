import numpy as np

class functionmodels:
    """
    A collection of mathematical function models.
    """

    @staticmethod
    def sigmoid(x: float, a: float, b: float) -> float:
        """
        Compute the sigmoid function.

        Parameters:
        x (float): The input value.
        a (float): The slope parameter.
        b (float): The shift parameter.

        Returns:
        float: The computed sigmoid value.
        """
        return 1 / (1 + np.exp(-a * (x - b)))

    @staticmethod
    def exponential(x: float, a: float, b: float) -> float:
        """
        Calculate the exponential function value for a given input.

        Parameters:
        x (float): The input value.
        a (float): The coefficient 'a' in the exponential function.
        b (float): The coefficient 'b' in the exponential function.

        Returns:
        float: The calculated value of the exponential function.
        """
        return a * np.exp(b * x)