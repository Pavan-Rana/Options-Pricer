from base_fetcher import BaseFetcher
import yfinance as yf
from datetime import datetime
import pandas as pd

class YahooFetcher(BaseFetcher):
    """
    Fetches data from Yahoo Finance.
    """

    def __init__(self, symbol: str):
        super().__init__(symbol)

    def fetch_data(self):
        """
        Fetch data for the given symbol.
        """
        data = yf.download(self.symbol, start="2020-01-01", end=datetime.now().strftime("%Y-%m-%d"))
        
        df = pd.DataFrame(data)
        
        df.reset_index(inplace=True)
        
        return df