#!/usr/bin/env python3
"""List recurring Jules sessions for a GitHub repo by grouping sessions by title+prompt."""

from __future__ import annotations

import datetime
import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests

BASE_URL = "https://jules.googleapis.com/v1alpha"
DEFAULT_REPO = "OWNER/REPO"


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"").strip("'")
        os.environ.setdefault(key, value)


def get_api_key() -> str:
    api_key = os.environ.get("JULES_API_KEY")
    if not api_key:
        raise SystemExit("Missing JULES_API_KEY in .env")
    return api_key


def list_sources(headers: Dict[str, str]) -> List[Dict[str, object]]:
    sources: List[Dict[str, object]] = []
    page_token: Optional[str] = None
    for _ in range(10):
        params = {"pageSize": 100}
        if page_token:
            params["pageToken"] = page_token
        resp = requests.get(f"{BASE_URL}/sources", headers=headers, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        sources.extend(data.get("sources", []))
        page_token = data.get("nextPageToken")
        if not page_token:
            break
    return sources


def find_source_name(sources: List[Dict[str, object]], repo: str) -> str:
    for source in sources:
        gh = source.get("githubRepo") or source.get("github_repo") or {}
        repo_name = gh.get("fullName") or gh.get("full_name") or gh.get("name")
        if repo_name and repo_name.endswith(repo):
            return str(source.get("name") or source.get("id"))
    raise SystemExit(f"Source for {repo} not found in sources list.")


def list_sessions(headers: Dict[str, str]) -> List[Dict[str, object]]:
    sessions: List[Dict[str, object]] = []
    page_token: Optional[str] = None
    for _ in range(40):
        params = {"pageSize": 50}
        if page_token:
            params["pageToken"] = page_token
        resp = requests.get(f"{BASE_URL}/sessions", headers=headers, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        sessions.extend(data.get("sessions", []))
        page_token = data.get("nextPageToken")
        if not page_token:
            break
    return sessions


def parse_time(value: Optional[str]) -> Optional[datetime.datetime]:
    if not value:
        return None
    try:
        return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def group_sessions(sessions: List[Dict[str, object]]) -> List[Tuple[Tuple[str, str], List[Dict[str, object]]]]:
    groups: Dict[Tuple[str, str], List[Dict[str, object]]] = defaultdict(list)
    for session in sessions:
        key = (session.get("title") or "", session.get("prompt") or "")
        groups[key].append(session)
    return sorted(groups.items(), key=lambda item: len(item[1]), reverse=True)


def main() -> None:
    repo = os.environ.get("JULES_REPO", DEFAULT_REPO)
    load_env(Path(__file__).resolve().parents[1] / ".env")
    api_key = get_api_key()

    headers = {"x-goog-api-key": api_key}

    sources = list_sources(headers)
    source_name = find_source_name(sources, repo)

    sessions = list_sessions(headers)
    filtered = [
        session
        for session in sessions
        if (session.get("sourceContext") or {}).get("source") == source_name
    ]

    print(f"Source: {source_name}")
    print(f"Total sessions for repo: {len(filtered)}")
    print("Potential schedules (grouped by title/prompt):")

    for (title, prompt), items in group_sessions(filtered):
        times = [parse_time(item.get("createTime")) for item in items]
        times = [t for t in times if t]
        latest = max(times).isoformat() if times else "unknown"
        count = len(items)
        title_display = title if title else "<no title>"
        prompt_display = (prompt[:120] + "…") if len(prompt) > 120 else prompt
        print(
            f"- count={count} latest={latest} title={title_display} prompt={prompt_display}"
        )


if __name__ == "__main__":
    main()
