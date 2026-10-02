#!/usr/bin/env python3
"""Measure a skill's token cost and check it against the budget.

Usage: measure.py <skill-dir> [<repo-root>]
Tokens are estimated: ~4 ASCII characters per token, ~2 for other scripts such as
Cyrillic, which tokenize worse. For official numbers in a Claude Code plugin use
`claude plugin details <plugin>`.
Prints JSON: sizes, budget flags, and whether a no-file-tool agent preloads
the skill (then references/ are unusable and everything must stay in SKILL.md).
"""
import json, re, sys
from pathlib import Path

DESC_CHARS, BODY_TOKENS = 200, 1500  # 200 = Claude.ai's description limit

def tok(text):
    ascii_chars = sum(1 for ch in text if ord(ch) < 128)
    return round(ascii_chars / 4 + (len(text) - ascii_chars) / 2)


def field(front, key):
    """Read a top-level YAML scalar, including block scalars (`key: >` or `key: |`)."""
    m = re.search(rf"^{key}:[ \t]*(.*)$", front, re.M)
    if not m:
        return ""
    value = m.group(1).strip()
    if value[:1] in (">", "|"):
        block = []
        for line in front[m.end():].split("\n")[1:]:
            if line.strip() and not line[:1].isspace():
                break
            block.append(line.strip())
        sep = "\n" if value[0] == "|" else " "
        return sep.join(block).strip()
    return value.strip("\"'")

skill = Path(sys.argv[1]).resolve()
root = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else skill.parent.parent
text = (skill / "SKILL.md").read_text()
m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
front, body = (m.group(1), m.group(2)) if m else ("", text)
desc = field(front, "description")
name = field(front, "name") or skill.name

refs = {str(p.relative_to(skill)): tok(p.read_text()) for p in sorted(skill.glob("references/**/*.md"))}

preloaded_by = []
for agent in sorted((root / "agents").glob("*.md")) if (root / "agents").is_dir() else []:
    a = agent.read_text()
    if re.search(rf"^\s*-\s*{re.escape(name)}\s*$", a, re.M) and re.search(r"disallowedTools:.*\bRead\b", a):
        preloaded_by.append(agent.stem)

out = {
    "skill": name,
    "description_chars": len(desc),
    "description_words": len(desc.split()),
    "description_tokens": tok(desc),
    "body_tokens": tok(body),
    "references_tokens": refs,
    "has_evals": (skill / "evals" / "evals.json").is_file(),
    "preloaded_by_no_read_agent": preloaded_by,
    "over_budget": {
        "description": len(desc) > DESC_CHARS,
        "body": tok(body) > BODY_TOKENS,
    },
}
print(json.dumps(out, indent=2))
