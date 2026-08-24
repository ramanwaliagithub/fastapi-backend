# Setup — What to Install, and When

Don't install everything up front. Part of the point of this course is understanding *why* each
tool exists, and that lands better if you install it right when you first need it. This file is
ordered to match [CURRICULUM.md](CURRICULUM.md) — each section names the day that first needs it.

If you're starting fresh today, at minimum do the **"Before Day 1"** section now; everything else
can wait.

---

## Before Day 1 — the baseline toolchain

| Tool | Why | Install | Verify |
|---|---|---|---|
| **Python 3.12+** | The language runtime everything else needs | [python.org](https://www.python.org/downloads/) or your OS package manager | `python --version` |
| **uv** | Package manager, virtual env, and lockfile in one tool | `curl -LsSf https://astral.sh/uv/install.sh \| sh` (macOS/Linux) or `powershell -c "irm https://astral.sh/uv/install.ps1 \| iex"` (Windows) | `uv --version` |
| **Git** | Version control — every day's work is a commit | [git-scm.com](https://git-scm.com/downloads) | `git --version` |
| **A code editor** | VS Code recommended: install the *Python* and *Pylance* extensions | [code.visualstudio.com](https://code.visualstudio.com/) | — |
| **A GitHub account** | Where the repo will eventually be pushed (optional until you want a remote) | [github.com](https://github.com/join) | — |
| **A REST client** | For manually poking endpoints outside `/docs` — VS Code's built-in *REST Client* extension, Postman, or plain `curl` all work | pick one | — |

You do **not** need to install FastAPI, SQLAlchemy, or anything else globally — `uv` manages all
of that per-project starting Day 1's `uv init` / `uv add` commands.

---

## Day 1 — project dependencies

Once `pyproject.toml` exists (first commit of Day 1), add the framework:

```
uv add "fastapi[standard]"
```

The `[standard]` extra pulls in `uvicorn` (the ASGI server that actually runs the app) plus the
`fastapi dev` CLI, form-data/multipart support, and a few other commonly-needed pieces — all as
regular (non-dev) dependencies, since the app needs `uvicorn` to run at all, not just during
development.

Run the app:
```
uv run fastapi dev app/main.py
```

## Day 4 — configuration

```
uv add pydantic-settings
```

From this point on, copy `.env.example` to a real `.env` before running the app:
```
cp .env.example .env
```
`.env` is gitignored — it's where your actual local values live. `.env.example` stays committed
and documents the *shape* of required config without leaking real secrets. As of Day 4, both
fields (`APP_NAME`, `DEBUG`) have defaults, so the app still runs even without a `.env` file; that
changes on Day 7, when a required database URL is added.

## Day 5 — testing

```
uv add --dev pytest
```

`--dev` because tests never need to ship with the running app — this dependency exists for local
development and CI only. `httpx` (needed by `fastapi.testclient.TestClient`) is already present,
pulled in transitively by the `fastapi[standard]` extra from Day 1.

```
uv run pytest -v
```

## Day 7 — Docker & Postgres

| Tool | Why | Install |
|---|---|---|
| **Docker Desktop** (or Docker Engine + Compose on Linux) | Runs Postgres (and later Redis) in a container instead of a native install | [docker.com/get-started](https://www.docker.com/get-started/) |

```
uv add "sqlalchemy[asyncio]" asyncpg psycopg2-binary alembic
```

`psycopg2-binary` is used only by Alembic for synchronous migrations; the app itself talks to
Postgres through `asyncpg`. Verify Docker: `docker compose up -d` after Day 7's `docker-compose.yml`
commit, then `docker compose ps` should show `postgres` healthy.

## Day 11 — auth dependencies

```
uv add pyjwt "pwdlib[argon2]" python-multipart
```

`python-multipart` is required for FastAPI to parse the form-encoded login request (Day 12).

## Day 20 — test dependencies

```
uv add --dev pytest pytest-asyncio httpx pytest-cov
```

Run tests from Day 20 onward with:
```
uv run pytest -v
```

## Day 23 — Celery & Redis

| Tool | Why | Install |
|---|---|---|
| **Redis** | Message broker for Celery, and later the cache backend | via Docker Compose — no native install needed |

```
uv add celery redis
```

Run a worker locally (separate terminal, once Day 23's code exists):
```
uv run celery -A app.tasks.celery_app worker --loglevel=info
```

## Day 24 — caching

No new tool — reuses the Redis container from Day 23. Just:
```
uv add redis
```
(if not already added on Day 23).

## Day 25–26 — WebSockets

No new install — WebSocket support ships with `uvicorn[standard]`, already present since Day 1.

## Day 27 — rate limiting

```
uv add slowapi
```

## Day 28 — structured logging

```
uv add structlog
```

## Day 29 — metrics (optional but recommended)

```
uv add prometheus-fastapi-instrumentator
```

Optional local viewing: run Prometheus + Grafana via a small additional Compose service if you
want to actually see the metrics graphed — not required to complete the course.

## Day 30 — full stack tooling

Nothing new to install — this day wires together everything already added (Docker, Compose) into
one multi-service `docker-compose.yml`.

## Day 31 — CI

Nothing to install locally. You'll need to have pushed the repo to GitHub for
`.github/workflows/ci.yml` to run.

Optional: install the [GitHub CLI](https://cli.github.com/) (`gh`) if you'd rather manage the repo
and check CI runs from the terminal instead of the browser.

## Day 32 — deployment

Pick **one** free-tier host when you get there (no need to decide now):
- [Render](https://render.com/) — simplest for a Docker Compose-shaped app
- [Railway](https://railway.app/)
- [Fly.io](https://fly.io/)

Whichever you pick, you'll need an account and (per their docs) their CLI tool installed at that
point.

---

## Quick reference — running things once the whole project exists

| Command | What it does |
|---|---|
| `uv sync` | Install/update all dependencies from the lockfile |
| `uv run fastapi dev app/main.py` | Run the API locally with auto-reload |
| `uv run alembic upgrade head` | Apply database migrations |
| `uv run alembic revision --autogenerate -m "message"` | Draft a new migration from model changes |
| `uv run pytest -v` | Run the test suite |
| `uv run ruff check .` | Lint |
| `docker compose up -d` | Start Postgres (+ Redis, worker, api once added) in the background |
| `docker compose down` | Stop everything |
| `uv run celery -A app.tasks.celery_app worker --loglevel=info` | Run a background worker |

## Linting (introduce whenever you like, no fixed day)

```
uv add --dev ruff
```
```
uv run ruff check .
uv run ruff format .
```
