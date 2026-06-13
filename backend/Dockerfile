FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    postgresql-client \
    libpq-dev \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy project files for dependency install
COPY pyproject.toml ./
COPY poetry.lock* ./

# Install Poetry and project dependencies (no virtualenv)
RUN pip install --no-cache-dir "poetry>=1.6" && \
    poetry config virtualenvs.create false && \
    if [ -f poetry.lock ]; then \
        poetry install --no-dev --no-interaction --no-ansi; \
    else \
        poetry install --no-interaction --no-ansi; \
    fi

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p static media logs

# Create a non-root user and set ownership
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app/backend
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -fsS http://localhost:8000/healthz || exit 1 || true

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
