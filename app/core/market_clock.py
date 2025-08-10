
from datetime import datetime, time
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

def is_market_open(now: datetime | None = None) -> bool:
    now = now or datetime.now(IST)
    # NSE regular hours 09:15–15:30 IST, Mon–Fri (basic; no holiday calendar here)
    if now.weekday() >= 5:
        return False
    start = time(9, 15, tzinfo=IST)
    end = time(15, 30, tzinfo=IST)
    return start <= now.timetz() <= end
