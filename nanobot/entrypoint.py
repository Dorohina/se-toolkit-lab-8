#!/usr/bin/env python
"""
Entrypoint for nanobot gateway in Docker.

Resolves environment variables into config.json at runtime, then launches
`nanobot gateway`. This allows Docker to pass config via env vars.
"""

import json
import os
import sys
from pathlib import Path


def resolve_config():
    """Read config.json, inject env vars, write resolved config."""
    config_path = Path("/app/nanobot/config.json")
    workspace_path = Path("/app/nanobot/workspace")

    with open(config_path) as f:
        config = json.load(f)

    # Resolve LLM provider API key and base URL from env vars
    llm_api_key = os.environ.get("LLM_API_KEY")
    llm_api_base_url = os.environ.get("LLM_API_BASE_URL")
    llm_api_model = os.environ.get("LLM_API_MODEL")

    if llm_api_key:
        config["providers"]["custom"]["apiKey"] = llm_api_key
    if llm_api_base_url:
        config["providers"]["custom"]["apiBase"] = llm_api_base_url
    if llm_api_model:
        config["agents"]["defaults"]["model"] = llm_api_model

    # Resolve gateway host/port from env vars
    gateway_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT")

    if gateway_host:
        config["gateway"]["host"] = gateway_host
    if gateway_port:
        config["gateway"]["port"] = int(gateway_port)

    # Resolve webchat channel host/port from env vars
    webchat_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT")

    if webchat_host:
        config["channels"]["webchat"]["host"] = webchat_host
    if webchat_port:
        config["channels"]["webchat"]["port"] = int(webchat_port)

    # Resolve MCP server env vars (LMS backend URL and API key)
    lms_backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL")
    lms_api_key = os.environ.get("NANOBOT_LMS_API_KEY")

    if lms_backend_url or lms_api_key:
        mcp_env = config["tools"]["mcp_servers"]["lms"]["env"]
        if lms_backend_url:
            mcp_env["NANOBOT_LMS_BACKEND_URL"] = lms_backend_url
        if lms_api_key:
            mcp_env["NANOBOT_LMS_API_KEY"] = lms_api_key

    # Write resolved config to a temp file
    resolved_path = Path("/tmp/nanobot-config-resolved.json")
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    return str(resolved_path), str(workspace_path)


def main():
    resolved_config, workspace = resolve_config()

    # Launch nanobot gateway
    os.execvp("nanobot", ["nanobot", "gateway", "--config", resolved_config, "--workspace", workspace])


if __name__ == "__main__":
    main()
