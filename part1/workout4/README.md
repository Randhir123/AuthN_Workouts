# Workout 4 — Introducing a Protected Endpoint

Workout 4 adds the first explicit "no" in the series. A new endpoint refuses requests outright. There is still no identity, login, or session, but we now have a concrete authentication rule that draws a line between callers.

## Backend quickstart

```bash
cd part1/workout4/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## Endpoints

- `GET /health` – returns `{ "status": "ok" }`.
- `GET /public` – always returns a hello-world payload.
- `GET /protected` – rejects every request with `403 Forbidden`. No credential yet, just a hard denial to make the boundary explicit.

Example:

```bash
curl -i http://localhost:8000/protected
# HTTP/1.1 403 Forbidden
```

The important part isn't sophistication; it's that the backend now has a binary decision. Later workouts will replace the hardcoded "no" with evidence-based checks.
