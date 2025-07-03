from unittest import TestCase
from unittest.mock import MagicMock, patch
from data_fetchers.yahoo_fetcher import YahooFetcher
import pytest

class TestYahooFetcher(TestCase):
    @patch("data_fetchers.yahoo_fetcher.yf.Ticker")
    def test_fetch_price_from_history(self, mock_ticker):
        mock_history = MagicMock()
        mock_history.empty = False
        mock_history.__getitem__.return_value.iloc.__getitem__.return_value = 150.75

        mock_instance = MagicMock()
        mock_instance.history.return_value = mock_history
        mock_ticker.return_value = mock_instance

        fetcher = YahooFetcher()
        price = fetcher.fetch_ticker_price("AAPL")
        
        assert isinstance(price, float)
        assert price == 150.75

    @patch("data_fetchers.yahoo_fetcher.yf.Ticker")
    def test_fetch_price_from_info(self, mock_ticker):
        mock_history = MagicMock()
        mock_history.empty = True
        mock_instance = MagicMock()
        mock_instance.history.return_value = mock_history
        mock_instance.info = {'currentPrice': 143.22}
        mock_ticker.return_value = mock_instance

        fetcher = YahooFetcher()
        price = fetcher.fetch_ticker_price("GOOGL")
        
        assert isinstance(price, float)
        assert price == 143.22

    @patch("data_fetchers.yahoo_fetcher.yf.Ticker")
    def test_fetch_price_raises_error(self, mock_ticker):
        mock_history = MagicMock()
        mock_history.empty = True
        mock_instance = MagicMock()
        mock_instance.history.return_value = mock_history
        mock_instance.info = {}
        mock_ticker.return_value = mock_instance

        fetcher = YahooFetcher()
        with pytest.raises(ValueError, match="Could not fetch price for ticker: FAKE"):
            fetcher.fetch_ticker_price("FAKE")
