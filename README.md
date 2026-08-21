# TaskFlow API

A learn-FastAPI-by-building-it project: a real task & project tracker backend (think a small
Trello/Asana), built from an empty folder up to a deployed, tested, containerized, CI'd service —
one day and one small set of commits at a time.

This is a **teaching project**. If you're picking this repo up to learn FastAPI with no prior
framework knowledge, start here:

1. Read [PROJECT_DETAILS.md](PROJECT_DETAILS.md) — what TaskFlow is, the tech stack (and *why*
   each piece was chosen), the data model, and the full API surface.
2. Read [SETUP.md](SETUP.md) — what to install, introduced exactly when the curriculum first
   needs it. Don't front-load every install; the point is understanding each tool as it arrives.
3. Follow [CURRICULUM.md](CURRICULUM.md) — the full day-by-day, commit-by-commit plan, 32 days
   across 11 phases, from "what is an API" through deployment and CI/CD. Every concept is
   explained with *why*, not just *what to type*.

Nothing in `app/` exists yet — this repo currently holds only its own teaching plan. Day 1's first
commits (see CURRICULUM.md) create `pyproject.toml` and the first `app/main.py`.

## What TaskFlow will end up doing

- Users register, log in, and get a JWT.
- Users create projects and invite other users as members (owner vs member roles).
- Projects contain tasks with status, priority, due dates, assignees, and labels.
- Tasks have comments and an activity log.
- A project dashboard shows cached, aggregated stats (task counts by status, overdue tasks).
- Task changes broadcast live over WebSockets to everyone viewing that project's board.
- Assignment notifications are processed by a Celery background worker.
- The whole stack — API, Postgres, Redis, worker — runs with `docker compose up`.
- Every push runs lint + the full test suite in GitHub Actions.

## Tech stack

FastAPI · Python 3.12+ · PostgreSQL · SQLAlchemy 2.0 (async) · Alembic · Pydantic v2 · PyJWT ·
pwdlib (Argon2) · Redis · Celery · WebSockets · pytest · Docker · GitHub Actions · uv

See [PROJECT_DETAILS.md](PROJECT_DETAILS.md#tech-stack-and-why-each-piece-is-in-here) for the
reasoning behind each choice.

## Repo map

```
fastapi-backend/
├── README.md            you are here
├── SETUP.md              what to install, and when
├── PROJECT_DETAILS.md    what TaskFlow is: data model, API surface, architecture
├── CURRICULUM.md         the full day-by-day, commit-by-commit learning plan
└── app/                  created starting Day 1 — doesn't exist yet
```

## Progress

Tracked in [CURRICULUM.md](CURRICULUM.md#progress-tracker) — check off each phase as you complete
it.

## Once the project exists (starting Day 1)

```
uv sync
uv run fastapi dev app/main.py
```
Then open `http://127.0.0.1:8000/docs`.

Full command reference lives in [SETUP.md](SETUP.md#quick-reference--running-things-once-the-whole-project-exists)
once there's something to run.


## Why `/docs` works with no extra code

FastAPI builds an OpenAPI schema from your route signatures as the app starts — every path
parameter, query parameter, and Pydantic body model you write becomes part of that schema
automatically. `/docs` (Swagger UI) and `/redoc` (ReDoc) are just two different renderers for
that same schema; you never hand-write API documentation, you generate it by writing normally
type-hinted Python.

## Why routes live in routers, not all in `main.py`

An `APIRouter` is a mini FastAPI app you attach to the real one with `app.include_router(...)` —
it lets each resource (items today; users, projects, tasks later) own its own file instead of
every route piling into one growing `main.py`. Two concrete payoffs: a router's logic can be
tested in isolation without booting the whole app, and ten routes changing in ten different files
means ten small diffs instead of one file everyone's editing at once. `prefix=` on the router
factors the shared path segment (`/items`) out of every route inside it; `tags=` controls how
`/docs` groups those routes in the UI — that's why the items routes now show under an "items"
heading instead of "default."
