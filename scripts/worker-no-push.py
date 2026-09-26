#!/usr/bin/env python3
"""PreToolUse hook: workers may not run git push. Other agents and the lead are untouched.

Plugin agents can't carry their own hooks, so this runs for every Bash call in the
session and filters by agent_type.
"""
import json
import re
import sys

GIT_PUSH = re.compile(r"\bgit\b[^;&|\n]*\bpush\b")


def is_worker(agent_type):
    return agent_type.split(":")[-1] == "worker"


def main():
    payload = json.load(sys.stdin)
    command = payload.get("tool_input", {}).get("command", "")
    if not is_worker(payload.get("agent_type", "")) or not GIT_PUSH.search(command):
        return
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Workers don't push; commit locally and leave pushing to the user.",
    }}))


if __name__ == "__main__":
    main()
