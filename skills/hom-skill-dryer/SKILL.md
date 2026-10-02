---
name: hom-skill-dryer
description: "Tree-shakes a skill after writing or changing it: tightens the description, moves rare parts to references/, overwrites only if its evals still pass. Use to dry, slim or optimize a skill."
---

# hom-skill-dryer

Build-time tree-shaking for skills: run once after a skill is written or changed, never before each use (reading a whole skill to trim it costs more than it saves).

Rule zero: **drying never changes behavior.** Every rule in the old skill survives — in SKILL.md or in references/. If the evals can't prove that, nothing is overwritten.

Work only on the skill folder you were given. Never add secrets, personal data, or project, company or customer names when rewriting; if the skill already holds any, stop and report the kind and the line, never the value. Report in the language of the user's request.

## Steps

1. **Measure.** `python3 <dir>/scripts/measure.py <skill-dir> [<repo-root>]`, where `<dir>` is the folder of this SKILL.md. Within budget and no obvious waste → report the numbers, stop.
2. **No `evals/evals.json`** → stop: without tests drying can't be verified. Suggest writing 2–3 evals with skill-creator first.
3. **Snapshot.** `snap=$(mktemp -d) && cp -r <skill-dir> "$snap/before" && echo "$snap"`; use the printed path as `<snap>`.
4. **Inventory.** List every rule, step, constraint and trigger phrase of the old skill, one line each. This list is the contract for step 7.
5. **Sort each item:**
   - **core** — needed on every run → stays in SKILL.md;
   - **rare** — only some cases (edge cases, long examples, reference tables) → `references/<topic>.md`, with a one-line pointer in SKILL.md saying *when* to read it;
   - **mechanical** — deterministic steps the model repeats → suggest a script in the report; write it only if it is trivial and covered by evals.
   If `measure.py` shows `preloaded_by_no_read_agent`, that agent can't read files: everything stays in SKILL.md, no references.
6. **Rewrite:**
   - description ≤ 200 characters (Claude.ai's limit; other tools allow 1024); keep what the skill does and its trigger phrases — cutting triggers saves tokens but breaks auto-invocation;
   - body: imperative, one-line "why" instead of paragraphs, one example instead of several, no repeated rules, lists over prose;
   - keep names, paths, script calls, templates and output formats exactly.
7. **Check the contract.** Every inventory line maps to the new SKILL.md or a reference. Anything unmapped → put it back.
8. **Run the evals** on the snapshot and on the dried skill, each in a fresh subagent with only that skill (in Claude.ai: one by one yourself — not cold, the second run sees the first; say so in the report). Compare each output with `expected_output` and with the snapshot's output.
9. **Decide:**
   - all evals pass and outputs are equivalent → keep the dried skill;
   - anything worse → restore: `rm -rf <skill-dir> && cp -r <snap>/before <skill-dir>`, and report which eval failed and why.
10. **Report**, ≤ 5 lines: description words and body tokens before → after, what moved to references/, scripts suggested, eval result. `rm -rf <snap>`. Don't commit.
