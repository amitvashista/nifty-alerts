
# NIFTY Alerts MVP

Live(ish) signal + notification scaffold for NIFTY options. This MVP runs on a mock 1‑minute feed so you can verify the
pipeline end-to-end (ingest → strategies → Telegram). Later, swap the mock feed for a real broker feed (Zerodha/Upstox/etc.).

## Features
- EMA(20/50)+IV gate strategy, VWAP mean reversion strategy
- Market-hours filter (IST 09:15–15:30, no holiday calendar yet)
- Telegram notifications (rich message)
- FastAPI service with /health
- Clean architecture: feed → engine → strategies → notifier

## Quickstart
1) **Python 3.10+** recommended. Create a venv and install deps:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2) Copy env template and fill Telegram credentials:
   ```bash
   cp config/.env.example config/.env
   # Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
   ```
   - Create a Telegram bot with @BotFather → get token.
   - Get your chat id by messaging your bot and using a small helper (many guides online).

3) Run the mock live loop:
   ```bash
   python run_live.py
   ```
   You should see logs and (if configured) receive Telegram messages when signals trigger.

4) Run the API (optional):
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

## Wiring a real broker
- Replace `CsvMockFeed` with a broker WebSocket client that yields `(Bar1m, ChainSnapshot)`.
- For Zerodha (Kite), subscribe to NIFTY index token for 1m bars (or aggregate ticks), and poll option chain
  (IV, OI, PCR) every 1–3 minutes. Build a small adapter that maps broker payloads into our dataclasses.

## Strategy tuning
- Strategies are in `app/strategies/`. Start with `EmaIvStrategy` and `VwapMrStrategy` configs. Add time-of-day filters,
  stop-loss/target policies, and spread logic later.

## Notes
- This is **for personal educational use**. It does not place orders.
- If you later enable auto-ordering, ensure you comply with your broker's terms and applicable regulations.
