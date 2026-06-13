FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml poetry.lock* ./
RUN uv pip install --system -r <(uv export --format requirements.txt 2>/dev/null || echo "")

COPY . .

FROM python:3.12-slim AS runtime

WORKDIR /app

RUN useradd -m appuser && \
    apt-get update && apt-get install -y --no-install-recommends curl postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local /usr/local
COPY . .

RUN mkdir -p static media logs && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK CMD curl -f http://localhost:8000/health/ || exit 1

CMD ["gunicorn","config.wsgi:application","--bind","0.0.0.0:8000"]
