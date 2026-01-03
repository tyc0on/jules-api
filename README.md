# Jules API Helpers (Agent-First)

This folder packages a small, agent-friendly CLI and workflow for interacting with the Jules REST API. It is designed to be used by agents via `AGENTS.md`, which documents the canonical usage patterns and constraints.

## What this is for

- Provide a thin, repeatable API surface for agents to list sources, sessions, and activities.
- Create sessions, send messages, and approve plans through the documented Jules REST endpoints.
- Approximate “scheduled tasks” by grouping recurring sessions (since schedules are not exposed in the public API).

## What’s included

- `AGENTS.md` – Agent instructions and preferred workflows.
- `jules-helpers/` – CLI helpers built around the Jules REST API.
- `jules-schedules/` – A focused helper that lists recurring sessions for a repo.

## Install

Requirements:
- Python 3.9+
- Network access to `https://jules.googleapis.com`
- Jules API key

Install dependencies:
```
python -m pip install requests pymysql
```

Environment:
Create a `.env` file in the repo root with:
```
JULES_API_KEY=your_key_here
```
Optional (only if you plan to push via HTTPS in automation):
```
GITHUB_PAT=your_github_token
```

## Quick start (agents)

Read `AGENTS.md` first. Then use the helper CLIs in `jules-helpers/` to call the API. The helpers read `JULES_API_KEY` from environment variables.

## Current limitations

- The public Jules REST API does not expose schedule create/update/delete endpoints.
- “Scheduled tasks” must be inferred from sessions (title/prompt grouping).
- No built-in helpers for pagination across all pages beyond the defaults (extend if needed).

## Repository intent

This is not a full SDK. It’s a minimal, practical interface designed to be reliable for agent workflows and simple automation, with documentation that keeps agents on the same rails.
