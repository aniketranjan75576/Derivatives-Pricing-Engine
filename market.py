# market.py
from dataclasses import dataclass

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