#!/usr/bin/env python3
"""Shared Jules API client helpers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests

BASE_URL = "https://jules.googleapis.com/v1alpha"
DEFAULT_TIMEOUT = 30


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


class JulesClient:
    def __init__(self, base_url: str = BASE_URL, api_key: Optional[str] = None) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        load_env(repo_root / ".env")
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or get_api_key()
        self.headers = {"x-goog-api-key": self.api_key}

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        resp = requests.get(
            f"{self.base_url}{path}",
            headers=self.headers,
            params=params or {},
            timeout=DEFAULT_TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json()

    def post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        resp = requests.post(
            f"{self.base_url}{path}",
            headers={**self.headers, "Content-Type": "application/json"},
            json=payload,
            timeout=DEFAULT_TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json()

    def list_sources(self, page_size: int = 100) -> Dict[str, Any]:
        return self.get("/sources", params={"pageSize": page_size})

    def list_sessions(self, page_size: int = 50, page_token: Optional[str] = None) -> Dict[str, Any]:
        params = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        return self.get("/sessions", params=params)

    def get_session(self, session_id: str) -> Dict[str, Any]:
        return self.get(f"/sessions/{session_id}")

    def delete_session(self, session_id: str) -> Dict[str, Any]:
        resp = requests.delete(
            f"{self.base_url}/sessions/{session_id}",
            headers=self.headers,
            timeout=DEFAULT_TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json() if resp.content else {}

    def list_activities(
        self, session_id: str, page_size: int = 50, page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        params = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        return self.get(f"/sessions/{session_id}/activities", params=params)

    def get_activity(self, session_id: str, activity_id: str) -> Dict[str, Any]:
        return self.get(f"/sessions/{session_id}/activities/{activity_id}")

    def create_session(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.post("/sessions", payload)

    def send_message(self, session_id: str, message: str) -> Dict[str, Any]:
        return self.post(
            f"/sessions/{session_id}:sendMessage",
            {"message": message},
        )

    def approve_plan(self, session_id: str) -> Dict[str, Any]:
        return self.post(f"/sessions/{session_id}:approvePlan", {})
