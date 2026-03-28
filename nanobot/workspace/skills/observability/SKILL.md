---
name: observability
description: Use observability MCP tools to investigate logs and traces
always: true
---

You have access to observability MCP tools that query VictoriaLogs and VictoriaTraces. Here's how to use them effectively:

## Available Tools

### Log tools (VictoriaLogs)
- `logs_search` — Search logs using LogsQL query. Returns structured log entries.
- `logs_error_count` — Count errors over a time window. Returns aggregated stats.

### Trace tools (VictoriaTraces)
- `traces_list` — List recent traces. Optionally filter by service name.
- `traces_get` — Get a specific trace by ID. Returns full span hierarchy.

## Strategy Rules

1. **When the user asks about errors or failures:**
   - First call `logs_error_count` with the relevant service name and time window to see if there are recent errors
   - If errors exist, call `logs_search` with a query like `_time:10m service.name:"Learning Management Service" severity:ERROR` to inspect the actual error messages
   - Look for `trace_id` in the error logs
   - If you find a `trace_id`, call `traces_get` to fetch the full trace and understand the failure context

2. **When the user asks about system health:**
   - Start with `logs_error_count` for the last 10-30 minutes
   - If there are no errors, report that the system appears healthy
   - If there are errors, investigate further with `logs_search`

3. **When the user provides a trace ID:**
   - Call `traces_get` directly with that ID
   - Explain the span hierarchy and where errors occurred

4. **Query format tips:**
   - Use `_time:Xm` for time range (e.g., `_time:10m` for last 10 minutes)
   - Use `service.name:"Service Name"` to filter by service
   - Use `severity:ERROR` to filter errors
   - Combine filters: `_time:10m service.name:"Learning Management Service" severity:ERROR`

5. **Response formatting:**
   - Summarize findings concisely — don't dump raw JSON
   - For errors, mention: timestamp, service, error message, and trace ID if available
   - For traces, describe the span hierarchy and highlight failed spans
   - If no errors found, clearly state that the system appears healthy

6. **Time windows:**
   - Use narrow windows (10-30 minutes) for recent issues
   - Use wider windows (1-6 hours) for historical analysis
   - Always specify the time window in your response so the user knows the scope

## Example Reasoning Flow

User: "Any LMS backend errors in the last 10 minutes?"

1. Call `logs_error_count(service="Learning Management Service", minutes=10)`
2. If count > 0:
   - Call `logs_search(query='_time:10m service.name:"Learning Management Service" severity:ERROR', limit=10)`
   - Extract `trace_id` from error logs
   - Call `traces_get(trace_id="...")` for the most recent error
   - Summarize: what failed, when, and in which service
3. If count = 0:
   - Report: "No errors found in the last 10 minutes for the LMS backend"
