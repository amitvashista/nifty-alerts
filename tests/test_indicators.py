import numpy as np
import pandas as pd

from app.core.indicators import ema, vwap, atr


def test_ema_simple_series():
    series = pd.Series([1, 2, 3, 4, 5], dtype=float)
    result = ema(series, length=3)
    expected = pd.Series([1.0, 1.5, 2.25, 3.125, 4.0625])
    np.testing.assert_allclose(result.values, expected.values)


def test_vwap_simple_dataframe():
    df = pd.DataFrame(
        {
            "close": [10, 20, 30],
            "high": [12, 22, 32],
            "low": [8, 18, 28],
            "volume": [100, 200, 300],
        }
    )
    result = vwap(df)
    expected = pd.Series([10.0, 5000 / 300, 14000 / 600])
    np.testing.assert_allclose(result.values, expected.values)


def test_atr_simple_dataframe():
    df = pd.DataFrame(
        {
            "high": [10, 15, 20, 18],
            "low": [5, 10, 12, 14],
            "close": [8, 12, 16, 17],
        }
    )
    result = atr(df, length=3)
    assert np.isnan(result.iloc[0])
    assert np.isnan(result.iloc[1])
    np.testing.assert_allclose(result.iloc[2:].values, np.array([20 / 3, 19 / 3]))
