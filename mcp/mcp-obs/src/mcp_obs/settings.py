"""Settings for the observability MCP server."""

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ObservabilitySettings:
    """Configuration for VictoriaLogs and VictoriaTraces endpoints."""

    victorialogs_url: str = "http://localhost:42010"
    victoriatraces_url: str = "http://localhost:42011"


def resolve_settings() -> ObservabilitySettings:
    """Resolve settings from environment variables."""
    return ObservabilitySettings(
        victorialogs_url=os.environ.get(
            "NANOBOT_VICTORIALOGS_URL", "http://localhost:42010"
        ),
        victoriatraces_url=os.environ.get(
            "NANOBOT_VICTORIATRACES_URL", "http://localhost:42011"
        ),
    )
