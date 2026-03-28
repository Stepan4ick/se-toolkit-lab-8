# mcp-obs

MCP server for observability tools (VictoriaLogs and VictoriaTraces).

## Tools

### logs_search
Search logs using LogsQL query.

**Parameters:**
- `query` (string): LogsQL query string, e.g., `_time:10m service.name:"backend" severity:ERROR`
- `limit` (int, optional): Max results to return (default: 100)

### logs_error_count
Count errors in logs over a time window.

**Parameters:**
- `service` (string, optional): Service name to filter
- `minutes` (int, optional): Time window in minutes (default: 60)

### traces_list
List recent traces.

**Parameters:**
- `service` (string, optional): Service name to filter
- `limit` (int, optional): Max traces to return (default: 20)

### traces_get
Get a specific trace by ID.

**Parameters:**
- `trace_id` (string): Trace ID to fetch

## Environment Variables

- `NANOBOT_VICTORIALOGS_URL` — VictoriaLogs endpoint (default: `http://localhost:42010`)
- `NANOBOT_VICTORIATRACES_URL` — VictoriaTraces endpoint (default: `http://localhost:42011`)

## Usage

```bash
uv run python -m mcp_obs
```
