# Temporal greetings (fieldkit onboarding fixture)

A tiny Temporal demo: a web page asks a workflow for a greeting.

    python web/build.py
    pip install -r requirements.txt
    python -m app.worker &
    uvicorn app.web:app --port 8000

Test fixture for the fieldkit onboarding flow (tdo-nwj); not a real demo.

Optional settings: `ANTHROPIC_API_KEY` (a model writes the greeting) and
`GREETINGS_SIGNING_SECRET` (signs each greeting for the partner system that checks it).

## Running on the Temporal field demo platform

The platform builds one image from the root `Dockerfile` and runs it twice: as the
`web` component (the FastAPI app on port 8000, behind the demo's ingress, health-checked
at `/api/health`) and as the `worker` component (`python -m app.worker`). It sets
`TEMPORAL_ADDRESS`, `TEMPORAL_NAMESPACE`, `TEMPORAL_API_KEY` and `TEMPORAL_TLS` on both,
and each crashable workspace gets its own `TEMPORAL_TASK_QUEUE`, so the workflows a
browser starts run on that workspace's own worker.
