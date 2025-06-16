class BaseStrategy:
    """
    Base class for option pricing strategies.
    """

    def __init__(self, underlying_price: float, strike_price: float, risk_free_rate: float, time_to_maturity: float):
        self.underlying_price = underlying_price
        self.strike_price = strike_price
        self.risk_free_rate = risk_free_rate
        self.time_to_maturity = time_to_maturity

    def call_price(self) -> float:
        """
        Calculate the call option price.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    def put_price(self) -> float:
        """
        Calculate the put option price.
        """
        raise NotImplementedError("Subclasses should implement this method.")