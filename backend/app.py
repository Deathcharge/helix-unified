from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time
from .state import get_live_state, get_status

app = FastAPI(title="Helix Unified")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"ok": True, "service": "helix-unified"}

@app.get("/status")
async def status():
    return get_status()

@app.get("/.well-known/helix.json")
async def helix_json():
    resp = get_live_state()
    return JSONResponse(resp, headers={"x-helix-version": resp.get("version","unknown")})

@app.websocket("/ws")
async def ws(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            await ws.send_json(get_live_state())
            await ws.receive_text()  # optional ping/pong
            time.sleep(1)
    except Exception:
        pass