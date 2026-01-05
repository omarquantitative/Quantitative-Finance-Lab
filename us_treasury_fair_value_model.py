import numpy as np
import matplotlib.pyplot as plt

# Configuration
plt.style.use('ggplot')
plt.rcParams['font.size'] = 12
plt.rcParams['figure.figsize'] = (15, 7)

# Bond Parameters
Face_Value = 100
T = 10.0                # Maturity (Years)
N = int(T * 252)        # Daily steps
dt = T / N

# Market Inputs
r0 = 0.0420             # Current Market Yield (4.20%)

# Calibrated Vasicek Parameters
b = 0.0306              # Long-Term Mean (3.06%)
a = 0.3651              # Reversion Speed
sigma = 0.0092          # Volatility
M = 10000               # Number of Simulations

# 1. Constant Rate Valuation (Benchmark)
price_constant = Face_Value * np.exp(-r0 * T)

# 2. Vasicek Stochastic Valuation (Simulation)
rates = np.zeros((N + 1, M))
rates[0] = r0

for t in range(N):
    current_r = rates[t]
    Z = np.random.normal(0, 1, M)
    dr = a * (b - current_r) * dt + sigma * np.sqrt(dt) * Z
    rates[t + 1] = current_r + dr

# Pricing
average_rate_per_path = np.mean(rates, axis=0)
prices_vasicek = Face_Value * np.exp(-average_rate_per_path * T)
price_vasicek_final = np.mean(prices_vasicek)

# Reporting
print(f"--- FAIR VALUE ESTIMATION ---")
print(f"Market Reality: Rates start at {r0:.2%} and revert to {b:.2%}")
print(f"-" * 50)
print(f"Constant Model:   ${price_constant:.2f}")
print(f"Vasicek Model:    ${price_vasicek_final:.2f}")
print(f"Alpha (Edge):     ${price_vasicek_final - price_constant:.2f}")
print(f"-" * 50)

# Visualization
fig, (ax1, ax2) = plt.subplots(1, 2)

# Rate Trajectories
ax1.plot(rates[:, :100], color='cornflowerblue', alpha=0.3, lw=1)
ax1.axhline(r0, color='firebrick', linestyle='-', linewidth=2, label=f'Start ({r0:.2%})')
ax1.axhline(b, color='forestgreen', linestyle='--', linewidth=2, label=f'Mean ({b:.2%})')
ax1.set_title(f"Interest Rate Projection ({T} Years)", fontweight='bold')
ax1.legend()

# Price Distribution
ax2.hist(prices_vasicek, bins=50, color='rebeccapurple', alpha=0.7, edgecolor='white')
ax2.axvline(price_constant, color='firebrick', linewidth=3, linestyle='--', label='Constant')
ax2.axvline(price_vasicek_final, color='gold', linewidth=3, linestyle='-', label='Vasicek')
ax2.set_title(f"Fair Value Distribution", fontweight='bold')
ax2.legend()

plt.tight_layout()
plt.show()