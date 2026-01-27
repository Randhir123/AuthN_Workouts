# Workout 1 - Hello-world backend (no auth)

Workout 1 — A Backend With No Authentication

We start by building the simplest possible backend that responds to requests without any notion of identity or authentication. This is not a warm-up exercise; it establishes the baseline. Every system already accepts or rejects requests in some way, even when no security logic is present. Before we can reason about authentication, we need to see what an unauthenticated system actually looks like.

This workout focuses on sending and receiving HTTP requests without any authentication. The backend intentionally returns a constant payload so that future workouts can build on top of it.

## Backend quickstart

Run everything from `part1/workout1/backend` so Python can import `app.py` correctly.

```bash
cd part1/workout1/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The server exposes two routes on port 8000:

- `GET /health` – sanity endpoint that replies with `{ "status": "ok" }`.
- `GET /` – returns a JSON hello-world payload.

Use `curl http://localhost:8000/` to confirm the response.
