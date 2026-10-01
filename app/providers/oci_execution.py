"""Puente WebSocket entre el navegador y un runner OCI privado."""

from __future__ import annotations

import asyncio
import json

import websockets
from fastapi import WebSocket

from ..validation import RunRequest
from .oci_container_instances import OciContainerInstanceProvisioner


async def run_via_oci(request: RunRequest, browser: WebSocket) -> None:
    provisioner = OciContainerInstanceProvisioner()
    await browser.send_json({"type": "status", "value": "creando runner"})
    endpoint = await provisioner.create()
    try:
        await browser.send_json({"type": "status", "value": "conectando runner"})
        async with websockets.connect(endpoint.websocket_url, open_timeout=120, max_size=128 * 1024) as runner:
            await runner.send(json.dumps({"type": "start", "code": request.code, "standard": request.standard}))

            async def browser_to_runner() -> None:
                while True:
                    await runner.send(await browser.receive_text())

            async def runner_to_browser() -> None:
                async for message in runner:
                    await browser.send_text(message)

            forward = asyncio.create_task(browser_to_runner())
            receive = asyncio.create_task(runner_to_browser())
            done, pending = await asyncio.wait({forward, receive}, return_when=asyncio.FIRST_COMPLETED)
            for task in pending:
                task.cancel()
            for task in done:
                if task.exception() and not isinstance(task.exception(), asyncio.CancelledError):
                    raise task.exception()
    finally:
        await provisioner.delete(endpoint.instance_id)
