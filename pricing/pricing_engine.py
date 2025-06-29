from pricing.black_scholes import BlackScholesStrategy
# from pricing.monte_carlo import MonteCarloStrategy
from data_fetchers.yahoo_fetcher import YahooFetcher

class PricingEngine:
    def __init__(self):
        """Only current model is Black-Scholes."""
        self.strategies = {
            'Black-Scholes': BlackScholesStrategy(),
        }
        self.data_provider = YahooFetcher()

    def calculate_call(self, option, volatility: float, risk_free_rate: float, spot=None):
        """Calculate price & Greeks for an option using the specified model."""
        strategy = self.strategies['Black-Scholes']
        if spot is None:
            spot = self.data_provider.fetch_data(option.underlying_symbol)
        call_result = strategy.calculate_call_values(option, spot, volatility, risk_free_rate)
        return call_result
    
    def calculate_put(self, option, volatility: float, risk_free_rate: float, spot=None):
        """Calculate price & Greeks for an option using the specified model."""
        strategy = self.strategies['Black-Scholes']
        if spot is None:
            spot = self.data_provider.fetch_data(option.underlying_symbol)
        put_result = strategy.calculate_put_values(option, spot, volatility, risk_free_rate)
        return put_result