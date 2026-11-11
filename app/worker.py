import asyncio
import os

from temporalio.client import Client
from temporalio.worker import Worker

from app.activities import compose_greeting
from app.workflows import GreetingWorkflow

TASK_QUEUE = "greetings"


async def main() -> None:
    client = await Client.connect(os.environ.get("TEMPORAL_ADDRESS", "localhost:7233"), namespace=os.environ.get("TEMPORAL_NAMESPACE", "default"))
    worker = Worker(client, task_queue=TASK_QUEUE, workflows=[GreetingWorkflow], activities=[compose_greeting])
    print(f"worker polling {TASK_QUEUE}", flush=True)
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
