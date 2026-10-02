# AGENTS.md

Instructions for AI coding agents (Claude Code, Codex, Cursor, Gemini CLI, Copilot and others) working with or in this repository.

## What is here

Agent skills in the open SKILL.md format: a folder per skill, a `SKILL.md` with YAML frontmatter (`name`, `description`) and plain Markdown instructions. Any agent that can read Markdown can use them.

| Skill | Use it when | Needs |
|---|---|---|
| `skills/hom-human-readable` | You need to make any long text readable for a human — or you are writing for one in another skill | Nothing |
| `skills/hom-output-formatting` | You have the **text** of a code review or a code check and need to present it to a human, and double-check it | Text only — never the code itself |
| `skills/hom-pr-comments-prep` | You need to check the open review comments of a GitHub PR | `gh` CLI, logged in |
| `skills/hom-skill-dryer` | A skill was written or changed and should be checked against the token budget | Python 3; the skill's `evals/evals.json` |
| `skills/hom-learn-from-fix` | A bug fix is finished | `git` (read-only); writes only `~/.hom/ladder/` or `<project>/.hom/ladder/` |

`agents/hom-output-checker.md` is a Claude Code subagent that runs `hom-output-formatting` in a fresh context with no file tools. It is an **agent, not a skill**: copying `skills/` alone leaves it out — use `./install.sh`, or the plugin, where it is named `homoantropos:hom-output-checker`.

## Using a skill

1. Read the description in the frontmatter to decide if it applies.
2. Read the whole `SKILL.md` before acting, and follow it.
3. Run scripts from the skill's own folder (`scripts/`), not from memory.

## If your agent has no subagents

`hom-output-formatting` is meant to run **cold**: without the reasoning that produced the review it checks. Without subagents, get the same effect by starting a **new session** (or a separate model call) whose only input is the two `SKILL.md` files (`hom-output-formatting` and `hom-human-readable`) and the review text — no files, no tools, no earlier conversation.

## Working on this repository

- Skill names: lowercase, hyphens, `hom-` prefix. The folder name equals `name` in the frontmatter.
- **Token budget.** These are helper skills: they must stay cheap.
  - `description` ≤ 200 characters: Claude.ai rejects longer ones, and it is loaded into every session.
  - `SKILL.md` body ≤ ~1,500 tokens. After writing or changing a skill, run `hom-skill-dryer` on it.
  - Mechanical work goes into `scripts/`, so data never passes through the model's context.
  - Read only what the step needs (`--stat` before a full diff, one section with `sed` instead of a whole file).
  - Stop at the first step that rules the run out; the cheapest run is the one that ends early.
  - Rare material goes to `references/` — except in skills preloaded into `hom-output-checker`, which has no file tools; the ladder cases reach it in the hand-off (`load_ladder.sh`).
- Test cases live in `<skill>/evals/evals.json`.
- `hom-output-formatting/ladder/*.md` hold the **base** cases, changed only by maintainers in this repository. Learned cases never come back here: `hom-learn-from-fix` writes only to the user's `~/.hom/ladder/` or `<project>/.hom/ladder/`.
- Write skills, docs and commit messages in English. Skills **answer** in the language of the user's request, never English-only.

## Safety rules for every skill

- Never output, quote, store or commit secrets or personal identifiers: passwords, API keys, tokens, private keys, connection strings, ID, card or account numbers. Write `[REDACTED: <kind>]`; a leaked secret is a finding (revoke and rotate).
- Never write project, company or customer names, internal paths, hosts or identifiers into anything that leaves the conversation: files outside the user's project, commits, shared text, this repository.
- Work only in the user's current project. No skill reads, edits or commits to this repository or any other.
- Scripts use private temp dirs (`mktemp -d`) and are called by full path, never after `cd` into the skill folder. They never read, print or pass auth tokens.
