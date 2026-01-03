#!/usr/bin/env python3
"""List recurring sessions (approx schedules) for a repo by grouping title+prompt."""

from __future__ import annotations

import argparse
import datetime
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from api import JulesClient

DEFAULT_REPO = "OWNER/REPO"


def parse_time(value: Optional[str]) -> Optional[datetime.datetime]:
    if not value:
        return None
    try:
        return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def find_source_name(sources: List[Dict[str, object]], repo: str) -> str:
    for source in sources:
        gh = source.get("githubRepo") or source.get("github_repo") or {}
        repo_name = gh.get("fullName") or gh.get("full_name") or gh.get("name")
        if repo_name and repo_name.endswith(repo):
            return str(source.get("name") or source.get("id"))
    raise SystemExit(f"Source for {repo} not found in sources list.")


def group_sessions(sessions: List[Dict[str, object]]) -> List[Tuple[Tuple[str, str], List[Dict[str, object]]]]:
    groups: Dict[Tuple[str, str], List[Dict[str, object]]] = defaultdict(list)
    for session in sessions:
        key = (session.get("title") or "", session.get("prompt") or "")
        groups[key].append(session)
    return sorted(groups.items(), key=lambda item: len(item[1]), reverse=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--page-size", type=int, default=50)
    parser.add_argument("--pages", type=int, default=40)
    args = parser.parse_args()

    client = JulesClient()

    sources = client.list_sources(page_size=100).get("sources", [])
    source_name = find_source_name(sources, args.repo)

    sessions: List[Dict[str, object]] = []
    page_token: Optional[str] = None
    for _ in range(args.pages):
        data = client.list_sessions(page_size=args.page_size, page_token=page_token)
        sessions.extend(data.get("sessions", []))
        page_token = data.get("nextPageToken")
        if not page_token:
            break

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
