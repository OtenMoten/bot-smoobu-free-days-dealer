from dataclasses import dataclass
from datetime import datetime


@dataclass
class ColorScheme:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"


@dataclass
class DateRange:
    start: datetime
    end: datetime


@dataclass
class Event:
    date: datetime
    type: str
    guest_name: str
    guest_email: str
    free_days: int
    price: float
    offer_price: float
