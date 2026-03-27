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

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
