
import pandas as pd
from datetime import datetime
from app.models.objects import Bar1m, ChainSnapshot
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

class CsvMockFeed:
    """Yields 1-minute bars from a CSV and synthesizes basic chain snapshots."""
    def __init__(self, path: str):
        self.df = pd.read_csv(path, parse_dates=['ts'])
        self.df.sort_values('ts', inplace=True)
        self.df.reset_index(drop=True, inplace=True)

    def stream(self):
        for _, row in self.df.iterrows():
            bar = Bar1m(
                ts=row['ts'].to_pydatetime().replace(tzinfo=IST),
                open=float(row['open']), high=float(row['high']),
                low=float(row['low']), close=float(row['close']),
                volume=float(row.get('volume', 0.0)),
            )
            # Synthesize chain snapshot (placeholders). In live mode, pull real VIX, IV%, PCR.
            snap = ChainSnapshot(
                ts=bar.ts,
                spot=bar.close,
                vix=14.0 + 4.0 * ((bar.close % 100) / 100.0),  # playful variation
                iv_percentile=50.0,  # constant placeholder
                pcr=1.0,  # neutral placeholder
            )
            yield bar, snap
