# Project Details — TaskFlow API

## What we're building

**TaskFlow** is a task & project tracking API — the backend for something like a small
Trello/Asana. It's a realistic, portfolio-worthy project: real auth, real relationships between
data, real background work, real caching, real deployment. Nothing here is a toy exercise you'd
throw away — every piece is something you'd find in an actual production backend, and by the end
you'll be able to explain *why* each piece exists, not just that it does.

Why this domain and not another CRUD app? Because it forces you to deal with the problems that
make backend engineering interesting:
- **Ownership & permissions** — a project has an owner and members; only some people can do some
  things. This is the seed of real authorization logic, not just "logged in or not."
- **Many-to-many relationships** — a task can have multiple assignees and multiple labels; a user
  can belong to multiple projects. You'll write real join tables, not just foreign keys.
- **State that changes over time** — tasks move through statuses, get commented on, get
  reassigned. This is what makes background jobs, notifications, and real-time updates actually
  useful instead of contrived.
- **Data worth aggregating** — a project dashboard (task counts by status, overdue tasks) is a
  natural excuse to learn caching, because naively recomputing it on every request is exactly the
  kind of thing that becomes a real performance problem in a real app.

## Tech stack (and why each piece is in here)

| Layer | Choice | Why this and not something else |
|---|---|---|
| Web framework | **FastAPI** | Async-native, automatic OpenAPI docs, Pydantic-based validation — the dominant modern choice for Python APIs |
| Language runtime | **Python 3.12+** | Current stable Python; FastAPI and its ecosystem target modern Python |
| Data validation | **Pydantic v2** | What FastAPI uses natively for request/response schemas |
| Database | **PostgreSQL** | The realistic default for production Python backends; real constraints, real relational features |
| ORM | **SQLAlchemy 2.0 (async)** | The standard Python ORM; async mode matches FastAPI's async request handling |
| Migrations | **Alembic** | SQLAlchemy's companion migration tool — how real teams evolve a schema without dropping tables |
| Package manager | **uv** | Fast, modern, the emerging standard for Python dependency management in 2025/2026 |
| Auth | **PyJWT + pwdlib (Argon2)** | JWT bearer tokens are the standard stateless API auth pattern; Argon2 is the current recommended password hash |
| Background jobs | **Celery + Redis** | The standard combination for "do this work, but not in the request/response cycle" |
| Caching | **Redis** | Same infrastructure as the job queue, reused for cached read paths |
| Real-time | **WebSockets** (via FastAPI/Starlette) | For live task-board updates — the realistic use case for WebSockets in a product like this |
| Testing | **pytest + pytest-asyncio + httpx** | The standard async-aware Python test stack |
| Containerization | **Docker + Docker Compose** | How you run Postgres/Redis locally without installing them natively, and how you'll eventually deploy |
| CI | **GitHub Actions** | Free, ubiquitous, the thing you'll encounter at almost any job |
| Linting | **ruff** | Fast, modern, replaces the old flake8/black/isort combo |

## Data model

```
User
 ├─ id, email, hashed_password, full_name, created_at
 │
 ├─< ProjectMember >── Project
 │     (role: owner | member)      ├─ id, name, description, owner_id, created_at
 │                                 │
 │                                 ├─< Label (id, name, color, project_id)
 │                                 │
 │                                 └─< Task
 │                                       ├─ id, title, description, status, priority,
 │                                       │  due_date, project_id, created_by, created_at, updated_at
 │                                       ├─< TaskAssignee >── User  (many-to-many)
 │                                       ├─< TaskLabel >──── Label (many-to-many)
 │                                       └─< Comment (id, body, author_id, created_at)
 │
 ├─< ActivityLog  (project_id, task_id, user_id, action, created_at)   — written by background jobs
 └─< Notification (user_id, message, read, created_at)                 — written by background jobs,
                                                                          pushed live over WebSocket
```

`status` is one of `todo`, `in_progress`, `done`. `priority` is one of `low`, `medium`, `high`.
`role` (on `ProjectMember`) is `owner` or `member` — this is the whole authorization model to
start: owners can do anything in their project, members have restricted permissions.

## API surface (built incrementally across the curriculum — see CURRICULUM.md)

```
Auth
  POST   /auth/register
  POST   /auth/login
  GET    /auth/me

Projects
  GET    /projects
  POST   /projects
  GET    /projects/{project_id}
  PATCH  /projects/{project_id}
  DELETE /projects/{project_id}
  POST   /projects/{project_id}/members
  DELETE /projects/{project_id}/members/{user_id}

Labels
  GET    /projects/{project_id}/labels
  POST   /projects/{project_id}/labels

Tasks
  GET    /projects/{project_id}/tasks      (filter by status/priority/assignee, paginated)
  POST   /projects/{project_id}/tasks
  GET    /tasks/{task_id}
  PATCH  /tasks/{task_id}
  DELETE /tasks/{task_id}
  POST   /tasks/{task_id}/assignees/{user_id}
  DELETE /tasks/{task_id}/assignees/{user_id}
  POST   /tasks/{task_id}/labels/{label_id}
  DELETE /tasks/{task_id}/labels/{label_id}

Comments
  GET    /tasks/{task_id}/comments
  POST   /tasks/{task_id}/comments

Dashboard
  GET    /projects/{project_id}/dashboard   (cached: counts by status, overdue tasks)

Notifications
  GET    /notifications
  POST   /notifications/{id}/read

Real-time
  WS     /ws/projects/{project_id}          (live task create/update/delete events)

Ops
  GET    /health
  GET    /metrics
```

## Repo layout (target shape — grows incrementally, day by day)

```
fastapi-backend/
├── README.md
├── SETUP.md
├── PROJECT_DETAILS.md
├── CURRICULUM.md
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/
├── app/
│   ├── main.py                 # FastAPI() instance, lifespan, router registration
│   ├── config.py                # pydantic-settings
│   ├── database.py              # async engine/session
│   ├── models/                  # SQLAlchemy models, one file per entity
│   ├── schemas/                 # Pydantic request/response models
│   ├── routers/                 # one file per resource
│   ├── services/                # business logic, kept out of routers
│   ├── auth/                    # password hashing, JWT, current-user dependency
│   ├── tasks/                   # Celery app + background job definitions
│   ├── ws/                      # WebSocket connection manager
│   └── core/                    # logging, middleware, rate limiting, exception handlers
└── tests/
    ├── conftest.py
    └── ...
```

You won't create all of this on day one — `CURRICULUM.md` introduces each folder exactly when
it's needed, and explains why it exists at that point.

## Non-functional goals (introduced progressively, not day one)

- Every list endpoint is paginated.
- Every error response has a consistent shape.
- Every request gets a request ID (for log correlation).
- Public endpoints are rate-limited.
- Secrets never live in code — only in `.env` (gitignored) and `.env.example` documents the shape.
- The whole stack (API, Postgres, Redis, Celery worker) runs with one `docker compose up`.
- CI runs lint + tests on every push.
