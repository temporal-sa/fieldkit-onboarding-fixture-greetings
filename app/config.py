"""Temporal connection settings, read from the environment.

The catalog sets TEMPORAL_ADDRESS, TEMPORAL_NAMESPACE, TEMPORAL_API_KEY and
TEMPORAL_TLS on workers and temporalAccess components; locally the defaults
point at a dev server on localhost.
"""
import os

from temporalio.client import Client

TASK_QUEUE = os.environ.get("TEMPORAL_TASK_QUEUE", "greetings")


async def connect() -> Client:
    api_key = os.environ.get("TEMPORAL_API_KEY") or None
    tls_env = os.environ.get("TEMPORAL_TLS", "").strip().lower()
    # An API key implies TLS (Temporal Cloud) unless TEMPORAL_TLS says otherwise.
    tls = tls_env in ("1", "true", "yes") if tls_env else api_key is not None
    return await Client.connect(
        os.environ.get("TEMPORAL_ADDRESS", "localhost:7233"),
        namespace=os.environ.get("TEMPORAL_NAMESPACE", "default"),
        api_key=api_key,
        tls=tls,
    )
