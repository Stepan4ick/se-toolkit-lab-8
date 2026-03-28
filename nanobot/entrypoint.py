#!/usr/bin/env python3
"""Entrypoint for nanobot gateway in Docker."""

import json
import os
import sys
from pathlib import Path

def resolve_config():
    config_path = Path(__file__).parent / "config.json"
    resolved_path = Path(__file__).parent / "config.resolved.json"
    
    with open(config_path, "r") as f:
        config = json.load(f)
    
    # Override from env vars
    if os.environ.get("LLM_API_KEY"):
        config["providers"]["custom"]["apiKey"] = os.environ["LLM_API_KEY"]
    if os.environ.get("LLM_API_BASE_URL"):
        config["providers"]["custom"]["apiBase"] = os.environ["LLM_API_BASE_URL"]
    if os.environ.get("LLM_API_MODEL"):
        config["agents"]["defaults"]["model"] = os.environ["LLM_API_MODEL"]
    if os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS"):
        config["gateway"]["host"] = os.environ["NANOBOT_GATEWAY_CONTAINER_ADDRESS"]
    if os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT"):
        config["gateway"]["port"] = int(os.environ["NANOBOT_GATEWAY_CONTAINER_PORT"])

    # MCP LMS
    if os.environ.get("NANOBOT_LMS_BACKEND_URL"):
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = os.environ["NANOBOT_LMS_BACKEND_URL"]
    if os.environ.get("NANOBOT_LMS_API_KEY"):
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = os.environ["NANOBOT_LMS_API_KEY"]

    # MCP OBS
    if os.environ.get("NANOBOT_VICTORIALOGS_URL"):
        config["tools"]["mcpServers"]["obs"]["env"]["NANOBOT_VICTORIALOGS_URL"] = os.environ["NANOBOT_VICTORIALOGS_URL"]
    if os.environ.get("NANOBOT_VICTORIATRACES_URL"):
        config["tools"]["mcpServers"]["obs"]["env"]["NANOBOT_VICTORIATRACES_URL"] = os.environ["NANOBOT_VICTORIATRACES_URL"]

    # MCP WEBCCHAT
    if os.environ.get("NANOBOT_WEBCCHAT_UI_RELAY_URL"):
        config["tools"]["mcpServers"]["webchat"]["env"]["NANOBOT_WEBCCHAT_UI_RELAY_URL"] = os.environ["NANOBOT_WEBCCHAT_UI_RELAY_URL"]
    if os.environ.get("NANOBOT_WEBCCHAT_UI_RELAY_TOKEN"):
        config["tools"]["mcpServers"]["webchat"]["env"]["NANOBOT_WEBCCHAT_UI_RELAY_TOKEN"] = os.environ["NANOBOT_WEBCCHAT_UI_RELAY_TOKEN"]

    # WebChat channel
    if os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS"):
        config["channels"]["webchat"]["host"] = os.environ["NANOBOT_WEBCHAT_CONTAINER_ADDRESS"]
    if os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT"):
        config["channels"]["webchat"]["port"] = int(os.environ["NANOBOT_WEBCHAT_CONTAINER_PORT"])

    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Using config: {resolved_path}", file=sys.stderr)
    return str(resolved_path)

def main():
    resolved_config = resolve_config()
    workspace = str(Path(__file__).parent / "workspace")
    os.execvp("nanobot", ["nanobot", "gateway", "--config", resolved_config, "--workspace", workspace])

if __name__ == "__main__":
    main()
