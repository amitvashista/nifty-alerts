
from app.strategies.utils import nearest_atm_strike, rr_target

def test_nearest_atm():
    assert nearest_atm_strike(23487) in (23450, 23500)

def test_rr_target():
    e = 100.0
    t = rr_target(e, 1.2, "long")
    assert t > e
