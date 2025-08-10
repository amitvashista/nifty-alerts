
from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
from app.core.indicators import vwap, atr
from .utils import nearest_atm_strike, rr_target
from app.models.objects import Signal, Bar1m, ChainSnapshot

@dataclass
class VwapMrConfig:
    band_bps: int = 25  # 25 bps from VWAP
    rsi_len: int = 3  # placeholder, not used without RSI calc
    rr: float = 1.2
    atr_mult_sl: float = 1.0

class VwapMrStrategy:
    def __init__(self, cfg: VwapMrConfig | None = None):
        self.cfg = cfg or VwapMrConfig()
        self.df = pd.DataFrame(columns=['open','high','low','close','volume'])

    def on_bar(self, bar: Bar1m, chain: ChainSnapshot) -> list[Signal]:
        self.df.loc[bar.ts] = [bar.open, bar.high, bar.low, bar.close, bar.volume]
        if len(self.df) < 20:
            return []

        df = self.df.copy()
        vw = vwap(df).iloc[-1]
        price = df['close'].iloc[-1]
        dist_bps = (price - vw) / vw * 10000.0

        atr14 = atr(df, 14).iloc[-1]
        if pd.isna(atr14):
            return []

        sigs: list[Signal] = []

        # Bounce above VWAP
        if dist_bps < -self.cfg.band_bps and chain.pcr < 1.1:
            strike = nearest_atm_strike(chain.spot)
            sl = price - self.cfg.atr_mult_sl * atr14
            tgt = rr_target(price, self.cfg.rr, "long")
            sigs.append(Signal(
                ts=bar.ts, side="BUY_CE",
                reason=f"Price {dist_bps:.0f}bps below VWAP; PCR {chain.pcr:.2f}",
                symbol=f"NIFTY {strike} CE",
                sl=sl, tgt=tgt, rr=self.cfg.rr, confidence=0.55
            ))

        # Revert downward to VWAP
        if dist_bps > self.cfg.band_bps and chain.pcr > 0.9:
            strike = nearest_atm_strike(chain.spot)
            sl = price + self.cfg.atr_mult_sl * atr14
            tgt = rr_target(price, self.cfg.rr, "short")
            sigs.append(Signal(
                ts=bar.ts, side="BUY_PE",
                reason=f"Price {dist_bps:.0f}bps above VWAP; PCR {chain.pcr:.2f}",
                symbol=f"NIFTY {strike} PE",
                sl=sl, tgt=tgt, rr=self.cfg.rr, confidence=0.55
            ))
        return sigs
