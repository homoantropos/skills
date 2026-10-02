#!/usr/bin/env bash
# Print the ladder cases for hom-output-formatting: the skill's base cases, then the
# user's personal cases (~/.hom/ladder/), then the project's team cases (<project>/.hom/ladder/).
# Usage: load_ladder.sh   (run from the user's project directory)
set -euo pipefail

base="$(cd "$(dirname "${BASH_SOURCE[0]}")/../ladder" && pwd)"
personal="$HOME/.hom/ladder"
project="$(git rev-parse --show-toplevel 2>/dev/null || pwd)/.hom/ladder"

echo "--- LADDER CASES (base, then personal, then project; for the same pattern the higher level wins) ---"
for level in killed wounded kicked scolded; do
  echo
  head -n 1 "$base/$level.md"
  for src in base personal project; do
    file="${!src}/$level.md"
    [ "$src" = project ] && [ "$project" = "$personal" ] && continue  # project dir is $HOME
    [ -f "$file" ] && grep '^- ' "$file" | sed "s/^- /- [$src] /" || true
  done
done
echo "--- END LADDER CASES ---"
