
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional

Side = Literal["BUY_CE", "BUY_PE", "SELL_CE", "SELL_PE", "NONE"]

@dataclass
class Bar1m:
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0

@dataclass
class ChainSnapshot:
    ts: datetime
    spot: float
    vix: float
    iv_percentile: float  # 0..100 for ATM bucket (placeholder)
    pcr: float  # Put/Call ratio (placeholder)

@dataclass
class Signal:
    ts: datetime
    side: Side
    reason: str
    symbol: str
    sl: Optional[float] = None
    tgt: Optional[float] = None
    rr: Optional[float] = None
    confidence: float = 0.5
