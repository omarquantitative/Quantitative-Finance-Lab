# Quantitative Finance & Derivatives Pricing Lab

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Active-success)

## 📖 Project Abstract
This repository houses a suite of Python-based financial models designed to address core problems in asset pricing, risk management, and stochastic calculus. The library moves beyond theoretical derivation, providing executable engines for:
* **Stochastic Interest Rate Calibration** (Vasicek Framework)
* **Multivariate Risk Analysis** (Monte Carlo VaR with Cholesky Decomposition)
* **Numerical Volatility Extraction** (Inverse Black-Scholes Solvers)
* **Path-Dependent Derivatives Pricing** (Geometric Brownian Motion)

---

## 🛠️ Model Architecture

### 1. Interest Rate Calibration (Vasicek Model)
**Script:** `us_treasury_fair_value_model.py`

**Objective:**
To quantify the "convexity bias" in bond pricing by comparing deterministic valuation (Constant Rate) against a stochastic mean-reverting framework.

**Mathematical Framework:**
The model implements the **Vasicek Ornstein-Uhlenbeck Process**, defined by the Stochastic Differential Equation (SDE):
$$dr_t = a(b - r_t)dt + \sigma dW_t$$

* $a$: Speed of mean reversion (calibrated to historical yield curve dynamics).
* $b$: Long-term equilibrium interest rate.
* $\sigma$: Instantaneous volatility of rate changes.

**Implementation Logic:**
* **Calibration:** Parameters are tuned to mimic the historical volatility and reversion characteristics of the 10-Year US Treasury Note (TNX).
* **Simulation:** Generates 10,000 discrete rate paths using Euler-Maruyama discretization.
* **Valuation:** Discounts Zero Coupon Bond (ZCB) cash flows along each stochastic path to derive a risk-adjusted Fair Value.

---

### 2. Portfolio Risk Engine (VaR & Correlation)
**Script:** `mc_var_portfolio_pricer_corralation.py`

**Objective:**
To calculate **Value at Risk (VaR)** and **Expected Shortfall (ES)** for a multi-asset technology portfolio (AAPL, MSFT, NVDA), ensuring that cross-asset correlations are preserved during stress testing.

**Mathematical Framework:**
To generate correlated market scenarios from uncorrelated random noise ($Z$), we apply **Cholesky Decomposition** to the covariance matrix $\Sigma$:
$$L L^T = \Sigma$$
$$Z_{correlated} = L \cdot Z_{uncorrelated}$$

**Implementation Logic:**
* **Data Ingestion:** Dynamically fetches historical adjusted close prices via `yfinance` to construct the rolling covariance matrix.
* **Matrix Algebra:** Decomposes the covariance structure to ensure simulated price paths respect the historical "coupling" of asset returns.
* **Risk Metric:** Computes the 95% Confidence Interval ($1-\alpha$) tail risk over a 30-day forward horizon.

---

### 3. Numerical Volatility Solver (Inverse BSM)
**Script:** `implied_vol_code.py`

**Objective:**
To extract **Implied Volatility (IV)** from observed market option prices. Since the Black-Scholes equation is not algebraically invertible, this script treats volatility as an optimization problem.

**Mathematical Framework:**
We solve for the root $\sigma$ where $C_{model}(\sigma) - C_{market} = 0$ using the **Newton-Raphson Method**:
$$\sigma_{n+1} = \sigma_n - \frac{C(\sigma_n) - C_{market}}{\nu(\sigma_n)}$$

* $\nu(\sigma_n)$: The option's Vega (sensitivity of price to volatility).

**Implementation Logic:**
* **Optimization:** Iteratively adjusts the volatility guess based on the gradient (Vega) until the model price converges to the market price.
* **Precision:** Enforces a strict convergence tolerance ($\epsilon < 1e-5$) to ensure pricing accuracy within one cent.

---

### 4. Monte Carlo Option Pricing
**Script:** `montecarlo_optionpricer_py.py`

**Objective:**
To validate analytical pricing formulas using numerical simulation. This module prices European Options under the **Risk-Neutral Measure ($\mathbb{Q}$)**.

**Mathematical Framework:**
Asset prices are modeled using **Geometric Brownian Motion (GBM)**:
$$S_T = S_0 \exp\left( (r - \frac{1}{2}\sigma^2)T + \sigma \sqrt{T} Z \right)$$

**Implementation Logic:**
* **Law of Large Numbers:** Demonstrates that as $N \to \infty$ (1,000,000 iterations), the simulated mean payoff converges to the analytical Black-Scholes price.
* **Distribution Analysis:** Visualizes the probability density function (PDF) of terminal asset prices to analyze the skewness and kurtosis of log-normal returns.

---

## 💻 Tech Stack & Dependencies

The laboratory is built on the standard Python quantitative stack:

* **NumPy:** High-performance vectorization and linear algebra (Cholesky, Dot Products).
* **SciPy:** Statistical functions for Cumulative Distribution Functions (`norm.cdf`) and Probability Density Functions (`norm.pdf`).
* **Matplotlib:** Visualization of stochastic paths and Monte Carlo distributions.
* **YFinance:** API integration for real-time market data ingestion.

## 🚀 Execution Guide
```bash
# 1. Clone the repository
git clone [https://github.com/YOUR_USERNAME/Quantitative-Finance-Lab.git](https://github.com/YOUR_USERNAME/Quantitative-Finance-Lab.git)

# 2. Install required libraries
pip install numpy scipy matplotlib yfinance

# 3. Run a model (e.g., Vasicek Interest Rates)
python us_treasury_fair_value_model.py
