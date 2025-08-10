
import logging, time
from pathlib import Path
from app.data.feeds.mock_feed import CsvMockFeed
from app.strategies.ema_iv import EmaIvStrategy
from app.strategies.vwap_mr import VwapMrStrategy
from app.core.signal_engine import SignalEngine
from app.notifiers.telegram_bot import TelegramNotifier
from app.core.market_clock import is_market_open

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("runner")

def main():
    feed = CsvMockFeed(str(Path("sample_data/nifty_1m_sample.csv").resolve()))
    engine = SignalEngine([EmaIvStrategy(), VwapMrStrategy()])
    notifier = TelegramNotifier()

    for bar, snap in feed.stream():
        if not is_market_open(bar.ts):
            continue
        sigs = engine.on_tick(bar, snap)
        for s in sigs:
            log.info(f"Signal: {s.side} {s.symbol} @ {bar.close} | Reason: {s.reason}")
            notifier.send_signal(s)
        time.sleep(0.1)  # simulate near-real-time

if __name__ == "__main__":
    main()
