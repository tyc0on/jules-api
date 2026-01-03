#!/usr/bin/env python3
"""Approve a plan for a session."""

import argparse
import json

from api import JulesClient


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("session_id")
    args = parser.parse_args()

    client = JulesClient()
    data = client.approve_plan(args.session_id)
    print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
