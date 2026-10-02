---
name: hom-human-readable
description: "Turns any long text (law, contract, spec, docs, thread) into a brief for a tired human, in their language. Use to explain, summarize, simplify or \"make readable\" a text. Writing rules for skills."
---

# hom-human-readable

Write in the **language of the user's request**; with no request (hand-off from another skill), in the source's language. Translate template headings; keep code, paths, IDs and quotes as they are.

**Private data.** Never repeat secrets or personal identifiers: passwords, API keys, tokens, private keys, connection strings, ID, passport, card or account numbers. Write `[REDACTED: <kind>]` and say in `Watch out` that the source exposes one.

## The reader

Exhausted, poor eyesight, badly fitted glasses, reading tangled text 8–9 hours a day. Hasn't slept properly in years. Real explosions, war, constant pressure, burning deadlines — the more pressure, the harder to focus. Write as a senior rewriting a task for their past junior self: clear, short, unambiguous, no magic. When a rule doesn't fit, do what this reader needs.

## Writing

- Brief on top, details beneath; the first screen alone is enough to act.
- Bottom line at the top; repeat it at the bottom only if the brief is longer than one screen.
- Lead with what matters to the reader, not what the text is about.
- Numbers as digits: counts, amounts, dates, deadlines.
- One idea per line; short sentences; bold only the one thing the eye must catch.
- Plain words; explain a term once, then keep it.
- No "might be worth", no "it seems": if unclear, say so and what would settle it.
- No preamble, no pleasantries. Same structure every time.

## Accuracy

- A source reference on every claim: `[Art. 12(3)]`, `[p. 4]`, `[msg 7]`.
- Must / may / must not, numbers, dates, conditions and exceptions stay exact; keep each exception next to its rule.
- Exact wording matters → close translation in quotes + reference.
- Nothing invented; contradictions and gaps are findings, not things to resolve silently.

## Saving tokens

- **Read for the goal.** If the reader's goal is known ("I want remote work"), skim the structure first and read closely only the parts that serve it; list skipped parts in one line under `Details`.
- **Very long text** (more than ~30 pages): work section by section, keep only obligations, numbers, deadlines and gaps, then write the brief once.
- **Don't restate the source.** Details cover what the reader needs, not every section.

## Default template

Another skill's template replaces this one; the rules above still apply.

```
## Bottom line
<1–3 lines: what this means for the reader>
### What you must do — N
1. **<action>** — by **<deadline>** [ref]
### Key numbers
- **<number>** — <what> [ref]
### Watch out — N
- <prohibitions, penalties, traps, biting exceptions> [ref]
---
### Details
#### <topic in the reader's terms>
- <point> [ref]
### Unclear or missing — N
- <gap or contradiction, and what would settle it>
---
## Bottom line                  (only if longer than one screen)
<one line, same as the top>
```

Empty sections show `— 0`; drop `Key numbers` only if the text has none.

## Self-check (silent)

No secret or personal identifier repeated, nothing invented, nothing distorted (modals, numbers, conditions), no obligation, deadline or penalty lost, and the first screen works alone.
