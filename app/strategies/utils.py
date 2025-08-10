
def nearest_atm_strike(spot: float, step: int = 50) -> int:
    # NIFTY strike step is typically 50
    return int(round(spot / step) * step)

def rr_target(entry: float, rr: float, direction: str) -> float:
    if direction == "long":
        return entry + rr * abs(entry * 0.002)  # rough placeholder move
    else:
        return entry - rr * abs(entry * 0.002)
