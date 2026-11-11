import asyncio
import uuid
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from temporalio.client import Client

from app.config import TASK_QUEUE, connect
from app.workflows import GreetingWorkflow

app = FastAPI()
DIST = Path(__file__).resolve().parent.parent / "web" / "dist"

_client: Client | None = None
_client_lock = asyncio.Lock()


async def get_client() -> Client:
    """One Temporal client per process, connected on first use."""
    global _client
    async with _client_lock:
        if _client is None:
            _client = await connect()
        return _client


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(DIST / "index.html")


@app.get("/api/health")
async def health() -> dict:
    # Cheap: no Temporal call, so the page stays up while workers or Temporal are away.
    return {"status": "ok", "taskQueue": TASK_QUEUE}


@app.get("/api/greet/{name}")
async def greet(name: str) -> dict:
    client = await get_client()
    # Each request gets its own workflow; the task queue keeps workspaces that
    # share a namespace apart.
    result = await client.execute_workflow(GreetingWorkflow.run, name, id=f"greeting-{TASK_QUEUE}-{uuid.uuid4()}", task_queue=TASK_QUEUE)
    return {"greeting": result}
