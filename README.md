<div align="center">

# 🌟 Gelt

### *Modern Django + Vue3 Full-Stack Platform*

[![Django](https://img.shields.io/badge/Django-5.2.4-092E20?logo=django)](https://djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0-4FC08D?logo=vue.js)](https://vuejs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://docker.com/)

**Production-ready full-stack web application platform with JWT authentication, Docker containerization, and automatic HTTPS**

**📖 [Complete Documentation](./docs/README.md)** • **🚀 [Quick Start](#-quick-start)**

</div>

---

## 🎯 What is Gelt?

Gelt is a sophisticated, containerized full-stack application framework that combines Django's robust backend with Vue.js's modern frontend experience. Designed for rapid development and production deployment, it provides everything you need to build scalable web applications.

### ⚡ Key Highlights

- **🚀 One-Command Setup** - From zero to running in under 60 seconds
- **🔐 JWT Authentication** - Email-based auth with custom user model built-in
- **🐳 Fully Containerized** - Docker + Compose for consistent environments
- **🔒 HTTPS by Default** - Automatic SSL certificates via Caddy proxy
- **⚡ Hot Reload** - Instant updates during development
- **📦 Production Ready** - Optimized builds and deployment strategies

## 🛠️ Tech Stack


| **Layer**     | **Technology**     | **Purpose**                                  |
|:--------------|:-------------------|:---------------------------------------------|
| **Frontend**  | Vue 3 + Vite       | Modern SPA with lightning-fast builds        |
| **Backend**   | Django 5.2.4 + DRF | Robust REST API with admin interface         |
| **Auth**      | JWT (Simple JWT)   | Stateless authentication with token rotation |
| **Database**  | SQLite/PostgreSQL  | Flexible data storage                        |
| **Proxy**     | Caddy 2.8          | Automatic HTTPS and reverse proxy            |
| **Container** | Docker + Compose   | Consistent dev/prod environments             |



## 📋 Prerequisites

- **Docker** 20.10+ & **Docker Compose** 2.0+ (I use podman, btw)
- **Git** 2.25+
- **Make** (optional, for convenience commands)

## 🚀 Quick Start

### ⚡ One-Command Setup

```bash
git clone https://github.com/yourusername/gelt.git
cd gelt
make setup
```

This single command will:
- ✅ Create secure environment configuration
- ✅ Build and start all Docker services
- ✅ Initialize database with migrations
- ✅ Prompt you to create an admin user

### 🌐 Access Your Application

| **Service**  | **URL**                         | **Purpose**      |
|:-------------|:--------------------------------|:-----------------|
| **Frontend** | http://localhost                | Main application |
| **API**      | http://api.localhost:8000       | REST endpoints   |
| **Admin**    | http://api.localhost:8000/admin | Django admin     |

### 🛠️ Development Commands

```bash
make up           # Start services
make down         # Stop services
make logs         # View logs
make migrate      # Run migrations
make superuser    # Create admin user
make shell-django # Access Django container
```

## 📚 Documentation

For comprehensive guides, API references, and advanced topics:

**➡️ [View Complete Documentation](./docs/README.md)**

### Quick Links

- **[🔐 Authentication Guide](./docs/authentication.md)** - JWT implementation details
- **[🛠️ API Reference](./docs/api-reference.md)** - Complete endpoint documentation  
- **[🏗️ Architecture Overview](./docs/README.md#architecture-overview)** - System design deep-dive
- **[🚢 Production Deployment](./docs/deployment.md)** - Scaling and deployment strategies
