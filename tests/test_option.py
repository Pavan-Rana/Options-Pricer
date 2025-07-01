from domain.option import Option
import pytest

class TestOptions(pytest):
    def test_option_initialization(self):
        option = Option("AAPL", 150, "2023-12-31")
        assert option.underlying_symbol == "AAPL"
        assert option.strike_price == 150
        assert option.expiration_date == "2023-12-31"