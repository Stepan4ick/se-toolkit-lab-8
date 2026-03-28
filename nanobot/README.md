# Nanobot Agent - Lab 8

Nanobot agent configured for the LMS backend with MCP tools.

## Quick Start

```bash
# Run agent in CLI mode
uv run nanobot agent --logs --session cli:test -c ./config.json -m "Hello"

# Run with LMS tools
NANOBOT_LMS_BACKEND_URL=http://localhost:42001 NANOBOT_LMS_API_KEY=my_LMS_api_key uv run nanobot agent --logs -c ./config.json -m "What labs are available?"
```

## Configuration

- `config.json` - Main configuration file
- `workspace/` - Agent workspace with skills and memory
- `../mcp/mcp-lms/` - LMS MCP server
