import abc
from domain.option import Option

class PricingStrategy(abc.ABC):
    """
    Base class for pricing
    """
    @abc.abstractmethod
    def calculate(self, option: Option, spot_price: float,
                  volatility: float, risk_free_rate: float) -> dict:
        """
        Calculate the price of the option.

        :param option: The option to price.
        :param spot_price: The current spot price of the underlying asset.
        :param volatility: The volatility of the underlying asset.
        :param risk_free_rate: The risk-free interest rate.
        :return: A dictionary containing the calculated price and other relevant data.
        """
        pass