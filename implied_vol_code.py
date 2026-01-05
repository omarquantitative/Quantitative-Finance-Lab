import numpy as np
from scipy.stats import norm

# ==========================================
#        IMPLIED VOLATILITY ENGINE
# ==========================================

def bs_price(S, K, T, r, sigma, option_type='call'):
    """Calculates Black-Scholes Price"""
    if sigma <= 0: return max(0, S - K) if option_type == 'call' else max(0, K - S)
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if option_type == 'call':
        return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    return K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)

def bs_vega(S, K, T, r, sigma):
    """Calculates Vega"""
    if sigma <= 0: return 0
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T)

def get_implied_volatility(target_price, S, K, T, r, option_type='call'):
    """Newton-Raphson Solver for IV"""
    sigma = 0.5
    for _ in range(100):
        price = bs_price(S, K, T, r, sigma, option_type)
        diff = target_price - price

        if abs(diff) < 1e-5: return sigma

        vega = bs_vega(S, K, T, r, sigma)
        if vega < 1e-8: break

        sigma += diff / vega
    return None

# ==========================================
#             TESTING AREA
# ==========================================
if __name__ == "__main__":

    # --- 1. PARAMETERS (EDIT HERE) ---
    MARKET_PRICE = 10.00
    STOCK_PRICE  = 100
    STRIKE_PRICE = 100
    TIME_YEARS   = 1
    RISK_FREE    = 0.0

    # --- 2. CALCULATION ---
    iv = get_implied_volatility(MARKET_PRICE, STOCK_PRICE, STRIKE_PRICE, TIME_YEARS, RISK_FREE)

    # --- 3. RESULT ---
    if iv:
        print(f"Market Price:   ${MARKET_PRICE:.2f}")
        print(f"Implied Vol:    {iv:.2%}")

        # Verification Check (Clean)
        check_price = bs_price(STOCK_PRICE, STRIKE_PRICE, TIME_YEARS, RISK_FREE, iv)
        print(f"Check Math:     ${check_price:.2f}")
    else:
        print("Error: Could not calculate IV.")