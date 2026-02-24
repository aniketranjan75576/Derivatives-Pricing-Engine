# main.py
from market import MarketEnvironment, YieldCurve
from instruments import EuropeanOption, AsianOption, AmericanOption, FRA
from engines import MonteCarloEngine, AnalyticEngine, LSMEngine, FRAengine

def calculate_delta(engine: MonteCarloEngine, instrument, T: float, bump: float = 0.01) -> float:
    """
    Calculates Delta using Finite Difference Method (Bump and Revalue).
    Delta ~ (Price(S + h) - Price(S - h)) / 2h
    """
    original_spot = engine.market.spot_price
    
    # Price with Up Bump
    engine.market = MarketEnvironment(original_spot * (1 + bump), engine.market.risk_free_rate, engine.market.volatility)
    price_up = engine.get_price(instrument, T)
    
    # Price with Down Bump
    engine.market = MarketEnvironment(original_spot * (1 - bump), engine.market.risk_free_rate, engine.market.volatility)
    price_down = engine.get_price(instrument, T)
    
    # Reset Market
    engine.market = MarketEnvironment(original_spot, engine.market.risk_free_rate, engine.market.volatility)
    
    return (price_up - price_down) / (2 * original_spot * bump)

def main():
    # 1. Setup Market Data
    # Spot=100, Rate=5%, Vol=20%
    optionEnv = MarketEnvironment(spot_price=100.0, risk_free_rate=0.05, volatility=0.2)
    irEnv = YieldCurve([60,180], [0.03,0.08],True)
    
    # 2. Define Instruments
    T = 1.0  # Time to maturity (1 year)
    euro_call = EuropeanOption(strike=100.0, option_type = "call")
    asian_call = AsianOption(strike=100.0, option_type = "call")
    american_call = AmericanOption(strike = 100.0, optionType = "call")
    american_put = AmericanOption(strike = 100.0, optionType = "put")
    fra_payer = FRA(60,180, 100000, 0.05, True)
    fra_receiver = FRA(60,180, 100000, 0.05, False)
    
    # 3. Analytic Price (Benchmark)
    bsm_price = AnalyticEngine.price_european(optionEnv, euro_call, T)
    print(f"--- Benchmark (Black-Scholes) ---")
    print(f"European Call Price: {bsm_price:.4f}\n")
    
    # 4. Monte Carlo Simulation
    mc_engine = MonteCarloEngine(optionEnv, simulations=50000, steps=252)
    mc_euro_price = mc_engine.get_price(euro_call, T)
    mc_asian_price = mc_engine.get_price(asian_call, T)
    
    print(f"--- Monte Carlo Simulation (50,000 paths) ---")
    print(f"European Call Price: {mc_euro_price:.4f} (Error: {abs(mc_euro_price - bsm_price):.4f})")
    print(f"Asian Call Price:    {mc_asian_price:.4f}")
    
    # 5. Calculate Greeks (Delta)
    # Asian options usually have lower delta than European
    euro_delta = calculate_delta(mc_engine, euro_call, T)
    asian_delta = calculate_delta(mc_engine, asian_call, T)
    
    print(f"\n--- Risk Metrics (Greeks) ---")
    print(f"European Delta: {euro_delta:.4f}")
    print(f"Asian Delta:    {asian_delta:.4f}")

    # 6. LSM engine simulation
    lsm_engine = LSMEngine(optionEnv, simulations=10000, steps = 100)
    lsm_call = lsm_engine.get_price(american_call, 1)
    lsm_put = lsm_engine.get_price(american_put, 1)

    print(f"\n--- American Option using LSM ---")
    print(f"American call price :{lsm_call}")
    print(f"American put price :{lsm_put}")


    # 7. FRA 
    fraEngine = FRAengine()
    fra_payer_price = fraEngine.priceFra(irEnv, fra_payer)
    print(f"\n--- IR Analytics ---\n")
    print(f"FRA payer payoff :{fra_payer_price}")

if __name__ == "__main__":
    main()