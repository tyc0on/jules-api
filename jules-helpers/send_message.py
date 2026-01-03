#!/usr/bin/env python3
"""Send a message to a session."""

import argparse
import json

from api import JulesClient


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("session_id")
    parser.add_argument("--message", required=True)
    args = parser.parse_args()

    client = JulesClient()
    data = client.send_message(args.session_id, args.message)
    print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
