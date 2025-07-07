import pytest
from pricing.black_scholes import BlackScholesStrategy
from math import isclose
from datetime import datetime, timedelta

class DummyOption:
    def __init__(self, strike_price, expiry_days=30):
        self.strike_price = strike_price
        self.expiry_date = datetime.now() + timedelta(days=expiry_days)

    def time_to_expiration(self):
        return (self.expiry_date - datetime.now()).days / 365.0

@pytest.fixture
def strategy():
    return BlackScholesStrategy()

@pytest.mark.parametrize("is_call", [True, False])
def test_option_pricing(strategy, is_call):
    option = DummyOption(strike_price=100)
    spot = 105
    vol = 0.2
    rate = 0.01

    if is_call:
        result = strategy.calculate_call_values(option, spot, vol, rate)
    else:
        result = strategy.calculate_put_values(option, spot, vol, rate)

    # Ensure basic keys are present
    for greek in ["price", "delta", "gamma", "vega", "theta", "rho"]:
        assert greek in result
        assert isinstance(result[greek], float)

    # Simple sanity checks
    assert result["price"] > 0
    assert result["gamma"] >= 0
    assert result["vega"] >= 0

def test_expired_option_returns_zero(strategy):
    option = DummyOption(strike_price=100, expiry_days=-1)
    spot = 100
    vol = 0.2
    rate = 0.01

    call_result = strategy.calculate_call_values(option, spot, vol, rate)
    put_result = strategy.calculate_put_values(option, spot, vol, rate)

    for greek in call_result:
        assert isclose(call_result[greek], 0.0)
        assert isclose(put_result[greek], 0.0)

def test_internal_derivative_and_common_factor_calculation(strategy):
    S, K, r, sigma, T = 100, 100, 0.05, 0.2, 1
    d1, d2 = strategy.calculate_derivatives(S, K, r, sigma, T)
    N_d1, N_d2, n_d1 = strategy.calculate_common_factors(d1, d2)

    assert d1 > d2
    assert 0 < N_d1 < 1
    assert 0 < N_d2 < 1
    assert n_d1 > 0
