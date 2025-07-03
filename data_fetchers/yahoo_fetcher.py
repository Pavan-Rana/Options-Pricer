from data_fetchers.base_fetcher import BaseFetcher
import yfinance as yf

class YahooFetcher(BaseFetcher):
    """
    Fetches data from Yahoo Finance.
    """

    def __init__(self):
        pass

    def fetch_ticker_price(self, ticker: str) -> float:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if not data.empty:
            last_price = data['Close'].iloc[-1]
            return float(last_price)
        info = stock.info
        price = info.get('currentPrice') or info.get('regularMarketPrice')
        if price is None:
            raise ValueError(f"Could not fetch price for ticker: {ticker}")
        return float(price)