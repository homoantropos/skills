#!/usr/bin/env bash
# Install the skills and the hom-output-checker agent for Claude Code without the plugin system.
# Usage: ./install.sh              -> ~/.claude (all your projects)
#        ./install.sh <project>    -> <project>/.claude (that project only)
# Replaces earlier copies of the hom-* skills and agent there; touches nothing else.
# Never touches your learned cases: they live in ~/.hom/ladder/ or <project>/.hom/ladder/.
set -euo pipefail

src="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ $# -gt 0 ]; then
  [ -d "$1" ] || { echo "Not a directory: $1" >&2; exit 2; }
  dest="$(cd "$1" && pwd)/.claude"
else
  dest="$HOME/.claude"
fi

mkdir -p "$dest/skills" "$dest/agents"
for skill in "$src"/skills/hom-*/; do
  name="$(basename "$skill")"
  rm -rf "${dest:?}/skills/$name"
  cp -R "$skill" "$dest/skills/$name"
  rm -rf "$dest/skills/$name/evals"  # tests are for developing the skills, not for using them
done
cp "$src"/agents/hom-*.md "$dest/agents/"

echo "Installed into $dest:"
ls -d "$dest"/skills/hom-* "$dest"/agents/hom-*.md | sed "s|^$dest/|  |"
echo "Start a new Claude Code session to pick them up."
