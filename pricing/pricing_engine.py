from pricing.black_scholes import BlackScholesStrategy
# from pricing.monte_carlo import MonteCarloStrategy
from data_fetchers.yahoo_fetcher import YahooFetcher

class PricingEngine:
    def __init__(self):
        self.strategies = {
            'Black-Scholes': BlackScholesStrategy(),
            #'Monte-Carlo': MonteCarloStrategy(num_paths=10000)
        }
        self.data_provider = YahooFetcher()

    def calculate(self, option, model_name: str, volatility: float, risk_free_rate: float):
        """Calculate price & Greeks for an option using the specified model."""
        if model_name not in self.strategies:
            raise ValueError(f"Unknown pricing model: {model_name}")
        strategy = self.strategies[model_name]
        spot = self.data_provider.fetch_data(option.underlying_symbol)
        result = strategy.calculate(option, spot, volatility, risk_free_rate)
        return result