ARG REGISTRY_PREFIX_DOCKER_HUB

FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy workspace files
COPY --from=workspace pyproject.toml uv.lock /app/
COPY --from=workspace mcp/mcp-lms /app/mcp/mcp-lms
COPY --from=workspace mcp/mcp-obs /app/mcp/mcp-obs
COPY --from=workspace nanobot /app/nanobot
COPY --from=workspace nanobot-websocket-channel /app/nanobot-websocket-channel

# Sync
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package nanobot

# --- Stage 2 ---
ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Use nonroot user (no custom UID/GID - let Docker handle it)
COPY --from=builder --chown=1000:1000 /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER 1000
WORKDIR /app/nanobot

CMD ["python", "/app/nanobot/entrypoint.py"]
