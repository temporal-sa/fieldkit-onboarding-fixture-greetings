import os
import uuid
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from temporalio.client import Client

from app.workflows import GreetingWorkflow

app = FastAPI()
DIST = Path(__file__).resolve().parent.parent / "web" / "dist"


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(DIST / "index.html")


@app.get("/api/greet/{name}")
async def greet(name: str) -> dict:
    client = await Client.connect(os.environ.get("TEMPORAL_ADDRESS", "localhost:7233"), namespace=os.environ.get("TEMPORAL_NAMESPACE", "default"))
    result = await client.execute_workflow(GreetingWorkflow.run, name, id=f"greeting-{uuid.uuid4()}", task_queue="greetings")
    return {"greeting": result}
