# -*- coding: utf-8 -*-
"""Minimal Slack connectivity test for THINC v4.0.

Sends a single test message to confirm that SLACK_BOT_TOKEN is valid and
that the bot has permission to post in the target channel.

Usage
-----
    export SLACK_BOT_TOKEN=xoxb-...   # set in your shell or CI secret store
    export SLACK_CHANNEL_ID=C0123...  # the target channel ID
    python scripts/slack_test.py

The token is read exclusively from the environment and is never printed,
logged, or included in any output.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

MESSAGE = "THINC Agent test successful from thinc-v4."
SLACK_API_URL = "https://slack.com/api/chat.postMessage"


def main() -> None:
    token = os.environ.get("SLACK_BOT_TOKEN", "").strip()
    channel = os.environ.get("SLACK_CHANNEL_ID", "").strip()

    if not token:
        sys.exit("Error: SLACK_BOT_TOKEN environment variable is not set.")
    if not channel:
        sys.exit("Error: SLACK_CHANNEL_ID environment variable is not set.")

    payload = json.dumps({"channel": channel, "text": MESSAGE}).encode()
    req = urllib.request.Request(
        SLACK_API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Bearer " + token,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:  # noqa: S310
            body = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode(errors="replace")
        sys.exit(f"HTTP {exc.code} from Slack API: {raw[:200]}")
    except urllib.error.URLError as exc:
        sys.exit(f"Network error contacting Slack API: {exc.reason}")

    if body.get("ok"):
        print("✓ Message delivered to Slack channel.")
    else:
        error = body.get("error", "unknown_error")
        sys.exit(f"Slack API error: {error}")


if __name__ == "__main__":
    main()
