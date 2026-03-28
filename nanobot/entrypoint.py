#!/usr/bin/env python3
"""Entrypoint for nanobot gateway in Docker.

Resolves environment variables into config at runtime, then launches nanobot gateway.
"""

import json
import os
import sys
from pathlib import Path


def resolve_config() -> str:
    """Read config.json, override fields from env vars, write config.resolved.json."""
    config_path = Path(__file__).parent / "config.json"
    resolved_path = Path(__file__).parent / "config.resolved.json"
    workspace_path = Path(__file__).parent / "workspace"

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Override LLM provider settings from env vars
    llm_api_key = os.environ.get("LLM_API_KEY")
    llm_api_base = os.environ.get("LLM_API_BASE_URL")
    llm_api_model = os.environ.get("LLM_API_MODEL")

    if llm_api_key:
        config["providers"]["custom"]["apiKey"] = llm_api_key
    if llm_api_base:
        config["providers"]["custom"]["apiBase"] = llm_api_base
    if llm_api_model:
        config["agents"]["defaults"]["model"] = llm_api_model

    # Override gateway settings from env vars
    gateway_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT")

    if gateway_host:
        config["gateway"]["host"] = gateway_host
    if gateway_port:
        config["gateway"]["port"] = int(gateway_port)

    # Override MCP server env vars for LMS
    lms_backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL")
    lms_api_key = os.environ.get("NANOBOT_LMS_API_KEY")

    if "tools" in config and "mcpServers" in config["tools"]:
        if "lms" in config["tools"]["mcpServers"]:
            if "env" not in config["tools"]["mcpServers"]["lms"]:
                config["tools"]["mcpServers"]["lms"]["env"] = {}
            if lms_backend_url:
                config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = lms_backend_url
            if lms_api_key:
                config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = lms_api_key

    # Override MCP server env vars for webchat UI delivery
    webchat_relay_url = os.environ.get("NANOBOT_WEBCCHAT_UI_RELAY_URL")
    webchat_relay_token = os.environ.get("NANOBOT_WEBCCHAT_UI_RELAY_TOKEN")

    if "tools" in config and "mcpServers" in config["tools"]:
        if "webchat" in config["tools"]["mcpServers"]:
            if "env" not in config["tools"]["mcpServers"]["webchat"]:
                config["tools"]["mcpServers"]["webchat"]["env"] = {}
            if webchat_relay_url:
                config["tools"]["mcpServers"]["webchat"]["env"]["NANOBOT_WEBCCHAT_UI_RELAY_URL"] = webchat_relay_url
            if webchat_relay_token:
                config["tools"]["mcpServers"]["webchat"]["env"]["NANOBOT_WEBCCHAT_UI_RELAY_TOKEN"] = webchat_relay_token

    # Override MCP server env vars for observability (VictoriaLogs and VictoriaTraces)
    victorialogs_url = os.environ.get("NANOBOT_VICTORIALOGS_URL")
    victoriatraces_url = os.environ.get("NANOBOT_VICTORIATRACES_URL")

    if "tools" in config and "mcpServers" in config["tools"]:
        if "obs" in config["tools"]["mcpServers"]:
            if "env" not in config["tools"]["mcpServers"]["obs"]:
                config["tools"]["mcpServers"]["obs"]["env"] = {}
            if victorialogs_url:
                config["tools"]["mcpServers"]["obs"]["env"]["NANOBOT_VICTORIALOGS_URL"] = victorialogs_url
            if victoriatraces_url:
                config["tools"]["mcpServers"]["obs"]["env"]["NANOBOT_VICTORIATRACES_URL"] = victoriatraces_url

    # Override channel settings from env vars
    webchat_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT")
    webchat_enabled = os.environ.get("NANOBOT_WEBCHAT_ENABLED", "true").lower() == "true"

    if "channels" not in config:
        config["channels"] = {}

    if webchat_enabled:
        config["channels"]["webchat"] = {
            "enabled": True,
            "allowFrom": ["*"]
        }
        if webchat_host:
            config["channels"]["webchat"]["host"] = webchat_host
        if webchat_port:
            config["channels"]["webchat"]["port"] = int(webchat_port)

    # Write resolved config
    with open(resolved_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"Using config: {resolved_path}", file=sys.stderr)
    return str(resolved_path)


def main():
    """Resolve config and exec into nanobot gateway."""
    resolved_config = resolve_config()
    workspace = str(Path(__file__).parent / "workspace")

    # Exec into nanobot gateway - replaces this process
    os.execvp("nanobot", ["nanobot", "gateway", "--config", resolved_config, "--workspace", workspace])


if __name__ == "__main__":
    main()
