# Foolstack - Modern Django + Vue3 Template (2026 Edition)

A high-performance, developer-first template for building modern web applications. Opinionated defaults, surgical architecture, and zero-config deployment.

## ✨ Features

- **Backend**: Django 6.0 REST API with **uv** for ultra-fast package management.
- **Frontend**: Vue 3 (Composition API) with **Bun 1.2**, Vite 8, and Tailwind 4.
- **Authentication**: JWT (SimpleJWT) with automatic token refresh.
- **Persistence**: PostgreSQL 16 (dev/prod parity) + Redis 7 (Caching & Sessions).
- **Architecture**:
    - **ULID Identity**: Models use time-sortable 26-char IDs by default.
    - **Native Async Tasks**: Django 6.0 Threaded Tasks (no extra worker container needed).
    - **Mobile First**: Built-in Progressive Web App (PWA) support with service workers.
- **Infrastructure**:
    - **Caddy 2**: Automatic SSL, single-domain routing, and production-ready SPA serving.
    - **Dockerized**: Optimized multi-stage builds for development and production.
    - **Makefile**: Unified CLI for the entire development lifecycle.

## 🚀 Quick Start

### 1. Requirements
- Docker & Docker Compose
- `uv` (for local Python IDE support)
- `bun` (for local JS IDE support)

### 2. Setup
```bash
make setup
```
This command will:
- Create your `.env` from the template.
- Generate a secure `SECRET_KEY`.
- Install local dependencies for IDE support.
- Build and start all Docker containers.

### 3. Initialize Database
```bash
make migrate
make superuser
```

### 4. Develop
Go to `https://localhost` (accept the self-signed certificate).
Hot reload is enabled for both backend and frontend.

## 🛠 Project Management

| Command | Description |
|---------|-------------|
| `make up` | Start services |
| `make down` | Stop services |
| `make logs` | View logs (`make logs s` for server only) |
| `make deps` | Sync local dependencies |
| `make shell` | Open Django shell |
| `make init <name>` | Rename project from template |

## 📦 Architecture Highlights

### Database & Identity
All models should inherit from `core.models.BaseModel`. It provides a `CharField` ID using ULIDs, ensuring your database remains performant as it scales while keeping IDs sortable and URL-friendly.

### Background Tasks
Django 6.0 Native Tasks are configured using the `ThreadedTaskBackend`. You can define tasks using the `@task()` decorator and execute them with `.enqueue()`. No separate `worker` process is required in Docker, simplifying your `docker-compose.yml`.

### PWA Readiness
The frontend is pre-configured with `vite-plugin-pwa`. See `PWA_SETUP.md` for instructions on generating icons and configuring the manifest for a native mobile experience.

## 📄 License
MIT

---
*Created by Yehuda Freedman*
