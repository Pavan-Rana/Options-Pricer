from math import log, sqrt, exp
from scipy.stats import norm
from pricing.strategy_base import PricingStrategy

class BlackScholesStrategy(PricingStrategy):
    def calculate(self, option, option_type: str, spot_price: float, volatility: float, risk_free_rate: float) -> dict:
        """
        Calculate the price of the option using the Black-Scholes formula.

        :param option: The option to price.
        :param option_type: 'call' or 'put'

        :param spot_price: The current spot price of the underlying asset.
        :param volatility: The volatility of the underlying asset.
        :param risk_free_rate: The risk-free interest rate.
        :return: A dictionary containing the calculated price and other relevant data.
        """
        T = option.time_to_expiration()
        if T <= 0:
            return {"price": 0.0, "delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0}
        S, K, r, sigma = spot_price, option.strike_price, risk_free_rate, volatility
        # Calculate d1 and d2
        d1 = (log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)
        # Calculate common factors
        N_d1, N_d2 = norm.cdf(d1), norm.cdf(d2)
        n_d1 = norm.pdf(d1) # Probability density function of d1 for Greeks
        # Calculate option price and Greeks
        if option_type == 'call':
            price = S * N_d1 - K * exp(-r * T) * N_d2
            delta = N_d1
            theta = -(S * n_d1 * sigma) / (2 * sqrt(T)) - r * K * exp(-r * T) * N_d2
            rho = K * T * exp(-r * T) * N_d2
        else:
            price = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
            delta = N_d1 - 1.0
            theta = -(S * n_d1 * sigma) / (2 * sqrt(T)) + r * K * exp(-r * T) * norm.cdf(-d2)
            rho = -K * T * exp(-r * T) * norm.cdf(-d2)
        gamma = n_d1 / (S * sigma * sqrt(T))
        vega = S * n_d1 * sqrt(T) / 100 # Convert to per 1% change in volatility
        theta /= 365  # Convert to per day
        return {
            "price": price,
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho
        }