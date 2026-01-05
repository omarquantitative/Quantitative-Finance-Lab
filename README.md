# Quantitative Finance & Derivatives Pricing Lab

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Active-success)

A library of Python implementations focused on Stochastic Calculus, Risk Management, and Numerical Methods in Financial Engineering.

## 1. Interest Rate Modeling (Vasicek Framework)
**Script:** `us_treasury_fair_value_model.py`

* **Core Mathematics:** Implements the **Vasicek Ornstein-Uhlenbeck Process** (SDE) to model mean-reverting interest rate dynamics:
  $$dr_t = a(b - r_t)dt + \sigma dW_t$$
* **Objective:** Calibrate a stochastic rate model against historical 10-Year Treasury (TNX) data to determine fair value for Zero Coupon Bonds.
* **Key Output:** Contrasts "Constant Rate" valuation against "Stochastic Path" valuation (10,000 simulations) to quantify convexity bias and rate volatility risk.

## 2. Portfolio Risk Engine (VaR)
**Script:** `mc_var_portfolio_pricer_corralation.py`

* **Objective:** Compute **Value at Risk (VaR)** and **Expected Shortfall** for a multi-asset technology portfolio (AAPL, MSFT, NVDA).
* **Correlation Preservation:** Utilizes **Cholesky Decomposition** ($L L^T = \Sigma$) to transform uncorrelated random variables into correlated market scenarios, preserving the portfolio's covariance structure ("Market DNA").
* **Risk Metric:** Calculates the 95% Confidence Interval ($1-\alpha$) tail risk over a 30-day forward horizon.

## 3. Numerical Volatility Solver (Inverse BSM)
**Script:** `implied_vol_code.py`

* **Problem Statement:** Extracts Implied Volatility ($\sigma_{imp}$) from observed market prices, treating volatility as the unknown variable in the Black-Scholes-Merton equation.
* **Algorithm:** Implements the **Newton-Raphson Method**, leveraging the option's Vega ($\nu$) sensitivity to iteratively converge on the root volatility with $\epsilon < 1e-5$ precision.

## 4. Derivatives Pricing (Monte Carlo)
**Script:** `montecarlo_optionpricer_py.py`

* **Methodology:** Prices European Call Options via **Geometric Brownian Motion (GBM)** simulations under the Risk-Neutral Measure ($\mathbb{Q}$).
* **Validation:** Demonstrates the **Law of Large Numbers** by converging the simulated mean payoff ($N=1,000,000$) to the analytical Black-Scholes solution.
* **Visualization:** Plots the probability density function (PDF) of terminal asset prices to analyze return distribution skewness.

---

### Tech Stack
* **Core Logic:** `NumPy` (Vectorization), `SciPy` (Statistical Functions)
* **Data & Viz:** `YFinance` (Market Data Feed), `Matplotlib` (Stochastic Path Visualization)
