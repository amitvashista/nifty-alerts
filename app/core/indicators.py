
import numpy as np
import pandas as pd

def ema(series: pd.Series, length: int) -> pd.Series:
    return series.ewm(span=length, adjust=False).mean()

def vwap(df: pd.DataFrame) -> pd.Series:
    # expects columns: 'close','high','low','volume'
    typical_price = (df['high'] + df['low'] + df['close']) / 3.0
    pv = typical_price * df['volume'].replace(0, np.nan).fillna(method='ffill').fillna(0)
    cumulative_pv = pv.cumsum()
    cumulative_vol = df['volume'].cumsum().replace(0, np.nan)
    out = cumulative_pv / cumulative_vol
    return out.fillna(method='bfill').fillna(method='ffill')

def atr(df: pd.DataFrame, length: int = 14) -> pd.Series:
    high, low, close = df['high'], df['low'], df['close']
    prev_close = close.shift(1)
    tr = pd.concat([(high - low), (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)
    return tr.rolling(length).mean()
