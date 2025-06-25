from datetime import date
from dataclasses import dataclass

@dataclass
class Option:
    underlying_symbol: str
    strike_price: float
    expiration_date: date
    option_type: str  # 'call' or 'put'

    def time_to_expiration(self, today: date = date.today()) -> float:
        """
        Calculate the time to expiration in years.
        """
        days = (self.expiration_date - today).days
        return days / 365.0