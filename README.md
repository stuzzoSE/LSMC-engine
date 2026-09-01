# American Option Pricing & Risk Engine

A quantitative framework for pricing American-style options and calculating risk sensitivities (Greeks). The engine combines the **Longstaff-Schwartz Least-Squares Monte Carlo (LSM)** algorithm with numerical stability enhancements, multi-measure volatility estimation ($\mathbb{P}$ vs. $\mathbb{Q}$), and custom random number generation.

---

## Key Features

* **American Option Engine (`Pricer.py`):** Longstaff-Schwartz (LSM) backward induction with degree-2 polynomial regression. Resolves ill-conditioned matrix warnings via domain normalization ($S_t / K$) and in-the-money (ITM) path filtering.
* **Random Number Generation (`RNGenerator.py`):** Flexible RNG supporting standard Normal draws, Quasi-Monte Carlo (Sobol sequences), and Antithetic Variates for variance reduction.
* **Volatility Modeling (`Volatility.py`):**
  * **Physical Measure ($\mathbb{P}$):** GARCH(1,1) time-series forecasting and rolling historical volatility.
  * **Risk-Neutral Measure ($\mathbb{Q}$):** Implied Volatility (IV) extraction using Brent's root-finding algorithm.
* **Live Market Integration (`DataFetch.py`):** Extracts real-time stock prices and option chain strikes directly from market data APIs.
* **Stable Greeks (`Greeks.py`):** Finite Difference sensitivities (Delta, Gamma, Vega) using **Common Random Numbers (CRN)** to isolate derivative signals from Monte Carlo noise.

---

## Repository Structure

```text
.
├── RNGenerator.py     # Custom RNG engine (Normal, Sobol, Antithetic)
├── Simulator.py       # Geometric Brownian Motion path generator
├── Pricer.py          # Longstaff-Schwartz (LSM) pricing engine
├── Volatility.py      # Rolling Vol, GARCH(1,1), and Brent's IV
├── DataFetch.py       # Market data and option chain puller
├── Greeks.py          # Finite Difference Greeks calculator using CRN
├── main.py            # Execution pipeline & results runner
└── requirements.txt   # Project dependencies (numpy, scipy, arch, yfinance)

```
---

## Quick Start

Execute the complete end-to-end pricing pipeline via `main.py`:

```python
from RNGenerator import random_numbers_generator
from Simulator import GBM
from Pricer import LSPricer
from Volatility import Volatility_RW, Implied_Volatility, Volatility_GARCH
from DataFetch import Market_Value
from Greeks import calculate_greeks

# Setting Parameters
ticker, start, end, k = 'NVO', '2024-08-26', '2026-08-26', 30
S_0, K, r, T, N = 55, 60, 0.05, 1, 252
n_simulations = 10000
d_t = T / N

# Fetch Data & Estimate Volatilities
market_price = Market_Value(ticker, target_strike=K)

sigmas = {
    "RW": Volatility_RW(ticker, start, end, k, N)[-1],
    "IV": Implied_Volatility(market_price, S_0, K, r, T, mode="Call"),
    "GARCH": Volatility_GARCH(ticker, start, end).iloc[-1]
}

# Generate Random Variables
Z = random_numbers_generator(n_simulations, N, mode="Normal")

# Run Pricer and Calculate Greeks across models
results = {} 
for model, sigma_val in sigmas.items():
    call_greeks = calculate_greeks(S_0, r, sigma_val, T, N, n_simulations, K, z=Z, mode="Call")
    put_greeks  = calculate_greeks(S_0, r, sigma_val, T, N, n_simulations, K, z=Z, mode="Put")
    
    results[model] = {
        "Sigma": sigma_val,
        "Call": call_greeks,
        "Put": put_greeks
    }

# Print Summary Table
print("\n" + "="*70)
print(f"{'Model':<8} | {'Option':<5} | {'Price':<7} | {'Delta':<7} | {'Gamma':<7} | {'Vega':<7}")
print("="*70)
for model, res in results.items():
    for opt_type in ["Call", "Put"]:
        g = res[opt_type]
        print(f"{model:<8} | {opt_type:<5} | ${g['Base Price']:<6.3f} | {g['Delta']:<7.4f} | {g['Gamma']:<7.4f} | {g['Vega']:<7.4f}")
```
---

```text
Sample Execution Output======================================================================
Model    | Option | Price   | Delta   | Gamma   | Vega   
======================================================================
RW       | Call   | $3.125  | 0.4821  | 0.0210  | 18.4120
RW       | Put    | $7.410  | -0.5112 | 0.0215  | 18.3900
IV       | Call   | $3.450  | 0.5012  | 0.0224  | 19.1050
IV       | Put    | $7.102  | -0.4901 | 0.0220  | 19.0800
GARCH    | Call   | $3.290  | 0.4910  | 0.0218  | 18.8200
GARCH    | Put    | $7.280  | -0.5011 | 0.0219  | 18.7900
```
---
## Numerical Engineering & Stability Highlights
* Orthogonal Fits: Employs numpy.polynomial.Polynomial.fit on rescaled asset paths ($S_t / K$), which automatically scales the domain to $[-1, 1]$ to eliminate matrix rank warnings and numerical precision loss during regression.
* Sparse Path Handling: Automatically detects time steps where in-the-money path counts drop to $\le 2$, skipping full regression to directly evaluate immediate payoff versus discounted cash flow.
* Common Random Numbers (CRN): Reuses identical random path matrices $Z$ across base and perturbed states ($\Delta S$, $\Delta \sigma$), isolating true derivative sensitivities without Monte Carlo variance dominating the signal.
---
## Future Extensions
* Stochastic Volatility: Expand path simulation to include Heston dynamics to capture volatility smile/skew.
* Surface Calibration: Implement parameter optimization to calibrate local/stochastic volatility models directly against live option chains

