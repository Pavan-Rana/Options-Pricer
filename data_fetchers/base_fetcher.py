import abc

class BaseFetcher(abc.ABC):
    """
    Base class for data fetchers.
    """

    def __init__(self, symbol: str):
        self.symbol = symbol

    def fetch_ticker_price(self):
        """
        Fetch data for the given symbol.
        """
        raise NotImplementedError("Subclasses should implement this method.")