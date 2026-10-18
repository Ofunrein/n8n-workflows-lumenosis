#!/usr/bin/env python3
"""Reject embedded Discord webhook credentials without printing their values."""

import pathlib
import re
import subprocess
import sys

WEBHOOK = re.compile(
    r"https?://(?:(?:canary|ptb)\.)?discord(?:app)?\.com/"
    r"api(?:/v\d+)?/webhooks/\d+/[A-Za-z0-9._-]{20,}",
    re.IGNORECASE,
)


def has_webhook(text):
    return WEBHOOK.search(text.replace(r"\/", "/")) is not None


def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    paths = subprocess.check_output(
        ["git", "ls-files", "-z", "--", "*.json"], cwd=root
    ).decode().split("\0")
    findings = []
    for name in filter(None, paths):
        path = root / name
        if path.is_file() and has_webhook(path.read_text(encoding="utf-8")):
            findings.append(name)
    if findings:
        print("Embedded Discord webhook credentials found in:", file=sys.stderr)
        for name in findings:
            print(name, file=sys.stderr)
        print("Use an n8n credential or an environment expression.", file=sys.stderr)
        return 1
    print("No embedded Discord webhook credentials in tracked JSON files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
