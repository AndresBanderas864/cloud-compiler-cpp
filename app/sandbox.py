"""Adaptador de ejecución aislada mediante Docker."""

from __future__ import annotations

import asyncio
import shutil
import tempfile
from pathlib import Path
from typing import Awaitable, Callable

from .validation import MAX_RUNTIME_SECONDS, MAX_OUTPUT_BYTES, RunRequest


class SandboxUnavailable(RuntimeError):
    """Docker o la imagen de compilación no están disponibles."""


async def run_in_sandbox(
    request: RunRequest,
    on_output: Callable[[str], Awaitable[None]],
    on_input: "asyncio.Queue[str]",
    on_status: Callable[[str], Awaitable[None]],
) -> None:
    """Compila y ejecuta sin ejecutar código del usuario en el host."""
    if shutil.which("docker") is None:
        raise SandboxUnavailable("CC-901: Docker no está disponible en este servidor.")

    with tempfile.TemporaryDirectory(prefix="cloud-compiler-") as temp_dir:
        workspace = Path(temp_dir)
        (workspace / "main.cpp").write_text(request.code, encoding="utf-8")
        flag = {"c++17": "-std=c++17", "c++20": "-std=c++20", "c++23": "-std=c++23"}[request.standard]
        command = f"g++ {flag} -O0 -Wall -Wextra /workspace/main.cpp -o /tmp/main 2>&1 && exec /tmp/main"
        process = await asyncio.create_subprocess_exec(
            "docker", "run", "--rm", "-i",
            "--network", "none",
            "--memory", "256m",
            "--cpus", "1",
            "--pids-limit", "64",
            "--read-only",
            "--tmpfs", "/tmp:rw,nosuid,size=64m",
            "-v", f"{workspace}:/workspace:ro",
            "cloud-compiler-sandbox:latest",
            "sh", "-c", command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        async def forward_input() -> None:
            while True:
                value = await on_input.get()
                if value == "__CANCEL__":
                    if process.returncode is None:
                        process.kill()
                    return
                if process.stdin is None:
                    return
                process.stdin.write(value.encode("utf-8"))
                await process.stdin.drain()

        input_task = asyncio.create_task(forward_input())
        output_size = 0
        try:
            await on_status("compilando")
            while True:
                line = await asyncio.wait_for(process.stdout.readline(), timeout=MAX_RUNTIME_SECONDS)
                if not line:
                    break
                remaining = MAX_OUTPUT_BYTES - output_size
                if remaining > 0:
                    text = line[:remaining].decode("utf-8", errors="replace")
                    output_size += len(line[:remaining])
                    await on_output(text)
                if output_size >= MAX_OUTPUT_BYTES:
                    await on_status("salida limitada")
                    process.kill()
                    break
            await asyncio.wait_for(process.wait(), timeout=MAX_RUNTIME_SECONDS)
            if process.returncode == 0:
                await on_status("finalizado")
            elif process.returncode < 0:
                await on_output("\n[CC-005] La ejecución fue cancelada o terminó por un límite.\n")
                await on_status("cancelado")
            else:
                await on_status("error")
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            await on_output("\n[CC-004] Se alcanzó el límite de 5 minutos.\n")
            await on_status("tiempo agotado")
        finally:
            input_task.cancel()
            if process.returncode is None:
                process.kill()
                await process.wait()
