"""Runner efímero: compila y ejecuta un único trabajo C++."""

from __future__ import annotations

import asyncio
import json
import os
import resource
import tempfile
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI(title="Cloud Compiler Runner")
STANDARDS = {"c++17": "-std=c++17", "c++20": "-std=c++20", "c++23": "-std=c++23"}
MAX_CODE_BYTES = 100 * 1024
MAX_OUTPUT_BYTES = 100 * 1024
MAX_RUNTIME_SECONDS = 300
TOKEN = os.environ.get("RUNNER_TOKEN", "")


def limits() -> None:
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_CPU, (MAX_RUNTIME_SECONDS, MAX_RUNTIME_SECONDS))
    resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_OUTPUT_BYTES, MAX_OUTPUT_BYTES))
    resource.setrlimit(resource.RLIMIT_NPROC, (64, 64))


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "compiler-runner"}


@app.websocket("/ws/run")
async def run_socket(websocket: WebSocket) -> None:
    if not TOKEN or websocket.query_params.get("token") != TOKEN:
        await websocket.close(code=1008)
        return
    await websocket.accept()
    process: asyncio.subprocess.Process | None = None
    input_queue: asyncio.Queue[str] = asyncio.Queue()
    cancelled = asyncio.Event()
    output_size = 0

    async def send(kind: str, value: str) -> None:
        await websocket.send_json({"type": kind, "value": value})

    async def receive_input() -> None:
        nonlocal process
        try:
            while True:
                message = json.loads(await websocket.receive_text())
                if message.get("type") == "stdin":
                    await input_queue.put(str(message.get("value", "")))
                elif message.get("type") == "cancel":
                    cancelled.set()
                    if process and process.returncode is None:
                        process.kill()
                    return
        except (WebSocketDisconnect, json.JSONDecodeError):
            cancelled.set()
            if process and process.returncode is None:
                process.kill()

    try:
        start = json.loads(await websocket.receive_text())
        code = start.get("code", "")
        standard = start.get("standard", "")
        if not isinstance(code, str) or len(code.encode("utf-8")) > MAX_CODE_BYTES:
            await send("error", "[CC-002] El código supera el límite permitido.")
            return
        if standard not in STANDARDS:
            await send("error", "[CC-003] Estándar C++ no soportado.")
            return
        receiver = asyncio.create_task(receive_input())
        with tempfile.TemporaryDirectory(prefix="compiler-runner-") as folder:
            source = Path(folder) / "main.cpp"
            source.write_text(code, encoding="utf-8")
            deadline = asyncio.get_running_loop().time() + MAX_RUNTIME_SECONDS

            await send("status", "compilando")
            process = await asyncio.create_subprocess_exec(
                "g++", STANDARDS[standard], "-O0", "-Wall", "-Wextra",
                str(source), "-o", str(Path(folder) / "main"),
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                preexec_fn=limits,
            )
            compile_output, _ = await asyncio.wait_for(process.communicate(), max(1, deadline - asyncio.get_running_loop().time()))
            if compile_output:
                await send("output", compile_output[:MAX_OUTPUT_BYTES].decode("utf-8", errors="replace"))
            if process.returncode != 0:
                await send("output", "\n[CC-006] Error de compilacion.\n")
                await send("status", "error")
                receiver.cancel()
                return

            await send("status", "ejecutando")
            process = await asyncio.create_subprocess_exec(
                str(Path(folder) / "main"),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                preexec_fn=limits,
            )

            async def forward_input() -> None:
                while True:
                    value = await input_queue.get()
                    if process.stdin is None:
                        return
                    process.stdin.write(value.encode("utf-8"))
                    await process.stdin.drain()

            forwarder = asyncio.create_task(forward_input())
            try:
                while True:
                    remaining = max(1, deadline - asyncio.get_running_loop().time())
                    line = await asyncio.wait_for(process.stdout.readline(), remaining)
                    if not line:
                        break
                    if output_size < MAX_OUTPUT_BYTES:
                        chunk = line[: MAX_OUTPUT_BYTES - output_size]
                        output_size += len(chunk)
                        await send("output", chunk.decode("utf-8", errors="replace"))
                await process.wait()
                if cancelled.is_set():
                    await send("status", "cancelado")
                elif process.returncode == 0:
                    await send("status", "finalizado")
                else:
                    await send("output", "\n[CC-007] Error de ejecucion.\n")
                    await send("status", "error")
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                await send("output", "\n[CC-004] Se alcanzo el limite de 5 minutos.\n")
                await send("status", "tiempo agotado")
            finally:
                forwarder.cancel()
        receiver.cancel()
    except (WebSocketDisconnect, asyncio.CancelledError):
        if process and process.returncode is None:
            process.kill()
            await process.wait()
