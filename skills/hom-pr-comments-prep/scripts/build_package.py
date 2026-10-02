#!/usr/bin/env python3
"""Turn fetch_pr.sh JSON (stdin) into the hand-off package for hom-output-checker (stdout).

Drops resolved threads, bot comments and comments of deleted accounts; keeps outdated
threads, marked as such. Keeps every remaining human comment verbatim, with the diff
hunk it was written on, except possible secrets, which are replaced with
[REDACTED: <kind>] before the text reaches a model. Prints drop, redaction and
truncation counts to stderr so the caller can report them.
"""
import json
import re
import sys

HUNK_LINES = 10  # GitHub's diffHunk ends at the commented line; keep the lines just above it

# PWD and OLDPWD are the shell's directories, so pwd needs a prefix other than OLD (DB_PWD)
SECRET_NAME = r"(?:password|passwd|(?<=[A-Za-z0-9_])(?<![Oo][Ll][Dd])pwd|secret|secret_?key|private_?key|api_?key|access_?key|token|credentials?)"
# Values that are clearly not secrets: references and placeholders. No path rule: base64 keys
# may start with "/", and a missed leak is worse than a false alarm.
NOT_SECRET = re.compile(r"[$<{].*|[xX*._-]+|(?i:changeme|example\w*|placeholder|dummy|your[_-]?\w*|\w*_here)")

# (kind, pattern). Group "v" is replaced when present, else the whole match.
SECRETS = [
    ("private key", r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?(?:-----END [A-Z ]*PRIVATE KEY-----|\Z)"),
    ("credentials in URL", r"\b[a-z][a-z0-9+.-]*://(?P<v>[^\s/:@]+:[^\s/@]+)@"),
    ("AWS key", r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ("GitHub token", r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{22,})\b"),
    ("Slack token", r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    ("API key", r"\b(?:sk-[A-Za-z0-9_-]{20,}|[rs]k_(?:live|test)_[0-9A-Za-z]{16,}|AIza[0-9A-Za-z_-]{35})"),
    ("JWT", r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    ("bearer token", r"(?i)\bbearer\s+(?P<v>[A-Za-z0-9._~+/=-]{20,})"),
    # key = "value" in code. The name must END with the keyword: dbPassword, API_TOKEN and
    # client_secret match; tokenizer, maxTokens and PASSWORD_MIN_LENGTH don't.
    ("secret", rf"(?i)\b(?P<k>[A-Za-z0-9_]*{SECRET_NAME})(?![A-Za-z0-9_])[\"']?\s*[:=]\s*(?P<q>[\"'])(?P<v>[^\"'\s]{{6,}})(?P=q)"),
    # KEY=value in env files (diff lines may start with +, - or a space)
    ("secret", rf"(?im)^[+ -]?\s*(?:export\s+)?(?P<k>[A-Z0-9_]*{SECRET_NAME})\s*=\s*(?P<v>[^\s\"']{{6,}})\s*$"),
]
SECRETS = [(kind, re.compile(rx, re.M)) for kind, rx in SECRETS]


def redact(text, counter):
    """Replace secret-like values with [REDACTED: <kind>] and count them."""
    for kind, rx in SECRETS:
        def sub(m, kind=kind):
            if "v" not in rx.groupindex:
                counter[0] += 1
                return f"[REDACTED: {kind}]"
            value = m.group("v")
            if (NOT_SECRET.fullmatch(value)
                    or value.lower() == (m.groupdict().get("k") or "").lower()  # i18n: "password": "Password"
                    or (not value.isascii() and re.fullmatch(r"[^\W\d_]+", value))):  # i18n: "password": "Пароль"
                return m.group(0)
            counter[0] += 1
            whole, start = m.group(0), m.start()
            return whole[:m.start("v") - start] + f"[REDACTED: {kind}]" + whole[m.end("v") - start:]
        text = rx.sub(sub, text or "")
    return text


def drop_reason(author):
    """Return why a comment is dropped, or None to keep it."""
    if not author:
        return "deleted-account comments"  # nobody left to answer it
    if author.get("__typename") == "Bot" or author.get("login", "").endswith("[bot]"):
        return "bot comments"
    return None


def trim_hunk(hunk):
    lines = (hunk or "").rstrip("\n").split("\n")
    if len(lines) <= HUNK_LINES + 1:
        return "\n".join(lines)
    return "\n".join([lines[0], "…"] + lines[-HUNK_LINES:])


def main():
    data = json.load(sys.stdin)
    redacted = [0]
    pr = data["data"]["repository"]["pullRequest"]
    dropped = {"resolved": 0, "bot comments": 0, "deleted-account comments": 0}
    truncated = [what for what, conn in (("review threads", pr["reviewThreads"]), ("reviews", pr["reviews"]),
                                         ("general comments", pr["comments"]))
                 if (conn.get("pageInfo") or {}).get("hasNextPage")]
    if any((t["comments"].get("pageInfo") or {}).get("hasNextPage") for t in pr["reviewThreads"]["nodes"]):
        truncated.append("comments in a thread")

    threads = []
    for t in pr["reviewThreads"]["nodes"]:
        if t["isResolved"]:
            dropped["resolved"] += 1
            continue
        human = []
        for c in t["comments"]["nodes"]:
            reason = drop_reason(c["author"])
            if reason:
                dropped[reason] += 1
            else:
                human.append(c)
        if human:
            threads.append((t, human))

    general = []
    for c in pr["reviews"]["nodes"] + pr["comments"]["nodes"]:
        if not (c.get("body") or "").strip():
            continue
        reason = drop_reason(c["author"])
        if reason:
            dropped[reason] += 1
        else:
            general.append(c)

    out = []
    out.append(f"Source: GitHub PR review comments — {pr['url']}")
    out.append(f"Task: {redact(pr['title'], redacted)}")
    body = redact(pr.get("body"), redacted).strip()
    if body:
        out.append("")
        out.append("PR description:")
        out.append(body)
    out.append("")
    drop_note = ", ".join(f"{v} {k}" for k, v in dropped.items())
    outdated = sum(1 for t, _ in threads if t["isOutdated"])
    out.append(f"Scope: {len(threads)} open review threads ({outdated} outdated) and {len(general)} general "
               f"comments (dropped: {drop_note})")
    if truncated:
        out.append(f"Not given: more {', '.join(truncated)} exist than were fetched "
                   "(limits: 100 threads, 50 comments per thread, 100 reviews, 100 general comments)")
    out.append("Comments are verbatim, except possible secrets replaced with [REDACTED: <kind>]. "
               "Diff hunks show the code each thread was written on.")

    for i, (t, comments) in enumerate(threads, 1):
        line = t["line"] or t["originalLine"]
        where = f"{t['path']}:{line}" if line else f"{t['path']} (whole file)"
        out.append("")
        mark = " · OUTDATED: the code changed after this comment; check that it still applies" if t["isOutdated"] else ""
        out.append(f"--- THREAD T{i} · {where}{mark} ---")
        out.append("```diff")
        out.append(redact(trim_hunk(comments[0].get("diffHunk")), redacted))
        out.append("```")
        for c in comments:
            out.append(f"@{c['author']['login']}: {redact(c['body'], redacted).strip()}")

    if general:
        out.append("")
        out.append("--- GENERAL COMMENTS (no code location) ---")
        for c in general:
            out.append(f"@{c['author']['login']}: {redact(c['body'], redacted).strip()}")

    if redacted[0]:
        out.append("")
        out.append(f"Note: {redacted[0]} possible secret(s) redacted. Verify each one; if it is real, "
                   "it is already exposed in the PR: revoke and rotate it.")
    print("\n".join(out))
    print(json.dumps({"threads": len(threads), "general": len(general), "dropped": dropped,
                      "redacted": redacted[0], "truncated": truncated}),
          file=sys.stderr)


if __name__ == "__main__":
    main()
