import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# --- 1. USER SETTINGS (The Control Panel) ---
TICKERS = ['AAPL', 'MSFT', 'NVDA']  # The portfolio stocks
INITIAL_INVESTMENT = 1_000_000      # Investment per stock ($)
SIMULATION_DAYS = 30                # How many days into the future?
N_SIMULATIONS = 1000                # How many "universes" to simulate?
CONFIDENCE_LEVEL = 0.05             # 5% Risk Level (95% Confidence)

# --- 2. DATA The results and the Correlation Matrix & DNA Relationships of Daily Return Corraltion  ---
print(f"Fetching data for {TICKERS}...")
data = yf.download(TICKERS, start="2024-01-01", end="2025-01-01")['Close']
returns = data.pct_change().dropna()

# Calculate Market DNA
mean_returns = returns.mean().values
std_devs = returns.std().values
corr_matrix = returns.corr().values
last_prices = data.iloc[-1].values

# The Cholesky Filter
L = np.linalg.cholesky(corr_matrix)

# --- 3. MONTE CARLO SIMULATION ---
print(f"Simulating {N_SIMULATIONS} market scenarios...")
final_portfolio_values = []

total_investment = INITIAL_INVESTMENT * len(TICKERS)

for i in range(N_SIMULATIONS):
    # A. Generate Random Noise
    uncorrelated_noise = np.random.normal(0, 1, (len(TICKERS), SIMULATION_DAYS))

    # B. Apply Cholesky (Force Correlation)
    correlated_noise = np.dot(L, uncorrelated_noise)

    # C. Calculate Price Paths
    simulated_returns = mean_returns.reshape(-1, 1) + (std_devs.reshape(-1, 1) * correlated_noise)
    price_paths = last_prices.reshape(-1, 1) * np.cumprod(1 + simulated_returns, axis=1)

    # D. Portfolio Value at End
    shares_owned = INITIAL_INVESTMENT / last_prices
    final_prices = price_paths[:, -1]
    total_value = np.sum(final_prices * shares_owned)
    final_portfolio_values.append(total_value)

# --- 4. RISK REPORT ---
sorted_values = np.sort(final_portfolio_values)
cutoff_index = int(N_SIMULATIONS * CONFIDENCE_LEVEL)
worst_case_value = sorted_values[cutoff_index]
VaR = total_investment - worst_case_value

print("\n" + "="*30)
print("   PORTFOLIO RISK REPORT")
print("="*30)
print(f"Total Invested:   ${total_investment:,.2f}")
print(f"Worst Case (5%):  ${worst_case_value:,.2f}")
print(f"Value at Risk:    ${VaR:,.2f}")
print("-" * 30)
print(f"INTERPRETATION: You are 95% confident that")
print(f"losses will not exceed ${VaR:,.2f} over {SIMULATION_DAYS} days.")
print("="*30)

# Visualization
plt.figure(figsize=(10, 6))
plt.hist(final_portfolio_values, bins=50, color='#1f77b4', edgecolor='black', alpha=0.7)
plt.axvline(worst_case_value, color='red', linestyle='dashed', linewidth=2, label=f'VaR Cutoff (${worst_case_value/1e6:.2f}M)')
plt.title(f"Monte Carlo VaR: 30-Day Forecast ({N_SIMULATIONS} Sims)")
plt.xlabel("Portfolio Value ($)")
plt.ylabel("Frequency")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()