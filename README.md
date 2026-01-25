# Derivatives Pricing Engine

A comprehensive Python-based toolkit for pricing financial derivatives using various numerical methods. This project implements closed-form solutions (Black-Scholes-Merton), Monte Carlo simulations, and the Least Squares Monte Carlo (LSM) method for American options.

## Features

- **Analytic Engine**: Closed-form Black-Scholes-Merton pricing for European options.
- **Monte Carlo Engine**: Path-dependent option pricing (e.g., Asian options) with Geometric Brownian Motion simulations.
- **LSM Engine**: Least Squares Monte Carlo for American options, handling early exercise optimally.
- **Instrument Classes**: Support for European, Asian, and American call/put options.
- **Greeks Calculation**: Finite difference method for Delta calculation.
- **Modular Design**: Easily extensible for new instruments and engines.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/derivatives-pricing-engine.git
   cd derivatives-pricing-engine
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   # On Windows:
   .\.venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is not present, install manually:
   ```bash
   pip install numpy scipy
   ```

## Usage

### Basic Example
Run the main script to see pricing examples:

```bash
python main.py
```

This will output prices for European and Asian calls using Monte Carlo, benchmarked against Black-Scholes, and American options using LSM.

### Custom Pricing
Import and use the engines in your code:

```python
from market import MarketEnvironment
from instruments import EuropeanOption, AmericanOption
from engines import AnalyticEngine, MonteCarloEngine, LSMEngine

# Setup market
env = MarketEnvironment(spot_price=100.0, risk_free_rate=0.05, volatility=0.2)

# Define option
option = EuropeanOption(strike=100.0, option_type="call")

# Price with Black-Scholes
price = AnalyticEngine.price_european(env, option, T=1.0)
print(f"BS Price: {price:.4f}")

# Price with Monte Carlo
mc_engine = MonteCarloEngine(env, simulations=10000, steps=252)
mc_price = mc_engine.get_price(option, T=1.0)
print(f"MC Price: {mc_price:.4f}")

# For American options
american_option = AmericanOption(strike=100.0, optionType="call")
lsm_engine = LSMEngine(env, simulations=10000, steps=100)
lsm_price = lsm_engine.get_price(american_option, T=1.0)
print(f"LSM Price: {lsm_price:.4f}")
```

### Calculating Greeks
Use the `calculate_delta` function for Delta:

```python
from main import calculate_delta

delta = calculate_delta(mc_engine, option, T=1.0)
print(f"Delta: {delta:.4f}")
```

## Project Structure

```
derivatives-pricing-engine/
├── main.py              # Main script with examples and Greeks calculation
├── engines.py           # Pricing engines (Analytic, Monte Carlo, LSM)
├── instruments.py       # Instrument classes (European, Asian, American options)
├── market.py            # Market environment dataclass
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Dependencies

- **numpy**: For numerical computations and array operations.
- **scipy**: For statistical functions (e.g., normal CDF in Black-Scholes).

## Methodology

- **Black-Scholes-Merton**: Closed-form solution for European options under GBM assumptions.
- **Monte Carlo**: Simulates asset paths and averages discounted payoffs.
- **LSM (Longstaff-Schwartz)**: Backward induction with polynomial regression to estimate continuation values for American options.
- **Geometric Brownian Motion**: Used for path generation in stochastic simulations.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, open an issue first to discuss.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/new-engine`)
3. Commit changes (`git commit -am 'Add new engine'`)
4. Push to branch (`git push origin feature/new-engine`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Based on quantitative finance concepts from Hull's "Options, Futures, and Other Derivatives".
- LSM method from Longstaff & Schwartz (2001).

## Contact

For questions or issues, open a GitHub issue or contact [your-email@example.com].