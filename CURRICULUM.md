# Curriculum — Learning FastAPI by Building TaskFlow

## How to use this document

- One **day** = one sitting. Each day has a goal, the concepts it introduces (with the *why*,
  not just the *what*), a sequence of **commits**, and the files that commit touches.
- Commit as you go, in the order listed. The commit messages are suggestions (conventional-commit
  style: `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`) — use your own wording if you
  like, but keep the same granularity. Small, meaningful commits are themselves part of what
  you're learning: they make the eventual `git log` a readable story of how the project grew.
- Don't copy-paste code you haven't read. Type it. When something works, stop for a second and
  answer "why did that work" before moving on.
- Every phase ends with a doc commit marking it complete — treat that as a checkpoint to
  re-read [PROJECT_DETAILS.md](PROJECT_DETAILS.md) and see how the piece you just built fits the
  whole.
- [SETUP.md](SETUP.md) tells you exactly what to install and *when* — you never need to install
  something before the day that first needs it.

**Pace**: 32 teaching days across 11 phases, roughly 6+ weeks at 5 days/week. Nothing here is
timed — go slower if a concept needs it. Understanding *why* SQLAlchemy sessions work the way they
do is worth more than finishing on schedule.

## Progress tracker

- [x] Phase 0 — Orientation & Environment (Days 1–2)
- [ ] Phase 1 — FastAPI & Python Web Fundamentals (Days 3–6, Day 3 done)
- [ ] Phase 2 — Database Foundations (Days 7–10)
- [ ] Phase 3 — Authentication & Authorization (Days 11–14)
- [ ] Phase 4 — Full CRUD + Business Logic (Days 15–19)
- [ ] Phase 5 — Testing (Days 20–21)
- [ ] Phase 6 — Background Jobs (Days 22–23)
- [ ] Phase 7 — Caching (Day 24)
- [ ] Phase 8 — Real-time with WebSockets (Days 25–26)
- [ ] Phase 9 — API Hardening (Days 27–28)
- [ ] Phase 10 — Observability (Day 29)
- [ ] Phase 11 — Deployment & CI/CD (Days 30–32)

---

## Phase 0 — Orientation & Environment

### Day 1 — Why FastAPI, and your first running server

**Goal**: Understand what a web framework does, why FastAPI specifically, and get a server running.

**Concepts**:
- What an API actually is: a program that talks HTTP (method + path + status code + JSON) instead
  of rendering HTML for humans.
- **WSGI vs ASGI** — the old Python web standard (WSGI, used by Flask/Django classic) handles one
  request at a time per worker; **ASGI** (used by FastAPI, via Starlette + Uvicorn) is built around
  `async`/`await`, so one worker can juggle many in-flight requests — crucial once you're waiting
  on a database or an external API.
- Why `uv` instead of raw `pip` + `venv`: one tool for the virtual environment, dependency
  resolution, and lockfile — the modern standard as of 2025/2026.
- `git init` on day one, not "later" — version control from the start is a habit, not an
  afterthought.

**Commits**:
1. `chore: initialize git repo and .gitignore` — start version control before any code exists.
2. `chore: initialize uv project` — `uv init`, creating `pyproject.toml`; establishes reproducible
   dependency management up front.
3. `feat: add hello-world FastAPI app` — the smallest possible app: one route returning JSON. The
   point is to run `uv run fastapi dev app/main.py` and see it work.
4. `docs: add README with project overview and run instructions` — the repo explains itself from
   commit one.

**Files created**: `.gitignore`, `pyproject.toml`, `uv.lock`, `app/__init__.py`, `app/main.py`,
`README.md`
- `app/main.py` — the entry point. Holds the single `FastAPI()` instance every route eventually
  attaches to. Everything else in the app exists to be *wired into* this file, directly or
  indirectly.
- `app/__init__.py` — marks `app/` as a Python package so `app.main` is importable.

### Day 2 — Anatomy of a FastAPI app & automatic docs

**Goal**: Understand path operations and *why* `/docs` exists for free.

**Concepts**:
- Path operation decorators (`@app.get`, `@app.post`, ...) register a function against a route.
- FastAPI reads your **type hints** to validate and convert incoming data — this is the core trick
  that makes everything else (docs, validation, editor autocomplete) work. A path param typed
  `int` rejects `"abc"` automatically; you didn't write that check.
- Path params vs query params (`/tasks/{id}` vs `/tasks?status=done`) and when to use each.
- Pydantic `BaseModel` as a request body — your first schema.
- The OpenAPI schema is generated from your code, not hand-written; Swagger UI (`/docs`) and
  ReDoc (`/redoc`) just render it.

**Commits**:
1. `feat: add path and query parameter example routes` — demonstrates type-hint-driven validation.
2. `feat: add Pydantic request body example route` — first `BaseModel`, first `POST`.
3. `docs: explain how automatic docs work` — close the loop on "why FastAPI" from Day 1.
4. `chore: add .env.example placeholder` — nothing reads it yet, but the habit starts now.

**Files created**: `app/routers/` isn't needed yet — everything still lives in `main.py`
deliberately, so Day 3's refactor has something real to point at. `.env.example`.

---

## Phase 1 — FastAPI & Python Web Fundamentals

### Day 3 — Routers & project structure

**Goal**: Understand why real apps don't put every route in one file, and split into an
`APIRouter`.

**Concepts**:
- `APIRouter` is a mini FastAPI app you `include_router()` into the real one — it lets each
  resource (users, projects, tasks...) own its own file.
- `prefix=` and `tags=` on a router control the URL prefix and how `/docs` groups routes.
- Why this matters beyond tidiness: testability (you can unit-test a router's logic in isolation)
  and merge conflicts (ten people editing one 2000-line `main.py` is miserable).

**Commits**:
1. `refactor: extract routers package, move example routes out of main.py`
2. `feat: add routers/items.py demo router with tags`
3. `docs: explain routers and why we organize this way`

**Files created**: `app/routers/__init__.py`, `app/routers/items.py`
- `app/routers/items.py` — a throwaway resource used only to learn the router pattern; deleted on
  Day 6 once the real domain (Phase 2 onward) replaces it.

### Day 4 — Config management & environment variables

**Goal**: Stop hardcoding values; learn `pydantic-settings`.

**Concepts**:
- The [12-factor app](https://12factor.net/config) principle: config lives in the environment, not
  in code — so the same code runs in dev/test/prod by changing only env vars.
- `pydantic-settings.BaseSettings` reads env vars (and a `.env` file) into a typed, validated
  object — get a typo in a var name and it fails at startup, not silently at 3am.
- Why `.env` is gitignored but `.env.example` is committed: document the *shape* of required
  config without leaking real secrets.

**Commits**:
1. `feat: add app/config.py with pydantic-settings`
2. `chore: wire settings into main.py, update .env.example`
3. `docs: update SETUP.md — env variables introduced here`

**Files created**: `app/config.py`
- `app/config.py` — the single source of truth for configuration; every other module that needs a
  setting imports `settings` from here instead of reading `os.environ` directly.

### Day 5 — Response models, status codes, and error handling

**Goal**: Understand `response_model`, explicit status codes, and `HTTPException`.

**Concepts**:
- `response_model=` filters and validates *outgoing* data — e.g. it's how you guarantee a password
  hash never accidentally leaks in a response, even if the ORM object technically has that field.
- Explicit `status_code=` on the decorator (e.g. `201` for creation) vs FastAPI's `200` default —
  API consumers rely on these being correct.
- `HTTPException` is how you turn "this request is invalid/not found/forbidden" into a proper HTTP
  response instead of a Python traceback leaking to the client.
- Why request and response schemas are usually *separate classes* even when they look similar
  (a `UserCreate` takes a password; a `UserOut` must never include one).

**Commits**:
1. `feat: add response_model and explicit status codes to demo routes`
2. `feat: add HTTPException error handling example (404 case)`
3. `test: add first pytest smoke test using TestClient`
4. `docs: note pytest install in SETUP.md`

**Files created**: `tests/__init__.py`, `tests/test_main.py`
- `tests/test_main.py` — first test file, using FastAPI's synchronous `TestClient`. Deliberately
  simple; Phase 5 replaces this with the real async test setup once there's a real app to test.

### Day 6 — Clear the scaffolding, prep the real domain

**Goal**: Remove the throwaway demo code and lay empty, documented folders for TaskFlow itself.

**Commits**:
1. `refactor: remove demo routes and items router`
2. `chore: scaffold empty app/models, app/schemas, app/services packages`
3. `docs: mark Phase 1 complete in the progress tracker`

**Files created**: `app/models/__init__.py`, `app/schemas/__init__.py`, `app/services/__init__.py`
(all empty — populated starting Day 8)

---

## Phase 2 — Database Foundations

### Day 7 — Postgres via Docker + the async SQLAlchemy engine

**Goal**: Get Postgres running without installing it natively, and connect to it.

**Concepts**:
- What an **ORM** is: it lets you work with Python objects/classes instead of writing raw SQL
  strings, while still ultimately generating SQL. You're not avoiding SQL — you're generating it
  from a typed, composable API.
- Why Postgres: the realistic default for a production Python backend — real transactions, real
  constraints, a real query planner.
- Why Docker for the database: your database version is *pinned and reproducible* across every
  machine that runs this project, and you don't pollute your OS with a native Postgres install.
- SQLAlchemy's **async engine**: because your route handlers are `async def`, DB calls need to be
  awaitable too, or they'd block the whole event loop — defeating the point of ASGI from Day 1.
- Dependency injection for DB sessions: `Depends(get_db)` hands each request its own session and
  guarantees it's closed afterward, even on error.

**Commits**:
1. `chore: add docker-compose.yml with a postgres service`
2. `feat: add app/database.py — async engine, session factory, get_db dependency`
3. `docs: SETUP.md — Docker Desktop and docker compose introduced here`

**Files created**: `docker-compose.yml`, `app/database.py`
- `app/database.py` — creates the async engine (the connection pool) once at import time, and
  exposes `get_db()`, a generator dependency every DB-touching route will depend on.

### Day 8 — First real models: User & Project

**Goal**: Define real SQLAlchemy models.

**Concepts**:
- SQLAlchemy 2.0's typed style: `Mapped[int]` + `mapped_column(...)` instead of the older untyped
  `Column(...)` — your editor now knows `user.id` is an `int`.
- Primary keys, foreign keys, `server_default` (a default computed by Postgres, e.g. `now()`, vs a
  Python-side default).
- `relationship()` — how SQLAlchemy lets you write `project.owner` in Python and have it resolve
  to a real SQL join/query behind the scenes.

**Commits**:
1. `feat: add User model`
2. `feat: add Project model with owner relationship`
3. `chore: register models on Base metadata`

**Files created**: `app/models/user.py`, `app/models/project.py`
- `app/models/user.py` — the `User` table definition: every other entity eventually points back to
  a user (owner, author, assignee).
- `app/models/project.py` — the first "real" domain entity; owns tasks, labels, and members.

### Day 9 — Alembic migrations

**Goal**: Understand schema evolution over time instead of `Base.metadata.create_all()`.

**Concepts**:
- Why `create_all()` doesn't scale past a toy project: it can create tables, but it can't safely
  evolve an existing table (add a column, rename one, backfill data) without data loss.
- Alembic tracks schema history as a sequence of Python migration scripts, each with an
  `upgrade()`/`downgrade()` — this is how a team keeps every developer's (and production's)
  database schema in sync.
- `--autogenerate` diffs your models against the current DB schema and drafts the migration for
  you — you review it, you don't blindly trust it.

**Commits**:
1. `chore: initialize alembic`
2. `feat: generate first migration — create users and projects tables`
3. `docs: SETUP.md — alembic upgrade head noted as a required step after pulling migrations`

**Files created**: `alembic.ini`, `alembic/env.py`, `alembic/versions/xxxx_create_users_and_projects.py`
- `alembic/env.py` — wires Alembic to your `Base.metadata` and your database URL, so
  `--autogenerate` can see your models.

### Day 10 — Many-to-many: ProjectMember & Label

**Goal**: Model relationships that carry their own data, not just bare foreign keys.

**Concepts**:
- A plain many-to-many needs only a bare association *table*. `ProjectMember` needs to be a full
  **association object** (a real mapped class) because it carries an extra column (`role`) — this
  distinction — table vs. object — is one of the most common SQLAlchemy stumbling points, worth
  sitting with.
- `Label` is a project-scoped lookup entity (colors/tags), simple one-to-many from `Project`.

**Commits**:
1. `feat: add ProjectMember association model with role column`
2. `feat: add Label model scoped to a project`
3. `feat: generate migration for project_members and labels`
4. `test: sanity-check relationships load correctly (a quick script or test)`

**Files created**: `app/models/project_member.py`, `app/models/label.py`,
`alembic/versions/xxxx_add_project_members_and_labels.py`

---

## Phase 3 — Authentication & Authorization

### Day 11 — Password hashing & registration

**Goal**: Never store a plaintext password; build `POST /auth/register`.

**Concepts**:
- Hashing is one-way (you can verify a password without ever being able to recover it); encryption
  is two-way. Passwords are always **hashed**, never merely encrypted.
- **Argon2** (via `pwdlib`) is the current recommended password hash — it's deliberately slow and
  memory-hard, which is exactly what you want against brute-force attacks.
- Why `UserOut` (the response schema) has no `password` field at all, rather than trusting
  yourself to remember to exclude it every time.

**Commits**:
1. `feat: add app/auth/hashing.py (Argon2 hash/verify via pwdlib)`
2. `feat: add schemas/user.py (UserCreate, UserOut)`
3. `feat: add POST /auth/register`
4. `docs: SETUP.md — pwdlib install noted here`

**Files created**: `app/auth/__init__.py`, `app/auth/hashing.py`, `app/schemas/user.py`,
`app/routers/auth.py`, `app/services/user_service.py`

### Day 12 — JWTs & the login endpoint

**Goal**: Understand JWTs; build `POST /auth/login`.

**Concepts**:
- A JWT is three base64 segments — `header.payload.signature` — and it's **signed, not
  encrypted**. Anyone can decode and read the payload; what they *can't* do without your secret
  key is forge a valid signature. This trips up almost every beginner — don't put secrets inside
  the JWT payload itself.
- The `exp` claim and why tokens expire.
- `OAuth2PasswordRequestForm`: the login endpoint accepts `application/x-www-form-urlencoded` data
  (username/password fields), not JSON — that's the OAuth2 "password flow" spec, and it's also
  exactly what Swagger UI's built-in "Authorize" button expects.

**Commits**:
1. `feat: add app/auth/jwt.py (create_access_token, decode_access_token)`
2. `feat: add POST /auth/login using OAuth2PasswordRequestForm`
3. `docs: explain JWT structure and signed-vs-encrypted in README`

**Files created**: `app/auth/jwt.py`, `app/schemas/token.py`

### Day 13 — Protecting routes: the current-user dependency

**Goal**: Build `get_current_user` and put it in front of a route.

**Concepts**:
- `OAuth2PasswordBearer` tells FastAPI (and `/docs`) where to send the token and how to read it
  off the `Authorization: Bearer <token>` header.
- Dependencies can depend on other dependencies — `get_current_user` depends on both the token
  extractor and `get_db`, and every protected route just depends on `get_current_user`. This
  composability is the payoff of FastAPI's DI system.
- 401 (not authenticated at all) vs 403 (authenticated, but not allowed) — a distinction you'll
  need precisely on Day 14.

**Commits**:
1. `feat: add get_current_user dependency`
2. `feat: add GET /auth/me`
3. `test: register/login/me happy path + wrong password + missing token`

**Files created**: `app/auth/dependencies.py`, `tests/test_auth.py`

### Day 14 — Authorization: project roles

**Goal**: Move from "logged in?" to "allowed to do *this*?"

**Concepts**:
- Authentication (who are you) vs authorization (what are you allowed to do) — a distinction
  that's easy to blur but matters a lot once real permissions exist.
- Build reusable dependencies (`require_project_member`, `require_project_owner`) so this logic
  isn't copy-pasted into every route that needs it.

**Commits**:
1. `feat: add require_project_member / require_project_owner dependencies`
2. `docs: document the authorization model in PROJECT_DETAILS.md`
3. `test: a non-member is rejected from a project's routes`

**Files created**: additions to `app/auth/dependencies.py`

---

## Phase 4 — Full CRUD + Business Logic

### Day 15 — Projects CRUD

**Goal**: The first complete resource: create/list/get/update/delete, owned by the current user.

**Concepts**:
- Why business logic (ownership checks, "can this be deleted") lives in a **service** function,
  not inline in the router — the router's job is HTTP concerns (parsing, status codes); the
  service's job is domain rules. This separation is what keeps routers readable as the app grows.

**Commits**:
1. `feat: add schemas/project.py (ProjectCreate, ProjectOut)`
2. `feat: add app/services/project_service.py`
3. `feat: add projects router (create/list/get/update/delete)`
4. `test: CRUD tests for projects`

**Files created**: `app/schemas/project.py`, `app/services/project_service.py`,
`app/routers/projects.py`, `tests/test_projects.py`

### Day 16 — Project membership endpoints

**Goal**: Add/remove members; only owners can manage membership.

**Commits**:
1. `feat: add POST/DELETE /projects/{id}/members`
2. `test: membership add/remove, including permission checks`

**Files created**: additions to `app/routers/projects.py`, `app/services/project_service.py`

### Day 17 — Tasks CRUD

**Goal**: The core resource of the whole app.

**Concepts**:
- Python `Enum` mapped to a SQLAlchemy `Enum` column for `status`/`priority` — the database
  itself now rejects an invalid status, not just your Pydantic schema.
- Nested resource routing: creating/listing tasks happens under `/projects/{id}/tasks` (a task
  always belongs to a project), but reading/updating a single task is just `/tasks/{id}` — you
  already know which project it's in from the row itself.

**Commits**:
1. `feat: add Task model + status/priority enums + migration`
2. `feat: add schemas/task.py`
3. `feat: add tasks router (create/list/get/update/delete)`
4. `test: task CRUD tests`

**Files created**: `app/models/task.py`, `app/schemas/task.py`, `app/routers/tasks.py`,
`app/services/task_service.py`, `tests/test_tasks.py`,
`alembic/versions/xxxx_create_tasks.py`

### Day 18 — Assignees, labels, and comments

**Goal**: Wire up the remaining relationships.

**Commits**:
1. `feat: add TaskAssignee + TaskLabel association tables + migration`
2. `feat: add assign/unassign and label attach/detach endpoints`
3. `feat: add Comment model + comments endpoints`
4. `test: assignment, labeling, and commenting tests`

**Files created**: `app/models/task_assignee.py`, `app/models/task_label.py`,
`app/models/comment.py`, `app/schemas/comment.py`, `app/routers/comments.py`,
`alembic/versions/xxxx_add_assignees_labels_comments.py`

### Day 19 — Filtering, search, sorting, pagination

**Goal**: Make list endpoints usable at real scale.

**Concepts**:
- Offset/limit pagination (`?skip=&limit=`) vs cursor-based pagination — we use offset for
  simplicity and explicitly note its weakness (pages shift if rows are inserted mid-scroll) rather
  than pretending it's flawless.
- A shared `Page[T]` response envelope (`items`, `total`, `page`, `page_size`) used by every list
  endpoint, instead of each one inventing its own shape.

**Commits**:
1. `feat: add pagination + filtering (status/priority/assignee) to GET tasks`
2. `feat: add a shared Page[T] response schema`
3. `test: pagination and filter tests`
4. `docs: mark Phase 4 complete`

**Files created**: `app/schemas/pagination.py`

---

## Phase 5 — Testing

### Day 20 — Real test infrastructure

**Goal**: Replace ad hoc tests with a proper isolated setup.

**Concepts**:
- Tests need their **own** database (never run tests against dev data — a failing test that
  half-completes shouldn't corrupt anything you care about).
- Fixture scope (`function` vs `session`) and why most of yours should be function-scoped for
  isolation, even though it's slower.
- `httpx.AsyncClient` + `ASGITransport` — the async-native replacement for the synchronous
  `TestClient` you used back on Day 5, needed because the app itself is fully async now.

**Commits**:
1. `chore: add pytest-asyncio and httpx, configure asyncio_mode`
2. `feat: add tests/conftest.py with db/session/client/user fixtures`
3. `refactor: migrate earlier tests onto the new fixture-based setup`

**Files created**: `tests/conftest.py` (rewritten), `pyproject.toml` (pytest config section)

### Day 21 — Coverage & edge cases

**Goal**: Close testing gaps and start measuring them.

**Commits**:
1. `test: edge cases — expired token, wrong role, not-found chains`
2. `chore: add pytest-cov and a coverage command`
3. `docs: mark Phase 5 complete`

---

## Phase 6 — Background Jobs

### Day 22 — FastAPI `BackgroundTasks` (the simple case first)

**Goal**: Understand the simplest "don't block the response" tool before reaching for a real queue.

**Concepts**:
- `BackgroundTasks` runs *after* the response is sent, but still in the same process — no
  retries, no persistence, and the work is lost if the server restarts mid-task. Understanding
  these limits is what makes Day 23's upgrade to Celery make sense instead of feeling arbitrary.

**Commits**:
1. `feat: log an ActivityLog entry via BackgroundTasks on task create/update`
2. `feat: add ActivityLog model + migration`
3. `test: activity log entries are created`

**Files created**: `app/models/activity_log.py`, `alembic/versions/xxxx_add_activity_log.py`

### Day 23 — Celery + Redis: a real task queue

**Goal**: Graduate to a queue with retries and persistence.

**Concepts**:
- A **message broker** (Redis here) sits between "something that wants work done" and "a worker
  process that does it" — decoupled, so the API process doesn't need the worker to be healthy to
  keep responding to requests.
- Celery's `@app.task` decorator, `.delay()`/`.apply_async()`, and running a worker as a *separate
  process* (`celery -A app.tasks.celery_app worker`).

**Commits**:
1. `chore: add redis service to docker-compose.yml`
2. `feat: add app/tasks/celery_app.py + notify_task_assigned task`
3. `feat: trigger the Celery task from the task-assignment endpoint`
4. `docs: SETUP.md — celery + redis install/run instructions`

**Files created**: `app/tasks/__init__.py`, `app/tasks/celery_app.py`, `app/tasks/notifications.py`

---

## Phase 7 — Caching

### Day 24 — Redis caching for the dashboard endpoint

**Goal**: Learn the read-through cache pattern and — the genuinely hard part — invalidation.

**Concepts**:
- Why cache at all: `GET /projects/{id}/dashboard` runs an aggregation query (counts by status,
  overdue tasks) that's cheap once but wasteful if hit constantly for data that rarely changes
  second-to-second.
- Cache key design (`dashboard:{project_id}`), TTL as a safety net, and **explicit invalidation**
  (delete the key whenever a task in that project changes) as the correctness-critical piece — a
  TTL alone would mean stale dashboards for however long the TTL is.

**Commits**:
1. `feat: add GET /projects/{id}/dashboard (uncached first)`
2. `feat: add redis-backed caching with a TTL`
3. `feat: invalidate the cache key on task create/update/delete in that project`
4. `test: cache hit/miss/invalidation tests`

**Files created**: `app/core/cache.py`, `app/routers/dashboard.py`

---

## Phase 8 — Real-time with WebSockets

### Day 25 — WebSocket basics

**Goal**: Understand what a WebSocket is for, with the simplest possible example first.

**Concepts**:
- HTTP is request/response — the client always speaks first. A **WebSocket** is a persistent,
  bidirectional connection: after the initial handshake, either side can send a message at any
  time. This is what makes "push a live update to the browser" possible without the browser
  polling every few seconds.
- `accept()` / `receive_text()` / `send_text()` and the connection lifecycle
  (`WebSocketDisconnect`).

**Commits**:
1. `feat: add a minimal /ws/echo route to learn the mechanics`
2. `docs: explain WebSocket vs HTTP request/response vs polling`

**Files created**: `app/ws/__init__.py`, `app/routers/ws_echo.py`

### Day 26 — Live task-board updates

**Goal**: Broadcast real task events to everyone viewing a project.

**Concepts**:
- The **connection manager** pattern: track which WebSocket connections are subscribed to which
  project, so a broadcast only reaches the right audience.
- Wiring broadcasts *in* from existing REST endpoints — the WebSocket layer doesn't duplicate
  business logic, it just announces that something the REST API already did has happened.

**Commits**:
1. `feat: add app/ws/manager.py (per-project ConnectionManager)`
2. `feat: add /ws/projects/{id} route`
3. `feat: broadcast task create/update/delete events from the tasks router`
4. `docs: mark Phase 8 complete; note a manual testing method (browser console or websocat)`

**Files created**: `app/ws/manager.py`, `app/routers/ws_projects.py`

---

## Phase 9 — API Hardening

### Day 27 — Rate limiting & consistent error handling

**Goal**: Protect the API from abuse; make errors predictable for consumers.

**Concepts**:
- Rate limiting concept (fixed-window here, via `slowapi`) — why login/register specifically need
  it most (credential-stuffing / brute-force targets).
- Custom exception handlers so every error response has the same JSON shape
  (`{"detail": ..., "error_code": ...}`), regardless of which part of the app raised it — an API
  consumer should never have to guess the error format per-endpoint.

**Commits**:
1. `chore: add slowapi, rate limit auth endpoints`
2. `feat: add global exception handlers for a consistent error shape`
3. `test: rate limit and error-shape tests`

**Files created**: `app/core/rate_limit.py`, `app/core/exception_handlers.py`

### Day 28 — Structured logging & request correlation

**Goal**: Understand why `print()` debugging doesn't survive contact with production.

**Concepts**:
- Structured (JSON) logs are machine-parseable — you can query "every log line for request X"
  instead of grepping free-text.
- A request-ID middleware stamps every incoming request with a unique ID, attached to every log
  line produced while handling it — this is how you trace one user's failing request through a
  system with many log lines interleaved from concurrent requests.

**Commits**:
1. `feat: add request-id middleware`
2. `feat: switch app logging to structured JSON logs`
3. `docs: mark Phase 9 complete`

**Files created**: `app/core/middleware.py`, `app/core/logging.py`

---

## Phase 10 — Observability

### Day 29 — Health checks & metrics

**Goal**: Understand liveness vs readiness, and what `/metrics` is for.

**Concepts**:
- **Liveness** ("is the process running at all") vs **readiness** ("can it actually serve a
  request right now" — e.g. is the DB reachable). Orchestrators (Docker healthchecks, Kubernetes)
  use these differently: a failed liveness check gets the process restarted; a failed readiness
  check just gets it pulled out of the traffic rotation.
- `/metrics` in Prometheus text format — the standard way infrastructure scrapes numeric
  time-series data (request counts, latencies) out of a running service.

**Commits**:
1. `feat: add /health (liveness) and /health/ready (readiness, checks DB+Redis)`
2. `feat: add /metrics via prometheus-fastapi-instrumentator`
3. `docs: SETUP.md — optional local Prometheus/Grafana note`

**Files created**: `app/routers/health.py`

---

## Phase 11 — Deployment & CI/CD

### Day 30 — Full Docker Compose stack

**Goal**: One command brings up everything: api, worker, postgres, redis.

**Concepts**:
- Multi-stage `Dockerfile`: a build stage with full tooling, a slim runtime stage — smaller,
  faster, more secure final image.
- `depends_on` + healthchecks in Compose: the api container shouldn't start accepting traffic
  before Postgres is actually ready to accept connections, not just "the container process
  started."
- The API and the Celery worker run from the **same image**, just different commands — one
  Dockerfile, two roles.

**Commits**:
1. `feat: add Dockerfile (multi-stage, uv-based)`
2. `feat: add docker-compose.yml services for api, worker, postgres, redis with healthchecks`
3. `docs: SETUP.md — docker compose up as the "just run everything" path`

**Files created**: `Dockerfile`, `docker-compose.yml` (extended)

### Day 31 — CI with GitHub Actions

**Goal**: Automated lint + test on every push.

**Concepts**:
- CI's purpose: catch a broken build *before* it's merged, from a clean environment — not "it
  worked on my machine."
- CI services (spinning up throwaway Postgres/Redis containers for the test job) mirror what
  Compose does locally, on purpose — the goal is that "works locally" and "works in CI" mean the
  same thing.

**Commits**:
1. `chore: add .github/workflows/ci.yml (lint + test, with postgres/redis services)`
2. `fix: address whatever the first CI run surfaces` — expect at least one real fix here; CI
   catching something local dev missed is the whole point, not a failure.
3. `docs: add a CI status badge to README`

**Files created**: `.github/workflows/ci.yml`

### Day 32 — Deploy to a real host + wrap-up

**Goal**: Get TaskFlow reachable on the internet, and reflect on what was built.

**Concepts**:
- Production config differs from dev on purpose: `DEBUG=false`, a real random `SECRET_KEY`,
  `CORS_ORIGINS` locked to your actual frontend domain instead of `*`.
- Picking a free-tier host (Render, Fly.io, or Railway all work for this stack) and understanding
  what "deployment" adds beyond Docker: a public domain, a place secrets live outside your laptop,
  and a process that restarts your app if it crashes.

**Commits**:
1. `chore: document production config differences`
2. `chore: deploy to chosen host, verify live /health and /docs`
3. `docs: final README pass — what TaskFlow does, what you learned, what you'd add next`

**Files created**: none new — this day is about the config differences and the deployment platform
setup, documented in README/SETUP rather than new app code.

---

## What's deliberately left out

To keep this a 6-week course and not a permanent job, some real-world concerns are named but not
built. Once you finish, these are the natural "season two" additions, and you'll have the
foundation to add any of them yourself:

- Refresh tokens / token revocation (we use short-lived access tokens only)
- File uploads (e.g. task attachments) via `python-multipart` + object storage
- Full-text search (Postgres `tsvector` or a dedicated search service)
- Multi-tenancy / organizations above the project level
- API versioning strategy
- A proper frontend (this course is backend-only, on purpose)
