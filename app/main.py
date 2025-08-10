
from fastapi import FastAPI
from app.config import settings

app = FastAPI(title="NIFTY Alerts MVP")

@app.get("/health")
def health():
    return {"ok": True, "env": settings.env}
