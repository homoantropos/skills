#!/usr/bin/env python3
"""Tests for build_package.py. Run: python3 test_build_package.py (no dependencies)."""
import importlib.util
import io
import json
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("build_package", HERE / "build_package.py")
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)

# text -> True if a secret must be redacted
REDACT = {
    'const password = "Tr0ub4dor-3-horse";': True,
    "+DB_PASSWORD=hunter2hunter2": True,
    '"apiKey": "abcdef123456789"': True,
    "export GITHUB_TOKEN=abc123def456": True,
    'const authToken = "q8Zr2pLx9"': True,
    'client_secret: "s3cr3tValue"': True,
    'SECRET_KEY = "dj4ng0s3cr3t"': True,
    "postgres://admin:s3cretpass@db.local:5432/app": True,
    "Authorization: Bearer abcdefghijklmnopqrstuvwxyz123456": True,
    "-----BEGIN RSA PRIVATE KEY-----\nMIIabc\n-----END RSA PRIVATE KEY-----": True,
    # false positives seen in review: the keyword is not at the end of the name
    'const tokenizer = "wordpiece"': False,
    'maxTokens: "2048000"': False,
    'const PASSWORD_MIN_LENGTH = "12345678"': False,
    "+PASSWORD_MIN_LENGTH=12345678": False,
    # references, numbers and placeholders
    "const token = getToken();": False,
    'password: "${PASSWORD}"': False,
    "apiKey: process.env.API_KEY": False,
    'const pin = "12345678"': False,
    'password = "changeme"': False,
    "API_KEY=your_api_key_here": False,
    "if (items.length = 0) return;": False,
    # shell variables holding paths, and i18n labels (third review)
    "PWD=/home/user/project": False,
    "+OLDPWD=/home/user/old": False,
    '"password": "Password"': False,
    '"password": "Пароль"': False,
    # base64 keys may start with "/"; numeric passwords and prefixed PWD are still secrets
    "AWS_SECRET_ACCESS_KEY=/aB3dE5fG7hI9jK1lM3nO5pQ7rS9tU1vW3xY5zA7": True,
    'secret: "/k8sTokenAbc/xyz123"': True,
    'password = "Пароль2024"': True,
    'password = "20240917"': True,
    "DB_PWD=k9x2m4q7": True,
}


def run(data):
    out, err = io.StringIO(), io.StringIO()
    sys.stdin = io.StringIO(json.dumps(data))
    with redirect_stdout(out), redirect_stderr(err):
        bp.main()
    return out.getvalue(), json.loads(err.getvalue())


def pr(threads, truncated=False):
    page = {"pageInfo": {"hasNextPage": truncated}}
    return {"data": {"repository": {"pullRequest": {
        "title": "t", "body": "", "url": "u",
        "reviewThreads": {"nodes": threads, **page},
        "reviews": {"nodes": []}, "comments": {"nodes": []}}}}}


def thread(outdated):
    return {"isResolved": False, "isOutdated": outdated, "path": "a.ts", "line": None, "originalLine": 7,
            "comments": {"nodes": [{"author": {"__typename": "User", "login": "x"}, "body": "b", "diffHunk": "@@"}]}}


failures = []
for text, want in REDACT.items():
    counter = [0]
    result = bp.redact(text, counter)
    if (counter[0] > 0) != want:
        failures.append(f"redact {text!r} -> {result!r}")

package, counts = run(pr([thread(True), thread(False)]))
if counts["threads"] != 2 or "outdated" in counts["dropped"]:
    failures.append(f"outdated threads must be kept: {counts}")
if package.count("OUTDATED") != 1 or "(1 outdated)" not in package:
    failures.append("outdated thread must be marked once")

package, counts = run(pr([thread(False)], truncated=True))
if counts["truncated"] != ["review threads"] or "Not given: more review threads" not in package:
    failures.append(f"truncation must be reported: {counts}")

print("\n".join(failures) or f"OK: {len(REDACT) + 2} checks")
sys.exit(1 if failures else 0)
