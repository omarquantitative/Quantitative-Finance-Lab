# Quantitative Finance & Derivatives Pricing Lab

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Active-success)

## 📖 Project Overview
This repository contains a suite of quantitative finance models developed in Python. It bridges the gap between theoretical financial engineering and practical implementation.

The library focuses on three core pillars of quantitative finance:
1.  **Stochastic Calculus:** Modeling random market behaviors (Brownian Motion, Mean Reversion).
2.  **Risk Management:** Quantifying portfolio tail risk using matrix algebra (Cholesky Decomposition).
3.  **Numerical Methods:** Solving complex pricing problems where analytical formulas fail (Monte Carlo, Newton-Raphson).

---

## 🛠️ Module Breakdown

### 1. Interest Rate Calibration (Vasicek Model)
**File:** `us_treasury_fair_value_model.py`

#### 🔹 The Concept 
Interest rates do not move randomly forever; they tend to "snap back" to a long-term average, like a rubber band. This model simulates thousands of possible future interest rate paths to determine the "Fair Price" of a Zero Coupon Bond today.

#### 🔸 The Mathematics 
Implements the **Vasicek Ornstein-Uhlenbeck Process** (SDE), defined as:
$$dr_t = a(b - r_t)dt + \sigma dW_t$$

* **$a$ (Speed of Reversion):** How fast rates return to the mean.
* **$b$ (Long Term Mean):** The equilibrium interest rate level.
* **$\sigma$ (Volatility):** The standard deviation of rate changes.

#### 💡 Usage Example
> **Scenario:** The 10-Year Treasury yield is currently **4.20%**, but the long-term historical average is **3.06%**.
> * **Model Action:** Simulates 10,000 paths where rates drift downward over time.
> * **Output:** Calculates a bond price that accounts for this "downward drift" risk, offering a more accurate valuation than simple constant-rate discounting.

---

### 2. Portfolio Risk Engine (VaR & Cholesky)
**File:** `mc_var_portfolio_pricer_corralation.py`

#### 🔹 The Concept 
If you own Apple, Microsoft, and Nvidia, you don't just have 3 random stocks. You have a "Tech Portfolio." If one crashes, the others likely will too. This script calculates the maximum amount you could lose in a month with 95% confidence, while respecting how these stocks move *together*.

#### 🔸 The Mathematics 
To simulate correlated assets, we cannot use simple random numbers. We apply **Cholesky Decomposition** to the Covariance Matrix $\Sigma$:
$$L L^T = \Sigma$$
$$Z_{correlated} = L \cdot Z_{uncorrelated}$$

This transforms standard normal random variables into correlated random variables that preserve the portfolio's "DNA."

#### 💡 Usage Example
> **Input:** Portfolio Value: \$3,000,000 (Equal weight AAPL, MSFT, NVDA).
> **Simulation:** Runs 1,000 "future months."
> **Output:**
> * *Worst Case (5% Cutoff):* \$2,750,000
> * *Value at Risk (VaR):* **\$250,000** (We are 95% sure losses won't exceed this amount).

---

### 3. Numerical Volatility Solver (Inverse BSM)
**File:** `implied_vol_code.py`

#### 🔹 The Concept 
In the option market, we know the Price (e.g., \$5.00), but we don't know the "Implied Volatility" (fear gauge). Since the Black-Scholes formula works forwards (Vol $\to$ Price), we need a special algorithm to work backwards (Price $\to$ Vol) to find out what the market is thinking.

#### 🔸 The Mathematics 
There is no algebraic inverse for the Cumulative Normal Distribution Function ($N(d_1)$). We solve for $\sigma$ numerically using the **Newton-Raphson Method**:
$$\sigma_{n+1} = \sigma_n - \frac{C(\sigma_n) - C_{market}}{\nu(\sigma_n)}$$

Where $\nu$ (Vega) is the derivative of price with respect to volatility.

#### 💡 Usage Example
> **Input:** Call Option Price = \$10.00 | Strike = \$100 | Underlying = \$100.
> **Process:** The script guesses a volatility (e.g., 50%), checks the error, and adjusts using the slope (Vega) until it matches the \$10.00 price perfectly.
> **Output:** Implied Volatility = **18.4%**.

---

### 4. Monte Carlo Option Pricing
**File:** `montecarlo_optionpricer_py.py`

#### 🔹 The Concept 
Sometimes, math formulas are too rigid. Monte Carlo simulation is like running a video game of the stock market 1,000,000 times. We record the profit in every single game, take the average, and discount it back to today. It validates that "The Law of Large Numbers" holds true.

#### 🔸 The Mathematics 
Prices European options under the Risk-Neutral Measure ($\mathbb{Q}$) using Geometric Brownian Motion (GBM):
$$S_T = S_0 \exp\left( (r - \frac{1}{2}\sigma^2)T + \sigma \sqrt{T} Z \right)$$

* **Convergence:** Demonstrates that as $N \to \infty$, $\text{Mean}(Payoff) \to \text{Black-Scholes Price}$.

#### 💡 Usage Example
> **Simulation:** 1,000,000 iterations.
> **Theoretical BSM Price:** \$15.34
> **Simulated Price:** \$15.33
> **Result:** Validates the pricing model with < $0.01 error.

---

## 💻 Tech Stack & Requirements

The project is built entirely in **Python 3.x** and relies on the standard quantitative stack:

* **NumPy:** For high-performance vectorization and matrix operations.
* **SciPy:** For statistical functions (`norm.cdf`, `norm.pdf`).
* **Matplotlib:** For visualizing stochastic paths and probability distributions.
* **YFinance:** For fetching real-time covariance data from Yahoo Finance.

## 🚀 How to Run
1.  Clone the repository.
2.  Install dependencies: `pip install numpy scipy matplotlib yfinance`
3.  Run any script: `python us_treasury_fair_value_model.py`
