---
name: hom-learn-from-fix
description: "After a bug fix, finds the root cause and real impact and, if new, adds a one-line case to your own ladder for hom-output-formatting. Use when a fix is done: fix commit, fix/ branch, \"it's fixed\"."
---

# hom-learn-from-fix

Turns a fixed bug into a one-line lesson for the ladder of **hom-output-formatting**, stored only on the user's machine or in their project. Runs in the main session: it needs what the session knows. Report in the language of the user's request.

Writes only `.md` files in `~/.hom/ladder/` or `<project>/.hom/ladder/`. Never edits installed skill files, never runs git commands that change anything, never sends lessons anywhere.

Every step can end the run. Stop at the first "no" — most fixes teach nothing new, and stopping early is the cheapest outcome.

1. **Is it a fix?** Session fixed a bug, commit type `fix`, or branch `fix/…`/`bugfix/…`. Else stop.
2. **Root cause, one sentence**, traced to the diff. Look at `git diff --cached --stat` (or `git show --stat HEAD`) first, then only the files that hold the fix. Unknown cause or a workaround (delay, retry, silencing catch) → stop: a lesson from a guess teaches every check the wrong thing.
3. **Impact**: what actually happened (from the session), placed by the ladder's principle.
4. **Generalize and strip everything private.** A lesson may be shared with a team later: no secrets, personal data, project, company or customer names, paths, domain terms, identifiers, values, ticket numbers. Test: reveals nothing about the project; a developer elsewhere recognizes the pattern.
   Good: `- JSON.parse of a storage read without a null check → crashes on first run, before the key exists. Every new user hits it.`
5. **New?** `bash <dir>/../hom-output-formatting/scripts/load_ladder.sh` (`<dir>` = folder of this SKILL.md; run from the project). Covered at the same level → stop. Covered but the real impact was worse → add at the higher level, naming the case it beats. Not covered → add.
6. **Where.** `<project>` = `git rev-parse --show-toplevel`.
   - `<project>/.hom/ladder/` exists → team ladder; else `~/.hom/ladder/` exists → personal ladder.
   - Neither → ask once: **personal** (`~/.hom/ladder/`, only you, every project) or **team** (`<project>/.hom/ladder/`, shared when you commit it)? Create the chosen folder.
7. **Write** one line, `- <pattern> → <effect>. <why this level>`, to `<ladder>/<level>.md` (`killed`, `wounded`, `kicked`, `scolded`). New file → first line `# <emoji> <LEVEL>`, as in `<dir>/../hom-output-formatting/ladder/`. Max 30 cases per file; full → show the user the two closest cases and a merged line, write it only if they agree.
8. **Report**, ≤3 lines: the line added or why nothing was; the file. Team ladder → remind them to commit `.hom/ladder/` to share it.
