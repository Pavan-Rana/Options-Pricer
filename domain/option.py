from datetime import date
from dataclasses import dataclass

@dataclass
class Option:
    underlying_symbol: str
    strike_price: float
    expiration_date: date

    def time_to_expiration(self, today: date = None) -> float:
        """
        Calculate the time to expiration in years.
        """
        if today is None:
            today = date.today()
        days = (self.expiration_date - today).days
        return days / 365.0