# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Question: "What is the agentic loop?"**
> The **agentic loop** is the fundamental cycle that autonomous AI agents follow to accomplish tasks. It's the core reasoning and action pattern that enables agents to work independently toward goals.
> 
> The Basic Loop:
> 1. Perceive — Observe the current state of the environment or context
> 2. Think/Reason — Analyze the situation, plan next steps, make decisions
> 3. Act — Execute actions (call tools, modify files, send messages, etc.)
> 4. Observe Results — See the outcome of the action
> 5. Repeat — Continue until the goal is achieved

**Question: "What labs are available in our LMS?"**
> Based on my exploration of the workspace, here are the available labs in your LMS:
> 
> Required Labs (Lab 8):
> 1. Task 1 — Set Up the Agent
> 2. Task 2 — Deploy and Connect a Web Client
> 3. Task 3 — Give the Agent New Eyes
> 4. Task 4 — Diagnose a Failure and Make the Agent Proactive
> 
> (Answered from local repo files, not real LMS backend data)

## Task 1B — Agent with LMS tools

**Question: "What labs are available?"**
> Here are the available labs from the LMS system:
> 
> | ID | Title |
> |----|-------|
> | 1 | Lab 01 – Products, Architecture & Roles |
> | 2 | Lab 02 — Run, Fix, and Deploy a Backend Service |
> | 3 | Lab 03 — Backend API: Explore, Debug, Implement, Deploy |
> | 4 | Lab 04 — Testing, Front-end, and AI Agents |
> | 5 | Lab 05 — Data Pipeline and Analytics Dashboard |
> | 6 | Lab 06 — Build Your Own Agent |
> | 7 | Lab 07 — Build a Client with an AI Coding Agent |
> | 8 | lab-08 |

**Question: "Is the LMS backend healthy?"**
> Yes, the LMS backend is healthy! It's currently tracking 56 items.

## Task 1C — Skill prompt

**Question: "Show me the scores"**
> I'll help you check the scores! First, let me get the list of available labs so you can choose which one you'd like to see.
> 
> Here are the available labs:
> 1. Lab 01 – Products, Architecture & Roles
> 2. Lab 02 — Run, Fix, and Deploy a Backend Service
> 3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
> 4. Lab 04 — Testing, Front-end, and AI Agents
> 5. Lab 05 — Data Pipeline and Analytics Dashboard
> 6. Lab 06 — Build Your Own Agent
> 7. Lab 07 — Build a Client with an AI Coding Agent
> 8. Lab 08 — lab-08
> 
> Which lab would you like to see the scores for?

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

**Nanobot startup logs:**
```
<!-- Add logs from: docker compose --env-file .env.docker.secret logs nanobot --tail 50 -->
```

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

**Screenshot:**
<!-- ![Flutter chat conversation](path/to/screenshot.png) -->

## Task 3A — Structured logging

**Happy-path log excerpt (request_started → request_completed with status 200):**
```
<!-- Add logs from: docker compose --env-file .env.docker.secret logs backend --tail 30 -->
```

**Error-path log excerpt (db_query with error when PostgreSQL stopped):**
```
<!-- Add error logs here -->
```

**VictoriaLogs query screenshot:**
<!-- ![VictoriaLogs query](path/to/victorialogs-screenshot.png) -->

## Task 3B — Traces

**Healthy trace screenshot:**
<!-- ![Healthy trace](path/to/healthy-trace-screenshot.png) -->

**Error trace screenshot:**
<!-- ![Error trace](path/to/error-trace-screenshot.png) -->

## Task 3C — Observability MCP tools

**Normal conditions — "Any LMS backend errors in the last 10 minutes?":**
> <!-- Add agent response here -->

**Failure conditions (PostgreSQL stopped) — "Any LMS backend errors in the last 10 minutes?":**
> <!-- Add agent response here -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
