from domain.option import Option
from datetime import date
from unittest import TestCase

class TestOption(TestCase):
    def test_option_init(self):
        test_option = Option(underlying_symbol="AAPL", strike_price=100, expiration_date="2025-07-03")
        self.assertEqual(test_option.underlying_symbol, "AAPL")
        self.assertEqual(test_option.strike_price, 100)
        self.assertEqual(test_option.expiration_date, "2025-07-03")
    
    def test_time_to_expiration(self):
        test_option = Option(underlying_symbol="AAPL", strike_price=100, expiration_date=date.today())
        self.assertEqual(test_option.time_to_expiration(), 0)
    