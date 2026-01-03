#!/usr/bin/env python3
"""Get a single activity for a session."""

import argparse
import json

from api import JulesClient


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("session_id")
    parser.add_argument("activity_id")
    args = parser.parse_args()

    client = JulesClient()
    data = client.get_activity(args.session_id, args.activity_id)
    print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
