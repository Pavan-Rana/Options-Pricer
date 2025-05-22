from math import log, sqrt, exp
from scipy.stats import norm
from .strategy_base import StrategyBase

class BlackScholesPricer(StrategyBase):
    """
    Black-Scholes option pricing model for European options.
    This class calculates the price of European call and put options using the Black-Scholes formula.
    """
    def __init__(self, S, K, T, r, sigma):
        self.S = S  # Current stock price
        self.K = K  # Option strike price
        self.T = T  # Time to expiration in years
        self.r = r  # Risk-free interest rate
        self.sigma = sigma  # Volatility of the underlying stock

    def d1(self):
        return (log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * sqrt(self.T))

    def d2(self):
        return self.d1() - self.sigma * sqrt(self.T)

    def call_price(self):
        return (self.S * norm.cdf(self.d1()) - self.K * exp(-self.r * self.T) * norm.cdf(self.d2()))

    def put_price(self):
        return (self.K * exp(-self.r * self.T) * norm.cdf(-self.d2()) - self.S * norm.cdf(-self.d1()))