# Workout 2 — A Client That Can Call the Backend

Workout 2 introduces a caller crossing the trust boundary. We add a thin client that issues HTTP requests to the unauthenticated backend from Workout 1. Everything still works, which is precisely the point—we now have a concrete call path to evaluate before layering authentication.

## Client quickstart (browser)

Spin up the Workout 1 FastAPI server first, then point your browser at `http://localhost:8000/`. The browser acts as our client, rendering the JSON from the backend. At this stage there is no authentication, cookies, or special headers—just a simple HTTP GET so we can inspect the raw request/response flow. 

Open `http://localhost:8000/health` for the health endpoint, or `http://localhost:8000/` for the hello-world payload.
