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
    
    
    @staticmethod
    def lineal(x: float, a: float, b: float) -> float:
        """
        Calculates the value of a linear model function.

        Parameters:
        x (float): The input value.
        a (float): The slope of the linear model.
        b (float): The y-intercept of the linear model.

        Returns:
        float: The calculated value of the linear model function.
        """
        return a * x + b