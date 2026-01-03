#!/usr/bin/env python3
"""List activities for a session."""

import argparse
import json

from api import JulesClient


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("session_id")
    parser.add_argument("--page-size", type=int, default=50)
    parser.add_argument("--page-token")
    args = parser.parse_args()

    client = JulesClient()
    data = client.list_activities(
        args.session_id, page_size=args.page_size, page_token=args.page_token
    )
    print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
