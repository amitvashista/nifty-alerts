
from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
from .utils import nearest_atm_strike, rr_target
from app.core.indicators import ema, atr
from app.models.objects import Signal, Bar1m, ChainSnapshot

@dataclass
class EmaIvConfig:
    fast: int = 20
    slow: int = 50
    atr_mult_sl: float = 1.2
    rr: float = 1.3

class EmaIvStrategy:
    def __init__(self, cfg: EmaIvConfig | None = None):
        self.cfg = cfg or EmaIvConfig()
        self.df = pd.DataFrame(columns=['open','high','low','close','volume'])

    def on_bar(self, bar: Bar1m, chain: ChainSnapshot) -> list[Signal]:
        # append row
        self.df.loc[bar.ts] = [bar.open, bar.high, bar.low, bar.close, bar.volume]
        if len(self.df) < max(self.cfg.fast, self.cfg.slow) + 2:
            return []

        close = self.df['close']
        ema_fast = ema(close, self.cfg.fast)
        ema_slow = ema(close, self.cfg.slow)

        cross_up = ema_fast.iloc[-2] <= ema_slow.iloc[-2] and ema_fast.iloc[-1] > ema_slow.iloc[-1]
        cross_dn = ema_fast.iloc[-2] >= ema_slow.iloc[-2] and ema_fast.iloc[-1] < ema_slow.iloc[-1]

        # Simple IV/VIX gating
        iv_ok = chain.iv_percentile < 60 and 12 <= chain.vix <= 22

        sigs: list[Signal] = []
        atr14 = atr(self.df, 14).iloc[-1]
        if atr14 is None or pd.isna(atr14):
            return []

        if cross_up and iv_ok:
            strike = nearest_atm_strike(chain.spot)
            sl = max(1.0, bar.close - self.cfg.atr_mult_sl * atr14)
            tgt = rr_target(entry=bar.close, rr=self.cfg.rr, direction="long")
            sigs.append(Signal(
                ts=bar.ts,
                side="BUY_CE",
                reason=f"EMA {self.cfg.fast}>{self.cfg.slow}, IV%ile {chain.iv_percentile:.1f}, VIX {chain.vix:.1f}",
                symbol=f"NIFTY {strike} CE",
                sl=sl, tgt=tgt, rr=self.cfg.rr, confidence=0.65
            ))
        if cross_dn and iv_ok:
            strike = nearest_atm_strike(chain.spot)
            sl = min(bar.close + self.cfg.atr_mult_sl * atr14, bar.close*1.5)
            tgt = rr_target(entry=bar.close, rr=self.cfg.rr, direction="short")
            sigs.append(Signal(
                ts=bar.ts,
                side="BUY_PE",
                reason=f"EMA {self.cfg.fast}<{self.cfg.slow}, IV%ile {chain.iv_percentile:.1f}, VIX {chain.vix:.1f}",
                symbol=f"NIFTY {strike} PE",
                sl=sl, tgt=tgt, rr=self.cfg.rr, confidence=0.65
            ))
        return sigs
