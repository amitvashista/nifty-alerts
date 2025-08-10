
from __future__ import annotations
from typing import Iterable, Callable
from app.models.objects import Signal, Bar1m, ChainSnapshot

class SignalEngine:
    def __init__(self, strategies: list):
        self.strategies = strategies

    def on_tick(self, bar: Bar1m, snap: ChainSnapshot) -> list[Signal]:
        out: list[Signal] = []
        for strat in self.strategies:
            try:
                sigs = strat.on_bar(bar, snap)
                if sigs:
                    out.extend(sigs)
            except Exception as e:
                # In production: metric + structured log
                print(f"[strategy_error] {strat.__class__.__name__}: {e}")
        return out
