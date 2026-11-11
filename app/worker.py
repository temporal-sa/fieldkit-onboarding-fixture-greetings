import asyncio

from temporalio.worker import Worker

from app.activities import compose_greeting
from app.config import TASK_QUEUE, connect
from app.workflows import GreetingWorkflow


async def main() -> None:
    client = await connect()
    worker = Worker(client, task_queue=TASK_QUEUE, workflows=[GreetingWorkflow], activities=[compose_greeting])
    print(f"worker polling {TASK_QUEUE}", flush=True)
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
