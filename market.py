# market.py
from dataclasses import dataclass
import numpy as np
import scipy.interpolate as interpolate

@dataclass(frozen=True)
class MarketEnvironment:
    """
    Container for market data required for pricing.
    
    Attributes:
        spot_price (float): Current price of the underlying asset (S0).
        risk_free_rate (float): Annualized risk-free rate (r).
        volatility (float): Annualized volatility (sigma).
        dividend_yield (float): Continuous dividend yield (q).
    """
    spot_price: float
    risk_free_rate: float
    volatility: float
    dividend_yield: float = 0.0

class YieldCurve:
    """
    Represents a yield curve using linear interpolation.
    
    Provides methods to retrieve zero rates and calculate discount factors
    and forward rates for different time horizons and daycount conventions.
    """

    def __init__(self, maturities: list[float], rates: list[float], isShortTerm: bool):
        """
        Initialize YieldCurve with market data.
        
        Args:
            maturities (list[float]): List of time points (in years or days depending on convention)
            rates (list[float]): Associated zero rates at each maturity
            isShortTerm (bool): If True, uses 360-day convention; if False, uses continuous compounding
        """
        self.maturities = maturities
        self.rates = rates
        self.isShortTerm = isShortTerm
        self.interpolator = interpolate.interp1d(self.maturities, self.rates, kind = 'linear', fill_value = "extrapolate")


    def getZeroRate(self, t: float) -> float:
        rate = float(self.interpolator(t))
        print(f"interpolated rate {rate} for time {t}")
        return rate
    
    def discount_factor(self, t: float, isShortTerm: bool) -> float:
        if not isShortTerm:
            return np.exp(-self.getZeroRate(t)*t)
        else:
            return 1/(1 + (self.getZeroRate(t) * (t/360)))
    
    def forward_rate(self, t1: float, t2: float, isShortTerm: bool) -> float:
        df1 = self.discount_factor(t1, isShortTerm)
        df2 = self.discount_factor(t2, isShortTerm)
        timeDifference = t2-t1
        if not isShortTerm:
            return ((df1/df2)-1)/timeDifference
        else:
            return ((df1/df2)-1)*(360/timeDifference)
        