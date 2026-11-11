# Temporal greetings (fieldkit onboarding fixture)

A tiny Temporal demo: a web page asks a workflow for a greeting.

    python web/build.py
    pip install -r requirements.txt
    python -m app.worker &
    uvicorn app.web:app --port 8000

Test fixture for the fieldkit onboarding flow (tdo-nwj); not a real demo.
