---
name: hom-pr-comments-prep
description: "Pulls a GitHub PR's open review comments via gh, drops resolved and bot threads, marks outdated ones, runs hom-output-checker on the rest. Use when given a PR link or number to check."
---

# hom-pr-comments-prep

Collects and cleans PR comments for **hom-output-checker**. Never judges, rewords or summarizes them: the checker must see them as written. All heavy lifting is in scripts, so the comments never pass through your context twice.

`<dir>` = the folder of this SKILL.md. Stay in the user's project directory and call scripts by full path; never `cd` into `<dir>` — a bare PR number takes the repo from the current directory.

1. Take a PR URL, or a number (repo from the current directory).
2. Fetch and build in **one** command (shell variables don't survive between calls), in a private temp dir:
   ```bash
   tmp=$(mktemp -d) && echo "$tmp" && bash <dir>/scripts/fetch_pr.sh <url-or-number> > "$tmp/pr.json" && python3 <dir>/scripts/build_package.py < "$tmp/pr.json" > "$tmp/package.md" && bash <dir>/../hom-output-formatting/scripts/load_ladder.sh >> "$tmp/package.md"
   ```
   Use the printed path as `<tmp>` below. No `gh` or not logged in → tell the user to install it or run `gh auth login`; never read, print or pass tokens.
3. The build appends the ladder cases (base, personal, team) for the checker, drops resolved, bot and deleted-account comments; keeps outdated threads, marked `OUTDATED`; keeps the rest verbatim with the last 10 lines of each diff hunk; replaces possible secrets with `[REDACTED: <kind>]`; prints counts to stderr. Don't read the JSON yourself; never look up or restore a redacted value.
4. 0 threads and 0 general comments → report what was dropped, `rm -rf <tmp>`, stop; don't start the checker.
5. Hand `<tmp>/package.md` unchanged to a **cold** checker, plus one first line: `Reply in: <language of the user's request>`. Nothing else of your own. Take the first that exists:
   - the **subagent** (not a skill) `hom-output-checker` — `homoantropos:hom-output-checker` when installed as a plugin;
   - a fresh general-purpose subagent told: "Use the skills hom-output-formatting and hom-human-readable on the text below. Don't read files, search or run commands: you check the text, not the code.";
   - no subagents → run **hom-output-formatting** yourself and start the report with `Not cold: checked in the main session.`
6. `rm -rf <tmp>`. Return the checker's report as is, with one line above: checked, dropped and redacted counts.

Limits: 100 threads, 50 comments per thread, 100 reviews, 100 general comments. The script reports anything cut off (`truncated` on stderr, `Not given` in the package); repeat it in your one line.
