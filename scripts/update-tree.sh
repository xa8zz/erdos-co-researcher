#!/usr/bin/env bash
# Regenerates the repo file tree, splices it into CLAUDE.md between
# <!-- REPO_TREE_BEGIN --> and <!-- REPO_TREE_END --> markers, then copies
# CLAUDE.md wholesale to AGENTS.md to guarantee content parity.
#
# CLAUDE.md is the source of truth. AGENTS.md is a mirror for Codex-family
# agents. Edit CLAUDE.md; run this script; both files stay byte-identical.
#
# Invoked by the SessionStart hook in .claude/settings.json, and can be
# run manually as `./scripts/update-tree.sh` whenever you want a refresh
# mid-session.

set -euo pipefail

cd "$(dirname "$0")/.."

SOURCE="CLAUDE.md"
MIRROR="AGENTS.md"
BEGIN="<!-- REPO_TREE_BEGIN -->"
END="<!-- REPO_TREE_END -->"
TMP_BLOCK=$(mktemp)
trap 'rm -f "$TMP_BLOCK"' EXIT

# Generate tree of tracked files, excluding extracted Aristotle Lean builds
# (anywhere in the tree — problem folders typically contain aristotle/
# subdirs with tarball extractions that shouldn't clutter the tree view).
# Uses git ls-files so .gitignore is automatically respected.
{
  echo "$BEGIN"
  echo '```'
  git ls-files \
    | grep -v -E '/aristotle/.*_out/' \
    | sort \
    | awk -F/ '
      {
        for (i = 1; i < NF; i++) {
          path = ""
          for (k = 1; k <= i; k++) path = path $k "/"
          if (!seen[path]) {
            seen[path] = 1
            indent = ""
            for (j = 1; j < i; j++) indent = indent "  "
            print indent $i "/"
          }
        }
        indent = ""
        for (j = 1; j < NF; j++) indent = indent "  "
        print indent $NF
      }'
  echo '```'
  echo "$END"
} > "$TMP_BLOCK"

if grep -qF "$BEGIN" "$SOURCE" && grep -qF "$END" "$SOURCE"; then
  # Splice in-place. Python handles multi-line replacement robustly.
  python3 - "$SOURCE" "$BEGIN" "$END" "$TMP_BLOCK" <<'PY'
import sys, re, pathlib
target = pathlib.Path(sys.argv[1])
begin, end, block_path = sys.argv[2], sys.argv[3], sys.argv[4]
text = target.read_text()
new_block = pathlib.Path(block_path).read_text().rstrip()
pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.DOTALL)
text, n = pattern.subn(new_block, text, count=1)
assert n == 1, "expected exactly one marker pair"
target.write_text(text)
PY
else
  # First run — prepend the block (plus blank line) to CLAUDE.md.
  tmp_out=$(mktemp)
  cat "$TMP_BLOCK" > "$tmp_out"
  echo "" >> "$tmp_out"
  cat "$SOURCE" >> "$tmp_out"
  mv "$tmp_out" "$SOURCE"
fi

# Mirror CLAUDE.md → AGENTS.md verbatim for content parity.
cp "$SOURCE" "$MIRROR"
