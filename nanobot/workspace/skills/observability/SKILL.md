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

### For "What went wrong?" or "Check system health" queries:

When the user asks about failures, follow this investigation flow:

1. **Check for recent errors first**
   - Call `logs_error_count(service="Learning Management Service", minutes=10)`
   - If count is 0, report "No recent errors found"

2. **Search error logs**
   - Call `logs_search(query='_time:10m service.name:"Learning Management Service" severity:ERROR', limit=10)`
   - Look for error messages and extract any `trace_id` from the results

3. **Fetch the trace**
   - If you found a `trace_id`, call `traces_get(trace_id="...")` 
   - Examine the span hierarchy to find where the failure occurred

4. **Summarize findings**
   - Combine log evidence (error message, timestamp, service) with trace evidence (failed span, operation)
   - Explain what failed, where, and why
   - Don't dump raw JSON — give a concise explanation

### For general health queries:

1. Start with `logs_error_count` for the last 10-30 minutes
2. If no errors, report the system appears healthy
3. If errors exist, investigate with `logs_search` and `traces_get`

### Query format tips:

- Use `_time:Xm` for time range (e.g., `_time:10m` for last 10 minutes)
- Use `service.name:"Service Name"` to filter by service
- Use `severity:ERROR` to filter errors
- Combine filters: `_time:10m service.name:"Learning Management Service" severity:ERROR`

### Response formatting:

- Summarize findings concisely — don't dump raw JSON
- For errors, mention: timestamp, service, error message, and trace ID if available
- For traces, describe the span hierarchy and highlight failed spans
- If no errors found, clearly state that the system appears healthy
- Always specify the time window in your response

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
