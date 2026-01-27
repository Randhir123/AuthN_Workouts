# Workout 3 — Trust Boundaries and CORS

Workout 3 makes the trust boundary explicit. The backend now decides which browser origins may read its responses. By turning on CORS we acknowledge that not every caller is equal, even when they can open a TCP connection. This is the scaffolding we'll need before adding any notion of identity.

## Backend quickstart

```bash
cd part1/workout3/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Key behavior: the FastAPI app uses `CORSMiddleware` to only allow browsers originating from `http://localhost:5173`, `http://127.0.0.1:5173`, `http://localhost:8001`, or `http://127.0.0.1:8001`. Command-line clients like `curl` still work from anywhere because CORS governs browser behavior rather than raw HTTP.

## Browser client

A bare-bones static page at `part1/workout3/client/index.html` runs `fetch()` against the backend. Serve it from an allowed origin to see a successful response:

```bash
cd part1/workout3/client
python -m http.server 5173
```

Then visit `http://localhost:5173/` in your browser, open DevTools, and click "Call backend". If you re-run the static file server on a different port (for example `python -m http.server 9000`), the request will be blocked because the origin is no longer on the allow-list. Use the Network tab to inspect the preflight (if any) and the failed request to understand how the boundary shows up in a real browser.
