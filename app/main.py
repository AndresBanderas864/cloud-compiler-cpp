"""Punto de entrada HTTP y WebSocket del MVP."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .sandbox import SandboxUnavailable, run_in_sandbox
from .validation import MAX_CONCURRENT_USERS, ValidationError, validate_run_request

app = FastAPI(title="Cloud Compiler C++", version="0.1.0")
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
active_runs = 0
active_runs_lock = asyncio.Lock()


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "cloud-compiler-cpp"}


async def send_error(websocket: WebSocket, error_id: str, message: str) -> None:
    await websocket.send_json({"type": "error", "error_id": error_id, "message": message})


@app.websocket("/ws/run")
async def run_socket(websocket: WebSocket) -> None:
    global active_runs
    await websocket.accept()
    try:
        raw = await websocket.receive_text()
        payload = json.loads(raw)
        request = validate_run_request(payload.get("code"), payload.get("standard"))
    except (json.JSONDecodeError, AttributeError, TypeError):
        await send_error(websocket, "CC-000", "La solicitud no tiene un formato válido.")
        await websocket.close(code=1003)
        return
    except ValidationError as error:
        await send_error(websocket, error.error_id, error.message)
        await websocket.close(code=1003)
        return

    async with active_runs_lock:
        if active_runs >= MAX_CONCURRENT_USERS:
            await send_error(websocket, "CC-010", "El servicio está ocupado. Intenta de nuevo más tarde.")
            await websocket.close(code=1013)
            return
        active_runs += 1

    input_queue: asyncio.Queue[str] = asyncio.Queue()

    async def output(text: str) -> None:
        await websocket.send_json({"type": "output", "value": text})

    async def status(value: str) -> None:
        await websocket.send_json({"type": "status", "value": value})

    async def receive_input() -> None:
        try:
            while True:
                message = json.loads(await websocket.receive_text())
                if message.get("type") == "stdin":
                    await input_queue.put(str(message.get("value", "")))
                elif message.get("type") == "cancel":
                    await input_queue.put("__CANCEL__")
                    return
        except (WebSocketDisconnect, json.JSONDecodeError):
            await input_queue.put("__CANCEL__")

    receiver = asyncio.create_task(receive_input())
    try:
        await status("iniciando")
        await run_in_sandbox(request, output, input_queue, status)
    except SandboxUnavailable as error:
        await send_error(websocket, "CC-901", str(error))
    except (WebSocketDisconnect, RuntimeError):
        pass
    finally:
        receiver.cancel()
        async with active_runs_lock:
            active_runs -= 1
        try:
            await websocket.close()
        except RuntimeError:
            pass
