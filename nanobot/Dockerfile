# Dockerfile for nanobot gateway
# Based on backend/Dockerfile pattern with uv multi-stage build

# ---
# Stage 1: Build the application in the `/app` directory
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
ARG APP_UID=1000
ARG APP_GID=1000

FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Disable Python downloads, use system interpreter
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy workspace root pyproject.toml and uv.lock for workspace resolution
COPY --from=workspace pyproject.toml uv.lock /app/

# Copy nanobot project files
COPY nanobot/pyproject.toml /app/nanobot/pyproject.toml

# Copy MCP packages that nanobot depends on
COPY mcp/mcp-lms/pyproject.toml /app/mcp/mcp-lms/pyproject.toml

# Sync nanobot package with its dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-workspace --package nanobot

# Copy the rest of nanobot source
COPY nanobot/ /app/nanobot/

# Copy MCP source for editable install
COPY mcp/ /app/mcp/

# Final sync to ensure all dependencies are installed
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package nanobot

# ---
# Stage 2: Final runtime image
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

# Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Create user with configurable UID/GID (matches host user for volume mounting)
ARG APP_UID=1000
ARG APP_GID=1000
RUN groupadd --system --gid ${APP_GID} nonroot \
    && useradd --system --gid ${APP_GID} --uid ${APP_UID} --create-home nonroot

# Copy the application from builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER nonroot

WORKDIR /app/nanobot

# Run nanobot gateway via entrypoint script
CMD ["python", "/app/nanobot/entrypoint.py"]
