# Project Web3

Narrative-driven RPG companion that blends cooperative storytelling with AI support. Players create text-based adventures, exchange turn-by-turn interactions, and let the narrator stream fresh story beats on demand.

## Execution

### Direct (local tooling)

- Backend: `python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000`
- Frontend: `cd frontend; npm install; npm run dev`

### Docker Compose

```
docker compose up --build
```

This exposes the API on port 8000 and the Svelte UI on port 5173.

## Code

### Backend

FastAPI service with SQLite persistence. Core flows:

- `/auth/*` for signup, login, and token verification
- `/game/*` to create, list, and manage text adventures (requires bearer token)
- `/play/player` and `/play/narrator` for player turns and AI narrator streaming

The backend directory ships with its own README containing detailed setup, schema, and route documentation.

### Frontend

SvelteKit app styled for a chat-like narrative cockpit. Key screens include home, games listing/creation, and the live session view with unified composer (player entry or narrator trigger). It consumes the backend REST endpoints via lightweight TypeScript API helpers and stores auth state through cookie-aware Svelte stores.
