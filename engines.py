# engines.py
import numpy as np
from scipy.stats import norm
from market import MarketEnvironment
from instruments import Instrument, EuropeanOption

class AnalyticEngine:
    """
    Closed-form solutions (Black-Scholes-Merton) for validation.
    """
    @staticmethod
    def price_european(market: MarketEnvironment, instrument: EuropeanOption, T: float) -> float:
        S = market.spot_price
        K = instrument.strike
        r = market.risk_free_rate
        sigma = market.volatility
        q = market.dividend_yield
        
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if instrument.option_type == "call":
            price = (S * np.exp(-q * T) * norm.cdf(d1) - 
                     K * np.exp(-r * T) * norm.cdf(d2))
        else:
            price = (K * np.exp(-r * T) * norm.cdf(-d2) - 
                     S * np.exp(-q * T) * norm.cdf(-d1))
        return price

class MonteCarloEngine:
    """
    Pricing engine using Monte Carlo simulation for path-dependent options.
    """
    def __init__(self, market: MarketEnvironment, simulations: int = 10000, steps: int = 100):
        self.market = market
        self.sims = simulations
        self.steps = steps

    def generate_paths(self, T: float) -> np.ndarray:
        """
        Simulates asset price paths using Geometric Brownian Motion (Vectorized).
        """
        dt = T / self.steps
        
        # Random component: Z ~ N(0, 1)
        Z = np.random.standard_normal((self.sims, self.steps))
        
        # Drift and Diffusion components
        # drift = (r - 0.5 * sigma^2) * dt
        drift = (self.market.risk_free_rate - 0.5 * self.market.volatility ** 2) * dt
        diffusion = self.market.volatility * np.sqrt(dt) * Z
        
        # Calculate log returns and cumulate them
        log_returns = np.cumsum(drift + diffusion, axis=1)
        
        # Add the initial spot price to the path
        # prices = S0 * exp(cumulative_returns)
        prices = self.market.spot_price * np.exp(log_returns)
        
        return prices

    def get_price(self, instrument: Instrument, T: float) -> float:
        # 1. Generate Paths
        paths = self.generate_paths(T)
        
        # 2. Calculate Payoff for each path
        payoffs = instrument.payoff(paths)
        
        # 3. Discount the average payoff back to present
        discount_factor = np.exp(-self.market.risk_free_rate * T)
        price = discount_factor * np.mean(payoffs)
        
        return price
    
class LSMEngine(MonteCarloEngine):
    """
    Least square method (Longstaff-Schwartz) for American options.
    """

    def get_price(self, instrument, T):
        paths = self.generate_paths(T) # 2D Array with T in X axis and Simulation number in Y Axis
        dt = T/self.steps
        discount_factor = np.exp(-self.market.risk_free_rate * dt)

        cashflows = instrument.payoff(paths[:,-1])

        for t in range(self.steps-1, -1, -1):
            st = paths[:,t] #Stock prices at t for all simulations(Vertical array)
            payoff = instrument.payoff(st) #Payoff at time t for all simulations(Vertical array)
            inTheMoney = payoff>0 #Vertical Boolean array depicting positive payoff at time t at which simulations

            if np.count_nonzero(inTheMoney)>0:
                X = st[inTheMoney] #Stock prices for all simulations with positive payoffs
                Y = cashflows[inTheMoney] #Payoffs of the positive simulations
                coefficients = np.polyfit(X,Y,deg=2) #Get the coefficients of the Regression based on Stock Prices and Payoffs
                continuation_values = np.polyval(coefficients, X) #After getting the regression line use the coefficients and Stock prices to get the predicted future payoff
                exercise_decision = payoff[inTheMoney]>continuation_values #Check if the current payoff time t is greater than predicted future payoff
                cashflows = cashflows*discount_factor
                full_exercise_indices = np.where(inTheMoney)[0][exercise_decision] #intheMoney[0] gets all the true values in inTheMoney Boolean array and then on top of it excercise_decision is added to filter out early excercise simulations
                cashflows[full_exercise_indices] = payoff[full_exercise_indices] #Overrides the value of discounted cashflows with their actual payoffs for those where early excercise is to be done
            else:
                cashflows = cashflows*discount_factor
        
        return np.mean(cashflows*(discount_factor))
