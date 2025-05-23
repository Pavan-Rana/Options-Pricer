class BaseFetcher:
    """
    Base class for data fetchers.
    """

    def __init__(self, symbol: str):
        self.symbol = symbol

    def fetch_data(self):
        """
        Fetch data for the given symbol.
        """
        raise NotImplementedError("Subclasses should implement this method.")