# -- Build Stage --
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS python-build-stage

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies only (Cache Layer)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy application code and sync project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# -- Run Stage --
FROM python:3.13-slim-bookworm AS python-run-stage

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Create non-root user
RUN addgroup --system fastapi && adduser --system --ingroup fastapi fastapi 

# Install runtime-only system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq5 \
    gettext \
    wait-for-it \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment and app from the builder
COPY --from=python-build-stage --chown=fastapi:fastapi /app /app

# Setup start script
COPY --chown=fastapi:fastapi ./compose/production/fastapi/start /start
RUN sed -i 's/\r$//g' /start && chmod +x /start

USER fastapi

ENTRYPOINT [ "/start" ]