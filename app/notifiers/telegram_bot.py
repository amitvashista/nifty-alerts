
from __future__ import annotations
import logging
from app.config import settings
from app.models.objects import Signal
from datetime import datetime

try:
    from telegram import Bot
except Exception:  # if not installed yet in your env
    Bot = None

log = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self):
        token = settings.telegram_bot_token
        chat_id = settings.telegram_chat_id
        if not token or not chat_id:
            self.bot = None
            self.chat_id = None
            log.warning("Telegram creds missing; messages will be logged only.")
        else:
            self.bot = Bot(token=token) if Bot else None
            self.chat_id = chat_id

    def send(self, msg: str):
        if self.bot and self.chat_id:
            self.bot.send_message(chat_id=self.chat_id, text=msg)
        else:
            log.info(f"[TELMSG] {msg}")

    def send_signal(self, sig: Signal):
        txt = (
            f"\u26A1 NIFTY Option Signal\n"
            f"Time: {sig.ts.strftime('%H:%M:%S IST')}\n"
            f"Action: {sig.side}\n"
            f"Symbol: {sig.symbol}\n"
            f"SL: {sig.sl} | TGT: {sig.tgt} | R:R {sig.rr}\n"
            f"Reason: {sig.reason}\n"
            f"Confidence: {sig.confidence:.2f}"
        )
        self.send(txt)
