import numpy as np
import matplotlib.pyplot as plt

# Model Parameters
S = 1000        # Asset Price
K = 850         # Strike Price
T = 7.0         # Time to Maturity (Years)
r = 0.03        # Risk-free Rate
sigma = 0.05    # Volatility
M = 1000000     # Simulations

# Simulation Engine
dt = T
nudt = (r - 0.5 * sigma**2) * dt
volsdt = sigma * np.sqrt(dt)
Z = np.random.normal(0, 1, M)

# Geometric Brownian Motion
lnSt = np.log(S) + nudt + (volsdt * Z)
ST = np.exp(lnSt)

# Payoff & Pricing
payoffs = np.maximum(ST - K, 0)
price = np.mean(payoffs) * np.exp(-r * T)

# Visualization Logic
plt.figure(figsize=(14, 6))

# Subplot 1: Path Visuals
plt.subplot(1, 2, 1)
steps = 100
dt_graph = T / steps
paths_to_show = 50
price_paths = np.zeros((steps + 1, paths_to_show))
price_paths[0] = S

for t in range(1, steps + 1):
    z_graph = np.random.normal(0, 1, paths_to_show)
    price_paths[t] = price_paths[t-1] * np.exp((r - 0.5 * sigma**2)*dt_graph + sigma * np.sqrt(dt_graph) * z_graph)

plt.plot(price_paths, lw=1.5, alpha=0.7)
plt.axhline(K, color='black', linestyle='--', linewidth=2, label=f'Strike (${K})')
plt.title(f'Monte Carlo Simulation ({paths_to_show} Paths)')
plt.xlabel('Time Steps')
plt.ylabel('Asset Price')
plt.legend()

# Subplot 2: Distribution
plt.subplot(1, 2, 2)
plt.hist(ST, bins=50, color='#1f77b4', edgecolor='white', alpha=0.8)
plt.axvline(K, color='black', linestyle='--', linewidth=2, label=f'Strike (${K})')
plt.title(f'Final Price Distribution')
plt.xlabel('Price at Maturity')
plt.ylabel('Frequency')
plt.legend()

plt.tight_layout()
plt.show()

# Verification & Reporting
theoretical_mean = S * np.exp(r * T)
simulated_mean = np.mean(ST)

print(f"-" * 40)
print(f"OPTION PRICING REPORT")
print(f"-" * 40)
print(f"Fair Option Price:      ${price:.2f}")
print(f"-" * 40)
print(f"Theoretical Mean:       ${theoretical_mean:.2f}")
print(f"Simulated Mean:         ${simulated_mean:.2f}")
print(f"Approximation Error:    ${abs(theoretical_mean - simulated_mean):.2f}")
print(f"-" * 40)