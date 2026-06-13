# AI-Powered Document Intelligence Platform
Upload documents → extract knowledge → query with natural language

## Overview
This repository contains a full-stack AI-powered document intelligence platform.
It includes a Django backend, a Vite + React + TypeScript frontend, and a complete Docker Compose setup for local development and production-style deployment.

## Repository Structure

```
backend/
  Dockerfile
  manage.py
  config/
  documents/
frontend/
  Dockerfile
  package.json
  tsconfig.json
  vite.config.ts
  public/
  src/
    App.tsx
    main.tsx
    components/
    pages/
    api/
    types/
    assets/
docker-compose.yml
.dockerignore
.env.example
nginx.conf
Makefile
docker-setup.sh
README.md
```

## Frontend Overview

### Technologies
- **Vite**: Fast frontend build tool
- **React**: UI library
- **TypeScript**: Static typing
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **Lucide React**: Icons
- **ESLint**: Linting and formatting

### Frontend Structure

```
frontend/
├── src/
│   ├── App.tsx
│   ├── main.tsx
│   ├── pages/
│   ├── components/
│   ├── api/
│   ├── types/
│   ├── utils/
│   ├── styles/
│   └── assets/
├── public/
├── package.json
├── vite.config.ts
├── tsconfig.json
├── eslint.config.js
└── index.html
```

## Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- Node.js 20+ (for local frontend development)
- npm 10+ or yarn

## Environment Variables
Copy `.env.example` to `.env` and update values.

```env
# Django
SECRET_KEY=<generate-secure-random-string>
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database
DB_USER=postgres
DB_PASSWORD=<secure-password>
DB_NAME=ai_platform

# Cache
REDIS_PASSWORD=<secure-password>

# Document Store
MONGO_USERNAME=admin
MONGO_PASSWORD=<secure-password>
MONGO_DATABASE=ai_platform

# Storage
AI_STORAGE_ACCESS_KEY=<your-aistor-key>
AI_STORAGE_SECRET_KEY=<secure-aistor-secret>

# AI Services
OPENAI_API_KEY=<your-openai-api-key>
OPENAI_API_BASE=https://api.openai.com/v1

# Frontend
REACT_APP_API_URL=http://localhost:8000
NODE_ENV=production
```

## Quick Start

### Option 1: Automated Setup

```bash
chmod +x docker-setup.sh
./docker-setup.sh
```

This script will:
- create `.env` if needed
- build Docker images
- start services
- run initial migrations

### Option 2: Manual Docker Setup (recommended: Docker Compose plugin)

```bash
cp .env.example .env
docker compose build
docker compose up -d
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

### Option 3: Makefile Commands

```bash
make setup    # Complete setup
make up       # Start all services
make down     # Stop all services
make logs     # View logs
```

## Service Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Nginx (Optional)                         │
│              (Reverse Proxy, SSL/TLS, CDN)                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │          Your Applications            │
├────────┴─────────────┬──────────────┬─────────────┤
│                      │              │             │
│   Backend (Django)   │  Frontend    │   Nginx     │
│   REST API           │  (React)     │  Console    │
│                      │              │             │
├──────────────────────┴──────────────┴─────────────┤
│          Container Network (ai_network)          │
├──────────────────────────────────────────────────┤
│                  Support Services                │
│  ┌──────────┐  ┌────────┐  ┌─────────┐  ┌────┐ │
│  │ Backend  │  │Celery  │  │ Celery  │  │    │ │
│  │Database  │  │Worker  │  │ Beat    │  │    │ │
│  │(Postgres)│  │        │  │(Scheduler)  │    │ │
│  └──────────┘  └────────┘  └─────────┘  └────┘ │
│                                                  │
│  ┌──────────┐  ┌────────┐  ┌─────────┐        │
│  │ Postgres │  │ Redis  │  │ MongoDB │        │
│  │ Database │  │ Cache  │  │ Store   │        │
│  └──────────┘  └────────┘  └─────────┘        │
│                                                  │
│  ┌───────────────────────────────────────────┐ │
│  │     Aistor (S3-Compatible Storage)         │ │
│  │     - Document Storage                    │ │
│  │     - Model Files                         │ │
│  │     - Backup Data                         │ │
│  └───────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

## Service Endpoints

| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| Backend | 8000 | http://localhost:8000 | Django REST API |
| Django Admin | 8000 | http://localhost:8000/admin | Management interface |
| Frontend | 3000 | http://localhost:3000 | React application |
| Aistor API | 9000 | http://localhost:9000 | S3-compatible storage |
| Aistor Console | 9001 | http://localhost:9001 | Storage management |
| PostgreSQL | 5432 | localhost:5432 | Database |
| Redis | 6379 | localhost:6379 | Cache / broker |
| MongoDB | 27017 | localhost:27017 | Document store |

## Docker Commands

```bash
# Build services (using the modern Docker Compose plugin)
docker compose build

docker compose up -d

docker compose logs -f

docker compose down

docker compose down -v  # remove volumes too
```

## Frontend Local Development

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

### Frontend Scripts

```bash
npm run dev          # Start Vite dev server
npm run build        # Build production bundle
npm run preview      # Preview built app locally
npm run lint         # Run ESLint
npm run lint -- --fix  # Auto-fix lint issues
npx tsc --noEmit     # TypeScript check
```

### Frontend Docker

```bash
make frontend-build
make frontend-logs
make frontend-bash
```

## Frontend Docker Notes

- The frontend Dockerfile uses a multi-stage build.
- It builds the Vite app into `dist/`.
- Production container serves the app with `serve` on port `3000`.
- `REACT_APP_API_URL` is used to configure the backend URL.
- The frontend service includes a health check and depends on the backend service state.

## API Integration

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.REACT_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
```

## Development Workflow

### Creating Components

```tsx
import React from 'react';

interface MyComponentProps {
  title: string;
}

const MyComponent: React.FC<MyComponentProps> = ({ title }) => (
  <div>
    <h1>{title}</h1>
  </div>
);

export default MyComponent;
```

### Creating Pages

```tsx
import React from 'react';

const MyPage: React.FC = () => (
  <div className="page">
    <h1>My Page</h1>
  </div>
);

export default MyPage;
```

### API Data Hook Example

```ts
import { useEffect, useState } from 'react';
import api from '../services/api';

export const useDocuments = () => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        setLoading(true);
        const response = await api.get('/api/documents/');
        setDocuments(response.data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchDocuments();
  }, []);

  return { documents, loading, error };
};
```

## Common Commands

```bash
# Docker and services
make up
make down
make restart
make ps
make logs
make health

# Database
make migrate
make makemigrations
make createsuperuser

# Shells
make shell
make backend-bash
make db-shell
make redis-cli

# Testing and quality
make test
make test-coverage
make lint
make format
make type-check
```

## Production Considerations

- Set `DEBUG=False`
- Use strong secrets in `.env`
- Enable `ALLOWED_HOSTS` for production domains
- Use HTTPS / SSL certificates
- Restrict database network access
- Rotate storage credentials regularly
- Configure health checks and logging

## Security Checklist

- Generate a secure Django `SECRET_KEY`
- Protect `.env` from version control
- Use HTTPS for public access
- Enable CORS restrictions in production
- Use strong passwords for PostgreSQL, Redis, MongoDB, Aistor
- Monitor logs and alerts

## Troubleshooting

### Service Startup Issues

```bash
docker-compose logs
docker-compose logs backend
```

### Port Conflicts

```bash
lsof -i :8000
kill -9 <PID>
```

### Database Issues

```bash
docker-compose exec postgres pg_isready -U postgres
```

### Celery Issues

```bash
docker-compose logs celery_worker
```

### Aistor Issues

```bash
docker-compose exec aistor curl -f http://localhost:9000/minio/health/live
```

## Verification Checklist

- [ ] Containers are running (`make ps`)
- [ ] Backend API returns a response
- [ ] Frontend is accessible at `http://localhost:3000`
- [ ] Django admin is accessible at `http://localhost:8000/admin`
- [ ] Aistor console is accessible at `http://localhost:9001`
- [ ] Database, Redis and MongoDB are reachable
- [ ] Celery worker is processing tasks

## Resources

- [Docker Compose](https://docs.docker.com/compose/)
- [Django Deployment](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [Celery Docs](https://docs.celeryproject.org/en/stable/)
- [Aistor Docs](https://docs.min.io/)
- [React](https://react.dev/)
- [Vite](https://vitejs.dev/)
- [TypeScript](https://www.typescriptlang.org/)

---

> This `README.md` consolidates the information previously stored in `FRONTEND_SETUP.md`, `DOCKER_COMPLETE_SETUP.md`, `DOCKER_SETUP.md`, and `DOCKER_FRONTEND_UPDATES.md`.

## Overview

This repository contains an AI-powered document intelligence platform with a Django backend, Celery workers, document storage, and a Vite + React + TypeScript frontend.

The system is built to:
- Upload documents and store them securely
- Extract knowledge with embeddings and retrieval
- Query content using natural language
- Serve a modern React frontend with Docker support

## Table of Contents

- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Docker Deployment](#docker-deployment)
- [Frontend Development](#frontend-development)
- [Environment Variables](#environment-variables)
- [Services and Endpoints](#services-and-endpoints)
- [Common Commands](#common-commands)
- [Docker Frontend Updates](#docker-frontend-updates)
- [Production Considerations](#production-considerations)
- [Troubleshooting](#troubleshooting)
- [Security and Scaling](#security-and-scaling)
- [Resources](#resources)
- [Verification Checklist](#verification-checklist)

## Project Structure

```
backend/
  Dockerfile
  manage.py
  config/
  documents/
frontend/
  Dockerfile
  package.json
  tsconfig.json
  vite.config.ts
  public/
  src/
    App.tsx
    main.tsx
    components/
    pages/
    api/
    types/
```

## Quick Start

### Option 1: Automated Setup (Recommended)

```bash
chmod +x docker-setup.sh
./docker-setup.sh
```

This script will:
- Create a `.env` file if needed
- Build Docker images
- Start all services
- Run initial backend migrations

### Option 2: Manual Setup

```bash
cp .env.example .env
docker-compose build
docker-compose up -d
```

Then run migrations:

```bash
docker-compose exec backend python manage.py migrate
```

Create a superuser:

```bash
docker-compose exec backend python manage.py createsuperuser
```

### Option 3: Makefile Shortcuts

```bash
make setup
make up
make down
make logs
```

## Docker Deployment

This project uses Docker Compose to orchestrate the full stack, including:
- PostgreSQL
- Redis
- MongoDB
- Aistor
- Django backend
- Celery worker
- Celery beat
- React frontend
- Optional Nginx reverse proxy

### Build and Run

```bash
docker-compose build
docker-compose up -d
```

### Stop and Remove

```bash
docker-compose down
```

To remove volumes as well:

```bash
docker-compose down -v
```

## Frontend Development

The frontend is built with Vite, React, and TypeScript.

### Local Development

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in the browser.

### Production Build

```bash
cd frontend
npm run build
npm run preview
```

### Available Scripts

```bash
npm run dev
npm run build
npm run preview
npm run lint
npm run lint -- --fix
npx tsc --noEmit
```

### Frontend Configuration

Create a `.env` file in `frontend/` with:

```env
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=AI Document Intelligence Platform
```

Access these values in code with `import.meta.env.VITE_API_URL`.

### API Integration Example

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
```

## Environment Variables

Essential variables in the repository root `.env`:

```env
# Django
SECRET_KEY=<generate-secure-random-string>
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database
DB_USER=postgres
DB_PASSWORD=<secure-password>
DB_NAME=ai_platform

# Cache
REDIS_PASSWORD=<secure-password>

# Document Store
MONGO_USERNAME=admin
MONGO_PASSWORD=<secure-password>
MONGO_DATABASE=ai_platform

# Storage
AI_STORAGE_ACCESS_KEY=<your-aistor-key>
AI_STORAGE_SECRET_KEY=<secure-aistor-secret>

# AI Services
OPENAI_API_KEY=<your-openai-api-key>
OPENAI_API_BASE=https://api.openai.com/v1

# Frontend
REACT_APP_API_URL=http://localhost:8000
NODE_ENV=production
```

## Services and Endpoints

| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| Backend | 8000 | http://localhost:8000 | Django REST API |
| Django Admin | 8000 | http://localhost:8000/admin | Management interface |
| Frontend | 3000 | http://localhost:3000 | React application |
| Aistor API | 9000 | http://localhost:9000 | S3-compatible storage API |
| Aistor Console | 9001 | http://localhost:9001 | Aistor management |
| PostgreSQL | 5432 | localhost:5432 | Database |
| Redis | 6379 | localhost:6379 | Cache/Message broker |
| MongoDB | 27017 | localhost:27017 | Document store |

## Common Commands

### Docker and Compose

```bash
docker-compose ps
docker-compose logs -f
docker-compose exec backend bash
docker-compose exec frontend sh
```

### Django Management

```bash
docker-compose exec backend python manage.py shell
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py test
docker-compose exec backend python manage.py migrate
```

### Frontend and Linting

```bash
cd frontend
npm install
npm run lint
npm run lint -- --fix
npm run build
```

### Makefile Targets

```bash
make logs
make logs-backend
make logs-celery
make frontend-build
make frontend-install
make frontend-lint
make frontend-fix-lint
make frontend-bash
make frontend-logs
```

## Docker Frontend Updates

The frontend Docker integration is configured for Vite production output with `dist/` and includes:
- multi-stage build with `npm ci`
- TypeScript compilation via `npm run build`
- `serve -s dist -l 3000`
- Docker healthcheck for the frontend container
- production environment variables
- read-only source/public volume mounts for optimization

The frontend service is wired to depend on backend health and use SPA routing in `nginx.conf` with:

```nginx
error_page 404 =200 /index.html;
```

## Production Considerations

### Security

- Use strong passwords in `.env`
- Set `DEBUG=False` in production
- Use a secure `SECRET_KEY`
- Restrict allowed hosts
- Enable HTTPS and update `nginx.conf` paths for certificates

### Performance

- Adjust Gunicorn worker count
- Configure Redis memory limits
- Tune database connection pooling
- Optimize Aistor and static file serving

### Monitoring

- Aggregate logs centrally
- Use error tracking (e.g. Sentry)
- Monitor container resource usage
- Enable service health checks

### Scaling

- Run multiple backend instances behind Nginx
- Use a dedicated database server
- Add load balancing and caching layers
- Consider Kubernetes or Swarm for orchestration

## Troubleshooting

### Port Already in Use

```bash
lsof -i :8000
kill -9 <PID>
```

### Database Connection Issues

```bash
docker-compose exec postgres pg_isready -U postgres
docker-compose logs postgres
```

### Celery Issues

```bash
docker-compose exec redis redis-cli ping
docker-compose logs celery_worker
docker-compose exec backend celery -A config inspect active
```

### Aistor Connection Issues

```bash
docker-compose exec aistor curl -f http://localhost:9000/minio/health/live
docker-compose logs -f aistor
```

### Frontend Build Failures

```bash
npm install --legacy-peer-deps
docker-compose build --no-cache frontend
```

### 404 on Page Refresh

Ensure SPA routing is configured properly in Nginx and that `index.html` is served for unknown frontend routes.

## Security and Scaling

### Development

- Debug mode enabled by default
- Simplified credentials for local use
- CORS can be permissive in development

### Production

- Use environment-specific `.env` files
- Enable HTTPS only
- Rotate keys regularly
- Harden Aistor access policies and bucket policies

### Scaling Strategies

- Horizontal: multiple backend replicas, load balancer, separate database
- Vertical: more CPU/memory, optimized query plans, caching
- Performance: asset hashing, caching headers, code splitting, bundle analysis

## Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Guide](https://docs.djangoproject.com/en/stable/howto/deployment/index/)
- [Celery Documentation](https://docs.celeryproject.org/en/stable/)
- [Aistor Documentation](https://docs.min.io/)
- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Axios Documentation](https://axios-http.com/)

## Verification Checklist

- [ ] All containers running: `make ps`
- [ ] Backend accessible: `curl http://localhost:8000/api/`
- [ ] Frontend accessible: `http://localhost:3000`
- [ ] Admin panel accessible: `http://localhost:8000/admin`
- [ ] Aistor console accessible: `http://localhost:9001`
- [ ] Database connection works: `make db-shell`
- [ ] Redis connection works: `make redis-cli`
- [ ] Celery worker is active: `docker-compose logs celery_worker`

---