import pytest
from pricing.black_scholes import BlackScholesStrategy
from math import isclose
from datetime import datetime, timedelta
from unittest import TestCase

class DummyOption:
    def __init__(self, strike_price, expiry_days=30):
        self.strike_price = strike_price
        self.expiry_date = datetime.now() + timedelta(days=expiry_days)

    def time_to_expiration(self):
        return max(0, (self.expiry_date - datetime.now()).days / 365.0)

class TestBlackScholes(TestCase):
    def setUp(self):  # Fixed: was setup_method()
        self.strategy = BlackScholesStrategy()

    def test_call_option_pricing(self):
        option = DummyOption(strike_price=100)
        spot = 105
        vol = 0.2
        rate = 0.01

        result = self.strategy.calculate_call_values(option, spot, vol, rate)

        for greek in ["price", "delta", "gamma", "vega", "theta", "rho"]:
            self.assertIn(greek, result)
            self.assertIsInstance(result[greek], float)

        self.assertGreater(result["price"], 0)
        self.assertGreaterEqual(result["gamma"], 0)
        self.assertGreaterEqual(result["vega"], 0)

    def test_put_option_pricing(self):
        option = DummyOption(strike_price=100)
        spot = 105
        vol = 0.2
        rate = 0.01

        result = self.strategy.calculate_put_values(option, spot, vol, rate)

        for greek in ["price", "delta", "gamma", "vega", "theta", "rho"]:
            self.assertIn(greek, result)
            self.assertIsInstance(result[greek], float)

        self.assertGreater(result["price"], 0)
        self.assertGreaterEqual(result["gamma"], 0)
        self.assertGreaterEqual(result["vega"], 0)

    def test_expired_option_returns_zero(self):
        option = DummyOption(strike_price=100, expiry_days=-1)
        spot = 100
        vol = 0.2
        rate = 0.01

        call_result = self.strategy.calculate_call_values(option, spot, vol, rate)
        put_result = self.strategy.calculate_put_values(option, spot, vol, rate)

        for greek in call_result:
            self.assertTrue(isclose(call_result[greek], 0.0))
            self.assertTrue(isclose(put_result[greek], 0.0))

    def test_internal_derivative_and_common_factor_calculation(self):
        S, K, r, sigma, T = 100, 100, 0.05, 0.2, 1
        d1, d2 = self.strategy.calculate_derivatives(S, K, r, sigma, T)
        N_d1, N_d2, n_d1 = self.strategy.calculate_common_factors(d1, d2)

        self.assertGreater(d1, d2)
        self.assertGreater(N_d1, 0)
        self.assertLess(N_d1, 1)
        self.assertGreater(N_d2, 0)
        self.assertLess(N_d2, 1)
        self.assertGreater(n_d1, 0)