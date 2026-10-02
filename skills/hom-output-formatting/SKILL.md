---
name: hom-output-formatting
description: "Formats and double-checks code review or check results as a triage for a tired human: killed, wounded, kicked, scolded, praised. Marks its own findings. Input is text, never code."
---

# hom-output-formatting

Input: a **text** about code (review, check results, PR comments). Two jobs: **format** it on the ladder, and **check the text** with fresh eyes. Never review code itself: no files, no codebase. Bare code with no findings → say a review or check result is needed, stop.

Write by the rules of **hom-human-readable** (reader, writing, accuracy). Write in the language the hand-off asks for (`Reply in:`), else the user's request, else the source; translate headings, keep emoji, IDs, code and paths. Runs cold: use only the hand-off — source (required), who produced it, task, scope; anything missing goes to `Not given`, never guess.

## Ladder

Severity = how certain the harm is + whether an explicit agreement is broken. Guaranteed > possible; documented rule > unwritten. Place anything unlisted by this principle. Goal: the reader **will** fix 🔴🟠, **likely** fix 🟡, **notice** 🔵.

- **🔴 KILLED** — must not ship: wrong results, crashes, freezes, security holes, data loss. Cases: [`ladder/killed.md`](ladder/killed.md).
- **🟠 WOUNDED** — fix before commit: harm likely or a documented rule broken. Cases: [`ladder/wounded.md`](ladder/wounded.md).
- **🟡 KICKED IN THE PANTS** — should fix: harm possible, or out-of-task changes. Cases: [`ladder/kicked.md`](ladder/kicked.md).
- **🔵 SCOLDED** — worth noticing: no harm, but waste or sloppiness. Cases: [`ladder/scolded.md`](ladder/scolded.md).
- **🟢 PRAISED** — always: what avoided the issues above, in ladder order (praise teaches); then the developer's strengths. Only what the text supports, else `Nothing in the source to praise specifically.`

**Cases.** Use the `LADDER CASES` block of the hand-off. No block and you can run commands → run `bash <dir>/scripts/load_ladder.sh` from the user's project (`<dir>` = folder of this SKILL.md). It merges the base cases with the user's own, learned by hom-learn-from-fix: personal `~/.hom/ladder/`, team `<project>/.hom/ladder/`. For the same pattern the higher level wins. Neither → place by the principle and make the report's first line `⚠️ Ladder cases not given: severity by principle only. Pass the output of load_ladder.sh.`

## Secrets and private data

Never repeat a secret or personal identifier from the source (password, API key, token, private key, connection string, ID or card number): write `[REDACTED: <kind>]`. A secret in code or a diff is a 🔴 finding; its fix is "revoke and rotate, then move to a secret store" — removing it from the code is not enough, history keeps it. `[REDACTED: …]` already in the source is a *possible* secret (a script can't be sure): still 🔴 with ❓ — a deliberate exception to guaranteed > possible, since a leaked secret can't be taken back — `❓ Fix: decide yourself — check it is a real secret; if so, revoke and rotate`.

## Your findings

- Mark with 🔍; unmarked = from the source.
- Only what the text shows (quoted code, numbers, claims) and that plainly breaks. No style opinions on fragments.
- Raise severity openly (`🔍 raised from WND`); lower only with a reason in SOURCE CHECK.
- Keep the source's locations, values and claims. Make vague items concrete only as far as the text allows.

## Fixes: three states

The reader copies fix lines as they are; a confident wrong fix is worse than none.
- **Certain (90–100%)**: plain, minimal — no refactors, renames or features.
- **Source fix doubtful**: keep it, add `🔍 Doubt: <why it fails>. Possibly: <better fix>`.
- **Problem certain, fix uncertain**: mark ❓, add `❓ Fix: decide yourself — <what is known, what it depends on>`.

## Template

```
## <✅ READY | ⚠️ READY WITH FIXES | ❌ NOT READY> — <one-line reason>
🔴 N · 🟠 N · 🟡 N · 🔵 N · 🔍 added N · doubtful fixes N · ❓ N
Source: <who> · Scope: <what it checked> · Not given: <missing, or —>
Unmarked = source; 🔍 = checker.

---
### 🔴 KILLED — N
**KIL-1 · [🔍 ·] [❓ ·] `file:line` — <what to change>**
Why: <input → line → result>
[🔍 Doubt: … Possibly: …] [❓ Fix: decide yourself — …]
Done when: <observable result>
Test: <input → expected>

### 🟠 WOUNDED — N        (same shape as KILLED)
### 🟡 KICKED IN THE PANTS — N
**KCK-1 · … — <what to change>**
Why: …
### 🔵 SCOLDED — N        (same shape as KICKED)
### 🟢 PRAISED
- …
### 🔍 SOURCE CHECK — N
**SRC-1 · <gap, contradiction, wrong severity, vague claim, doubtful fixes count>**
Why: …
---
## <VERDICT> — <what to fix first, by ID>
```

Rules: any 🔴 → NOT READY; any 🟠 → at most READY WITH FIXES. Empty blocks show `— 0`. One finding = one fix. No location in the source → name what it gives (function, module), never invent a line. IDs on every finding so the reader can say "KIL-1 done".

## Self-check (silent, fix before returning)

1. Every finding traces to the text. 2. Each 🔴 and 🔍 has a causal "Why"; can't write one → lower or mark ❓. 3. Every fix runs in the shown context; below ~90% → Possibly or ❓. 4. Counts, IDs and both verdicts agree. 5. No secret or personal identifier in the output.
