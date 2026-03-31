# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Question: "What is the agentic loop?"**

The agentic loop is the fundamental cycle that autonomous AI agents follow to accomplish tasks. It's the core reasoning pattern that enables agents to act independently toward goals.

**The Basic Loop:**

```
Perceive → Think → Act → Observe → (repeat)
```

1. **Perceive** - The agent gathers information about its environment (user input, tool outputs, file contents, API responses, system state)
2. **Think** - The agent processes information and plans (analyze current state, reason about what needs to be done, decide on next action, consider constraints and risks)
3. **Act** - The agent executes its decision (call a tool, send a message, modify a file, run a command)
4. **Observe** - The agent receives feedback (tool output or error messages, success/failure signals, new state information)

Then the loop repeats until the goal is achieved or the agent determines it cannot proceed.

**Question: "What labs are available in our LMS?"**

The bare agent (without MCP tools) responded by searching the workspace files and provided information from the lab documentation, not real backend data. It listed labs from the README and task files but couldn't access actual LMS data.

---

## Task 1B — Agent with LMS tools

**Question: "What labs are available?"**

The agent with MCP tools returned real data from the LMS backend:

| ID | Lab Title |
|----|-----------|
| 1 | Lab 01 – Products, Architecture & Roles |
| 2 | Lab 02 — Run, Fix, and Deploy a Backend Service |
| 3 | Lab 03 — Backend API: Explore, Debug, Implement, Deploy |
| 4 | Lab 04 — Testing, Front-end, and AI Agents |
| 5 | Lab 05 — Data Pipeline and Analytics Dashboard |
| 6 | Lab 06 — Build Your Own Agent |
| 7 | Lab 07 — Build a Client with an AI Coding Agent |
| 8 | lab-08 |

**Question: "Which lab has the lowest pass rate?"**

The agent called multiple MCP tools (`lms_labs`, `lms_completion_rate`) and returned:

| Lab | Completion Rate | Passed | Total |
|-----|-----------------|--------|-------|
| Lab 01 | 100.0% | 258 | 258 |
| Lab 02 | 89.1% | 131 | 147 |
| Lab 03 | 89.7% | 156 | 174 |
| Lab 04 | 96.7% | 238 | 246 |
| Lab 05 | 98.4% | 246 | 250 |
| Lab 06 | 98.4% | 241 | 245 |
| Lab 07 | 99.6% | 236 | 237 |
| Lab 08 | 0.0% | 0 | 0 |

**Answer: Lab 02 has the lowest pass rate at 89.1%** (among labs with actual submissions; Lab 08 shows 0% because it has no submissions yet).

---

## Task 1C — Skill prompt

**Question: "Show me the scores" (without specifying a lab)**

The agent with the skill prompt provided a comprehensive overview of all lab scores, including:

- Average scores by lab (all tasks combined)
- Detailed breakdown per lab with task-level statistics
- Key insights:
  - Highest performing lab: Lab 05 & Lab 07 (~67.3% avg)
  - Lowest performing lab: Lab 02 (~48.8% avg)
  - Most attempted task: Lab 01 "Lab setup" (2,970 attempts)
  - Toughest task: Lab 06 "The System Agent" (42.8% avg, 2,052 attempts)

The skill prompt taught the agent to:

- Format percentages as `XX.X%`
- Use markdown tables for comparative data
- Lead with the answer, then offer optional details
- Ask for clarification when a required parameter (like `lab`) is missing

## Task 2A — Deployed agent

**Nanobot gateway startup logs:**

```
nanobot-1  | Using config: /tmp/nanobot-config-resolved.json     
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  | 2026-03-27 12:02:11.182 | INFO     | nanobot.channels.manager:_init_channels:54 - WebChat channel enabled
nanobot-1  | ✓ Channels enabled: webchat                         
nanobot-1  | ✓ Heartbeat: every 1800s                            
nanobot-1  | 2026-03-27 12:02:12.077 | INFO     | nanobot.channels.manager:start_all:87 - Starting webchat channel...
nanobot-1  | 2026-03-27 12:02:12.134 | INFO     | nanobot_webchat.channel:start:72 - WebChat starting on 0.0.0.0:8765
```

The gateway started successfully with the WebChat channel enabled on port 8765.

## Task 2B — Web client

**WebSocket endpoint test:**

```
Request: {"content": "What can you do?"}

Response: Hi! I'm nanobot 🐈, your personal AI assistant. Here's what I can help you with:

## Core Capabilities

**📁 File Management**
- Read, write, and edit files
- Browse directories and explore your workspace

**🌐 Web Access**
- Search the web for information
- Fetch and extract content from URLs

**⚡ Command Execution**
- Run shell commands in your Linux environment
- Execute scripts and automate tasks

**⏰ Scheduling**
- Set one-time reminders
- Create recurring tasks and cron jobs

**💬 Communication**
- Send messages to Telegram, Discord, and other channels
- Spawn subagents for complex background tasks

## Available Skills

- **Memory** — Store and retrieve important information across sessions
- **Skill Creator** — Create or update custom agent skills
- **ClawHub** — Browse and install skills from the public registry
- **Cron** — Manage scheduled reminders and recurring tasks

## What I Value

- Accuracy over speed
- Transparency in my actions
- Your privacy and safety

Is there something specific you'd like help with? 😊
```

**Flutter web client:** Accessible at `http://localhost:42002/flutter`, protected by `NANOBOT_ACCESS_KEY`. Login successful, agent responds to queries via WebSocket.

## Task 3A — Structured logging

### Happy-path log excerpt (request_started → request_completed with status 200)

Querying VictoriaLogs at `http://localhost:42010/select/logsql/query?query=*&limit=3` returns structured JSON logs:

**Request to `/docs` (healthy):**

```json
{
  "_msg": "request_started",
  "_time": "2026-03-31T18:15:04.501837056Z",
  "event": "request_started",
  "method": "GET",
  "path": "/docs",
  "service.name": "Learning Management Service",
  "severity": "INFO",
  "trace_id": "ba6b88e9706e5ffe22fbf06386d6e7f0",
  "span_id": "34100597c9a82e7f",
  "otelServiceName": "Learning Management Service",
  "otelTraceID": "ba6b88e9706e5ffe22fbf06386d6e7f0",
  "otelSpanID": "34100597c9a82e7f"
}
```

```json
{
  "_msg": "request_completed",
  "_time": "2026-03-31T18:15:04.502991104Z",
  "event": "request_completed",
  "method": "GET",
  "path": "/docs",
  "status": "200",
  "duration_ms": "0",
  "service.name": "Learning Management Service",
  "severity": "INFO",
  "trace_id": "ba6b88e9706e5ffe22fbf06386d6e7f0",
  "span_id": "34100597c9a82e7f"
}
```

Key structured fields visible:
- `event` — The type of event (`request_started`, `request_completed`, `db_query`)
- `severity` — Log level (`INFO`, `ERROR`)
- `trace_id` / `span_id` — Correlation IDs for distributed tracing
- `service.name` — Service identifier
- `method`, `path`, `status` — HTTP request details
- `duration_ms` — Request duration

### Error-path log excerpt (db_query with error)

After stopping PostgreSQL and triggering a request to `/items/`, VictoriaLogs shows:

```json
{
  "_msg": "db_query",
  "_time": "2026-03-31T14:04:43.743758848Z",
  "event": "db_query",
  "operation": "select",
  "table": "item",
  "error": "[Errno -2] Name or service not known",
  "service.name": "Learning Management Service",
  "severity": "ERROR",
  "trace_id": "3f9165e36843cd21ba2c5f2968c47bc5",
  "span_id": "9a4d265a531d6491",
  "scope.name": "app.db.items"
}
```

Another error example (connection closed):

```json
{
  "_msg": "db_query",
  "_time": "2026-03-31T14:02:53.836495104Z",
  "event": "db_query",
  "operation": "select",
  "table": "item",
  "error": "(sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: connection is closed",
  "service.name": "Learning Management Service",
  "severity": "ERROR",
  "trace_id": "115ba066b54f3d7b3b65408a58f05a6a",
  "span_id": "8d45c25034dd87ab"
}
```

### VictoriaLogs UI screenshot

![VictoriaLogs UI Query](wiki/images/task3a-victorialogs-query.png)

*Screenshot shows the VictoriaLogs UI with structured logs from "Learning Management Service". The query filters by `service.name="Learning Management Service"` and displays 30 entries with timestamps and event types.*

---

## Task 3B — Traces

### Healthy trace analysis

![Healthy Trace](wiki/images/task3b-healthy-trace.png)

**Trace ID:** `a6a7d6a1f0093845e43e11c92c54f9c4`

**Span hierarchy description:**

The healthy trace shows a successful `GET /docs` request with the following span structure:

| Field | Value |
|-------|-------|
| `parent_span_id` | `1b16944820564ff2` |
| `resource_attr::service.name` | `Learning Management Service` |
| `resource_attr::telemetry.auto.version` | `0.61b0` |
| `resource_attr::telemetry.sdk.language` | `python` |
| `resource_attr::telemetry.sdk.name` | `opentelemetry` |
| `resource_attr::telemetry.sdk.version` | `1.40.0` |
| `scope_name` | `opentelemetry.instrumentation.fastapi` |
| `span_attr::asgi.event.type` | `http.response.start` |
| `span_attr::http.status_code` | `200` |
| `span_id` | `76642ddda8dd6b24` |
| `trace_id` | `a6a7d6a1f0093845e43e11c92c54f9c4` |

**What the trace shows:**
- The request was handled by the FastAPI instrumentation (`opentelemetry.instrumentation.fastapi`)
- HTTP response started successfully with status code `200`
- The span is part of a larger trace (has a `parent_span_id`)
- OpenTelemetry SDK version 1.40.0 with auto-instrumentation 0.61b0

### Error trace analysis

![Error Trace](wiki/images/task3b-error-trace.png)

**Trace ID:** (from error trace screenshot)

**Span details showing the failure:**

| Field | Value |
|-------|-------|
| `_msg` | `-` |
| `_stream` | `{name="GET /items/",resource_attr::service.name="Learning Management Service"}` |
| `_time` | `2026-03-31T14:02:53.813448496Z` |
| `duration` | `24461396` (nanoseconds: ~24ms) |
| `kind` | `2` (server span) |
| `name` | `GET /items/` |
| `resource_attr::service.name` | `Learning Management Service` |
| `span_attr::http.flavor` | `1.1` |
| `span_attr::http.host` | `172.19.0.8:8000` |
| `span_attr::http.method` | `GET` |
| `span_attr::http.route` | `/items/` |
| `span_attr::http.scheme` | `http` |
| `span_attr::http.server_name` | `localhost:42002` |
| `span_attr::http.status_code` | `404` |
| `span_attr::http.target` | `/items/` |
| `span_attr::http.url` | `http://localhost:42002/items/` |
| `span_attr::http.user_agent` | `curl/8.5.0` |
| `span_attr::net.host.port` | `8000` |
| `span_attr::net.peer.ip` | `172.19.0.10` |

**What the error trace shows:**
- The request to `/items/` returned HTTP status `404` (Not Found)
- The span duration was ~24ms
- This is a server span (`kind: 2`)
- The request came from internal Docker network (`172.19.0.10`)
- The error occurred during the database query phase (see Task 3A error logs with matching trace pattern)

**Comparing healthy vs error traces:**
- **Healthy**: Status code `200`, span completes normally with `http.response.start` event
- **Error**: Status code `404`, the underlying `db_query` event (visible in logs) shows `severity: ERROR` with "connection is closed" or "Name or service not known"

---

## Task 3C — Observability MCP tools

### Files created/modified

- **`mcp/mcp_lms/client.py`** — Added `ObservabilityClient` class with methods for querying VictoriaLogs and VictoriaTraces APIs.
- **`mcp/mcp_lms/server.py`** — Added tool handlers and registered all four observability tools.
- **`nanobot/config.json`** — Added `NANOBOT_VICTORIALOGS_URL` and `NANOBOT_VICTORIATRACES_URL` environment variables.
- **`nanobot/workspace/skills/observability/SKILL.md`** — Created observability skill prompt teaching the agent how to use the new tools.

### Tools registered

| Tool | Description | Parameters |
|------|-------------|------------|
| `logs_search` | Search logs in VictoriaLogs using LogsQL queries | `query` (default "*"), `limit` (default 20), `time_range` (default "1h") |
| `logs_error_count` | Count errors per service over a time window | `time_range` (default "1h") |
| `traces_list` | List recent traces, optionally filtered by service | `service`, `limit` (default 10), `time_range` (default "1h") |
| `traces_get` | Fetch a specific trace by ID | `trace_id` (required) |

### Test 1: Normal conditions (all services healthy)

**User query:** "Any errors in the last hour?"

**Agent tool calls:**
1. Called `logs_error_count` with `time_range="1h"`

**Tool response:**
```json
{
  "errors": [],
  "time_range": "1h"
}
```

**Agent response:**
> ✅ No errors detected in the last hour. The system appears to be running smoothly. All services (backend, postgres, caddy, nanobot, observability stack) are operating without logged errors.

### Test 2: Failure conditions (PostgreSQL stopped)

**Setup:** Ran `docker compose stop postgres` and triggered a few requests to `/items/`.

**User query:** "Any errors in the last hour?"

**Agent tool calls:**
1. Called `logs_error_count` with `time_range="1h"` → Found 2 errors
2. Called `logs_search` with `query="severity:ERROR"`, `time_range="1h"`, `limit=5`

**Tool response from `logs_error_count`:**
```json
{
  "errors": [
    {"service": "Learning Management Service", "count": 2}
  ],
  "time_range": "1h"
}
```

**Tool response from `logs_search` (excerpt):**
```json
{
  "entries": [
    {
      "timestamp": "2026-03-31T14:04:43.743758848Z",
      "message": "db_query",
      "level": "ERROR",
      "service": "Learning Management Service",
      "event": "db_query",
      "error": "[Errno -2] Name or service not known",
      "trace_id": "3f9165e36843cd21ba2c5f2968c47bc5"
    },
    {
      "timestamp": "2026-03-31T14:02:53.836495104Z",
      "message": "db_query",
      "level": "ERROR",
      "service": "Learning Management Service",
      "event": "db_query",
      "error": "connection is closed",
      "trace_id": "115ba066b54f3d7b3b65408a58f05a6a"
    }
  ],
  "total": 2,
  "query": "severity:ERROR"
}
```

**Agent response:**
> ⚠️ Found **2 errors** in the last hour from **Learning Management Service**:
>
> | Time | Error | Trace ID |
> |------|-------|----------|
> | 14:04:43 | `[Errno -2] Name or service not known` during `db_query` | `3f9165e36843cd21ba2c5f2968c47bc5` |
> | 14:02:53 | `connection is closed` during `db_query` | `115ba066b54f3d7b3b65408a58f05a6a` |
>
> Both errors occurred during database operations. This suggests the PostgreSQL database may be unreachable. Would you like me to fetch the full trace for either of these failures?

### Agent behavior pattern

The agent's behavior followed the expected pattern from the skill prompt:

1. **Called `logs_error_count`** to assess system health first
2. **On finding errors, called `logs_search`** with `query="severity:ERROR"` to retrieve details
3. **Extracted `trace_id`** from error logs and offered to fetch the full trace with `traces_get`
4. **Summarized findings concisely** — didn't dump raw JSON, used a markdown table

### Skill prompt summary

The skill at `nanobot/workspace/skills/observability/SKILL.md` teaches the agent to:

1. **Start with `logs_error_count`** for quick health assessment
2. **Use `logs_search`** with `query="level:error"` or `query="severity:ERROR"` to see error details
3. **Extract `trace_id`** from error logs and fetch full traces with `traces_get`
4. **Summarize findings** concisely — don't dump raw JSON
5. **Use appropriate time ranges** — "1h" for recent, "24h" or "7d" for historical

### LogsQL Query reference

- `*` — All logs
- `level:error` — Error-level logs
- `severity:ERROR` — Alternative error filter
- `service.name:"Learning Management Service"` — Filter by service
- `event:db_query` — Filter by event type
- `path:/items/` — Filter by request path
- Combine: `service.name:"backend" AND level:error`

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

### 1. Root cause identified

**Location:** `backend/app/routers/items.py`, lines 16-22

**The planted bug:** The `get_items` endpoint caught ALL exceptions (including database connection failures) and incorrectly returned HTTP 404 (Not Found) instead of HTTP 500 (Internal Server Error).

```python
# BEFORE (buggy code):
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    """Get all items."""
    try:
        return await read_items(session)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # ❌ Wrong: DB failures are not 404
            detail="Items not found",
        ) from exc
```

**Why this is wrong:** A 404 means "the requested resource doesn't exist" — but when PostgreSQL is down, the `/items/` endpoint exists, it just can't reach the database. This is a server error (500), not a missing resource (404).

### 2. Code fix

Changed the status code from `HTTP_404_NOT_FOUND` to `HTTP_500_INTERNAL_SERVER_ERROR` and updated the detail message:

```python
# AFTER (fixed code):
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    """Get all items."""
    try:
        return await read_items(session)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # ✅ Correct: DB failures are 500
            detail="Database error",
        ) from exc
```

### 3. Post-fix verification (DB failure returns 500)

After rebuilding and redeploying, stopped PostgreSQL and triggered `/items/`:

```bash
docker compose --env-file .env.docker.secret stop postgres
curl -v http://localhost:42002/items/ -H "Authorization: Bearer lms-adminvd-key"
```

**Response after fix:**
```
< HTTP/1.1 500 Internal Server Error
{"detail":"Database error"}
```

✅ **Confirmed:** The endpoint now correctly returns **500 Internal Server Error** instead of 404.

### 4. Healthy follow-up

After restarting PostgreSQL:

```bash
docker compose --env-file .env.docker.secret start postgres
curl -sf http://localhost:42002/items/ -H "Authorization: Bearer lms-adminvd-key"
```

**Response after recovery:**
```json
[{"title":"Lab 01 – Products, Architecture & Roles","id":1,"attributes":{},"description":"","type":"lab","parent_id":null,"created_at":"2026-03-27T10:43:36.144514"},...]
```

✅ **Confirmed:** The endpoint returns actual item data after PostgreSQL recovery.
