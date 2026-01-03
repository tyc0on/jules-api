#!/usr/bin/env python3
"""List sources."""

import argparse
import json

from api import JulesClient


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--page-size", type=int, default=100)
    args = parser.parse_args()

    client = JulesClient()
    data = client.list_sources(page_size=args.page_size)
    print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
