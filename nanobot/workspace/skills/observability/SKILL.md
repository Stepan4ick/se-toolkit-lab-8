---
name: observability
description: Use observability MCP tools to investigate logs and traces
always: true
---

You have access to observability MCP tools that query VictoriaLogs and VictoriaTraces.

## Available Tools

- `logs_search` — Search logs using LogsQL query
- `logs_error_count` — Count errors over a time window
- `traces_list` — List recent traces
- `traces_get` — Get a specific trace by ID

## For "What went wrong?" queries:

1. Call `logs_error_count(service="Learning Management Service", minutes=10)`
2. If count > 0: call `logs_search` to find errors and extract `trace_id`
3. Call `traces_get(trace_id="...")` to see the failure context
4. Summarize: combine log evidence + trace evidence, explain what failed

## For health check queries:

1. Start with `logs_error_count` for last 10-30 minutes
2. If no errors: report system is healthy
3. If errors: investigate with `logs_search` and `traces_get`

## Response format:

- Be concise, don't dump raw JSON
- Mention: timestamp, service, error message, trace_id if available
- Always specify the time window
