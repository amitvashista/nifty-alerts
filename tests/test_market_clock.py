from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.market_clock import is_market_open

IST = ZoneInfo("Asia/Kolkata")


def test_is_market_open_during_hours():
    dt = datetime(2023, 6, 5, 10, 0, tzinfo=IST)  # Monday
    assert is_market_open(dt) is True


def test_is_market_open_weekend():
    dt = datetime(2023, 6, 3, 10, 0, tzinfo=IST)  # Saturday
    assert is_market_open(dt) is False


def test_is_market_open_after_hours():
    dt = datetime(2023, 6, 5, 16, 0, tzinfo=IST)  # Monday after close
    assert is_market_open(dt) is False
