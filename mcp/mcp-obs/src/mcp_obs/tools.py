"""Tool schemas, handlers, and registry for the observability MCP server."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from mcp.types import Tool
from pydantic import BaseModel, Field

from mcp_obs.client import ObservabilityClient


class LogsSearchParams(BaseModel):
    """Parameters for searching logs."""

    query: str = Field(
        description="LogsQL query string, e.g., '_time:10m service.name:\"backend\" severity:ERROR'"
    )
    limit: int = Field(default=100, ge=1, le=1000, description="Max results to return")


class LogsErrorCountParams(BaseModel):
    """Parameters for counting errors."""

    service: str | None = Field(
        default=None, description="Service name to filter (e.g., 'Learning Management Service')"
    )
    minutes: int = Field(default=60, ge=1, description="Time window in minutes")


class TracesListParams(BaseModel):
    """Parameters for listing traces."""

    service: str | None = Field(default=None, description="Service name to filter")
    limit: int = Field(default=20, ge=1, le=100, description="Max traces to return")


class TracesGetParams(BaseModel):
    """Parameters for getting a specific trace."""

    trace_id: str = Field(description="Trace ID to fetch")


ToolPayload = BaseModel | list[dict] | dict
ToolHandler = Callable[[ObservabilityClient, BaseModel], Awaitable[ToolPayload]]


@dataclass(frozen=True, slots=True)
class ToolSpec:
    """Specification for an MCP tool."""

    name: str
    description: str
    model: type[BaseModel]
    handler: ToolHandler

    def as_tool(self) -> Tool:
        schema = self.model.model_json_schema()
        schema.pop("$defs", None)
        schema.pop("title", None)
        return Tool(name=self.name, description=self.description, inputSchema=schema)


async def _logs_search(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    """Search logs using LogsQL query."""
    if not isinstance(args, LogsSearchParams):
        raise TypeError(f"Expected LogsSearchParams, got {type(args).__name__}")
    return await client.logs_query(args.query, args.limit)


async def _logs_error_count(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    """Count errors over a time window."""
    if not isinstance(args, LogsErrorCountParams):
        raise TypeError(f"Expected LogsErrorCountParams, got {type(args).__name__}")
    return await client.logs_error_count(args.service, args.minutes)


async def _traces_list(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    """List recent traces."""
    if not isinstance(args, TracesListParams):
        raise TypeError(f"Expected TracesListParams, got {type(args).__name__}")
    return await client.traces_list(args.service, args.limit)


async def _traces_get(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    """Get a specific trace by ID."""
    if not isinstance(args, TracesGetParams):
        raise TypeError(f"Expected TracesGetParams, got {type(args).__name__}")
    result = await client.traces_get(args.trace_id)
    return result if result else {"error": "Trace not found"}


TOOL_SPECS = (
    ToolSpec(
        "logs_search",
        "Search logs using LogsQL query. Use _time:Xm for time range, service.name for service, severity for level.",
        LogsSearchParams,
        _logs_search,
    ),
    ToolSpec(
        "logs_error_count",
        "Count errors in logs over a time window. Optionally filter by service name.",
        LogsErrorCountParams,
        _logs_error_count,
    ),
    ToolSpec(
        "traces_list",
        "List recent traces. Optionally filter by service name.",
        TracesListParams,
        _traces_list,
    ),
    ToolSpec(
        "traces_get",
        "Get a specific trace by ID. Returns full span hierarchy.",
        TracesGetParams,
        _traces_get,
    ),
)

TOOLS_BY_NAME = {spec.name: spec for spec in TOOL_SPECS}
