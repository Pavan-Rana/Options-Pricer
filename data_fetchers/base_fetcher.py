import abc

class BaseFetcher(abc.ABC):
    """
    Base class for data fetchers.
    """

    def __init__(self, symbol: str):
        pass

    def fetch_ticker_price(self, symbol: str):
        """
        Fetch data for the given symbol.
        """
        raise NotImplementedError("Subclasses should implement this method.")