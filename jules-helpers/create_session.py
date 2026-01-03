#!/usr/bin/env python3
"""Create a session."""

import argparse
import json

from api import JulesClient


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--source", required=True, help="sources/{sourceId}")
    parser.add_argument("--starting-branch", required=True)
    parser.add_argument("--title")
    parser.add_argument("--require-plan-approval", action="store_true")
    parser.add_argument("--automation-mode", help="e.g. AUTO_CREATE_PR")
    args = parser.parse_args()

    payload = {
        "prompt": args.prompt,
        "sourceContext": {
            "source": args.source,
            "githubRepoContext": {"startingBranch": args.starting_branch},
        },
    }
    if args.title:
        payload["title"] = args.title
    if args.require_plan_approval:
        payload["requirePlanApproval"] = True
    if args.automation_mode:
        payload["automationMode"] = args.automation_mode

    client = JulesClient()
    data = client.create_session(payload)
    print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
