import pytest
from unittest.mock import patch
from pricing.pricing_engine import PricingEngine

class DummyOption:
    def __init__(self, underlying_symbol):
        self.underlying_symbol = underlying_symbol

class TestPricingEngine:
    def setup_method(self):
        self.engine = PricingEngine()

    def test_calculate_call_with_provided_spot(self):
        option = DummyOption("AAPL")
        volatility = 0.2
        rate = 0.01
        spot = 150.0
        expected_result = {"price": 10, "delta": 0.5}

        with patch.object(self.engine.strategies['Black-Scholes'], 'calculate_call_values', return_value=expected_result) as mock_calc:
            result = self.engine.calculate_call(option, volatility, rate, spot)
            mock_calc.assert_called_once_with(option, spot, volatility, rate)
            assert result == expected_result

    def test_calculate_call_without_spot(self):
        option = DummyOption("AAPL")
        volatility = 0.2
        rate = 0.01
        fetched_spot = 145.0
        expected_result = {"price": 12, "delta": 0.6}

        with patch.object(self.engine.data_provider, 'fetch_ticker_price', return_value=fetched_spot) as mock_fetch, \
            patch.object(self.engine.strategies['Black-Scholes'], 'calculate_call_values', return_value=expected_result) as mock_calc:
            result = self.engine.calculate_call(option, volatility, rate)
            mock_fetch.assert_called_once_with("AAPL")
            mock_calc.assert_called_once_with(option, fetched_spot, volatility, rate)
            assert result == expected_result

    def test_calculate_put_with_provided_spot(self):
        option = DummyOption("GOOG")
        volatility = 0.3
        rate = 0.015
        spot = 120.0
        expected_result = {"price": 8, "delta": -0.4}

        with patch.object(self.engine.strategies['Black-Scholes'], 'calculate_put_values', return_value=expected_result) as mock_calc:
            result = self.engine.calculate_put(option, volatility, rate, spot)
            mock_calc.assert_called_once_with(option, spot, volatility, rate)
            assert result == expected_result

    def test_calculate_put_without_spot(self):
        option = DummyOption("TSLA")
        volatility = 0.25
        rate = 0.02
        fetched_spot = 700.0
        expected_result = {"price": 20, "delta": -0.5}

        with patch.object(self.engine.data_provider, 'fetch_ticker_price', return_value=fetched_spot) as mock_fetch, \
            patch.object(self.engine.strategies['Black-Scholes'], 'calculate_put_values', return_value=expected_result) as mock_calc:
            result = self.engine.calculate_put(option, volatility, rate)
            mock_fetch.assert_called_once_with("TSLA")
            mock_calc.assert_called_once_with(option, fetched_spot, volatility, rate)
            assert result == expected_result
