# instruments.py
from abc import ABC, abstractmethod
import numpy as np
from typing import Literal

OptionType = Literal["call", "put"]

class Instrument(ABC):
    """
    Abstract Base Class for all financial instruments.
    """
    @abstractmethod
    def payoff(self, prices: np.ndarray) -> np.ndarray:
        """
        Calculate the payoff given a simulated price path.
        
        Args:
            prices (np.ndarray): A 2D array of shape (simulations, steps).
                                 prices[:, -1] is the terminal price.
        """
        pass

class EuropeanOption(Instrument):
    def __init__(self, strike: float, option_type: OptionType):
        self.strike = strike
        self.option_type = option_type

    def payoff(self, prices: np.ndarray) -> np.ndarray:
        # European options only depend on the final price at maturity (T)
        terminal_price = prices[:, -1]
        
        if self.option_type == "call":
            return np.maximum(terminal_price - self.strike, 0)
        else:
            return np.maximum(self.strike - terminal_price, 0)

class AsianOption(Instrument):
    """
    Asian Option: Payoff depends on the AVERAGE price over the path.
    This demonstrates handling of 'Path Dependent' options.
    """
    def __init__(self, strike: float, option_type: OptionType):
        self.strike = strike
        self.option_type = option_type

    def payoff(self, prices: np.ndarray) -> np.ndarray:
        # Calculate the arithmetic average across the time path
        average_price = np.mean(prices, axis=1)
        
        if self.option_type == "call":
            return np.maximum(average_price - self.strike, 0)
        else:
            return np.maximum(self.strike - average_price, 0)
        
class AmericanOption(Instrument):
    def __init__(self, strike: float, optionType: OptionType):
        self.strike = strike
        self.optionType = optionType

    def payoff(self, prices: np.ndarray)-> np.ndarray:
        if(self.optionType == "call"):
            return np.maximum(prices-self.strike, 0)
        else:
            return np.maximum(self.strike-prices, 0)