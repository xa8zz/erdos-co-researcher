#!/usr/bin/env python3
"""Extract user-pasted content from the current Claude Code session transcript
and save it as a round doc with YAML front-matter.

The front-matter is treated as opaque — this script doesn't parse it, just
wraps it with `---` delimiters and combines with the extracted body. The
compile script (compile_rounds.py) is what parses.

# Single file
Pass front-matter as YAML via stdin:

    scripts/add_round_doc.py \\
      --marker "Here is the full proof" \\
      --target erdos-872/researcher-56-pro-tau-sf-refuted.md <<'YAML'
    id: R56-tau-sf-refuted
    type: refutation
    date: 2026-04-19
    intent: >
      Determine whether tau_SF Shortener can reach O(r_1(n)).
    predecessors: [R52-sep-first, R54-sigma-star-audit]
    action:
      kind: refutes
      target: R52-sep-first
    claim: tau_SF fails; Prolonger forces L >= cn.
    failure_mechanism: >
      Upper-half dyadic shielding: Prolonger plays an even element of U,
      then preempts separators with 2^a * s_Q at cost n^(1/8+o(1)).
    confidence_at_time: high
    YAML

# Multi-block paste (user labeled blocks with ^#1, #2, ...)
Run once per block using --split-on + --split-index:

    scripts/add_round_doc.py --marker "Here are three responses" \\
      --split-on '^#\\d+\\s*$' --split-index 0 \\
      --target erdos-872/researcher-56-pro-a.md < fm-a.yaml

    scripts/add_round_doc.py --marker "Here are three responses" \\
      --split-on '^#\\d+\\s*$' --split-index 1 \\
      --target erdos-872/researcher-56-pro-b.md < fm-b.yaml

# No front-matter (raw save — same as the old save-pasted-response pattern)
    scripts/add_round_doc.py \\
      --marker "..." --target path.md --no-frontmatter

# Dry-run to preview
    scripts/add_round_doc.py --marker "..." --target /tmp/x.md \\
      --dry-run < fm.yaml

# Defaults
- Project dir defaults to ~/.claude/projects/-Users-omisverycool-erdos-harness/
  Override with --project-dir for other repos.
- Uses the *most recent* matching user message (branched sessions create new
  jsonl files; this script follows the freshest).
- Refuses to overwrite existing target files unless --force.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

PROJECT_DIR_DEFAULT = Path.home() / ".claude/projects/-Users-omisverycool-erdos-harness"


def content_text(entry: dict) -> str | None:
    """Extract plain text from a user message entry; return None for tool results."""
    msg = entry.get("message", {})
    content = msg.get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        for b in content:
            if isinstance(b, dict) and b.get("type") == "tool_result":
                return None
        return "\n".join(
            b.get("text", "")
            for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        )
    return None


def find_latest_match(project_dir: Path, marker: str) -> tuple[str, str, Path] | None:
    """Scan all session jsonls (newest first) for a user message containing marker.
    Returns (timestamp, content, session_path) for the most recent match."""
    if not project_dir.exists():
        raise FileNotFoundError(f"project dir not found: {project_dir}")
    sessions = sorted(project_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    for sp in sessions:
        # Iterate newest entries first within each session by reading all, then reversing
        entries: list[tuple[str, str]] = []
        for line in sp.read_text(errors="ignore").splitlines():
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("type") != "user":
                continue
            text = content_text(entry)
            if text and marker in text:
                entries.append((entry.get("timestamp", ""), text))
        if entries:
            # Return the latest match in this (latest) session
            ts, text = entries[-1]
            return ts, text, sp
    return None


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--marker", required=True, help="Unique phrase from the paste to locate it in the session")
    p.add_argument("--target", required=True, help="Path where the round doc should be written")
    p.add_argument("--project-dir", default=str(PROJECT_DIR_DEFAULT), help="Claude Code session jsonl directory")
    p.add_argument("--no-frontmatter", action="store_true", help="Skip front-matter; just save extracted body")
    p.add_argument("--split-on", default=None, metavar="REGEX", help="Split body on this regex (for multi-block pastes)")
    p.add_argument("--split-index", type=int, default=None, help="Which block (0-indexed) to save after --split-on")
    p.add_argument("--dry-run", action="store_true", help="Print to stdout instead of writing")
    p.add_argument("--force", action="store_true", help="Overwrite target if it exists")
    args = p.parse_args()

    # Front-matter from stdin unless --no-frontmatter
    frontmatter = ""
    if not args.no_frontmatter:
        frontmatter = sys.stdin.read().strip()
        if not frontmatter:
            print("ERROR: front-matter expected on stdin (use --no-frontmatter to skip)", file=sys.stderr)
            return 2

    project_dir = Path(args.project_dir)
    try:
        match = find_latest_match(project_dir, args.marker)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    if match is None:
        print(f"ERROR: marker not found in any session: {args.marker!r}", file=sys.stderr)
        return 1

    ts, body, session_path = match
    print(f"[match] session={session_path.name} ts={ts} body-len={len(body)}", file=sys.stderr)

    if args.split_on:
        blocks = re.split(args.split_on, body, flags=re.MULTILINE)
        blocks = [b.strip() for b in blocks if b.strip()]
        print(f"[split] found {len(blocks)} blocks:", file=sys.stderr)
        for i, b in enumerate(blocks):
            preview = b[:80].replace("\n", " ")
            print(f"  [{i}] {preview}...", file=sys.stderr)
        if args.split_index is None:
            print("ERROR: --split-on requires --split-index", file=sys.stderr)
            return 2
        if not (0 <= args.split_index < len(blocks)):
            print(f"ERROR: --split-index {args.split_index} out of range [0, {len(blocks)})", file=sys.stderr)
            return 1
        body = blocks[args.split_index]

    target = Path(args.target)
    if target.exists() and not args.force:
        print(f"ERROR: target exists: {target} (use --force)", file=sys.stderr)
        return 1

    # Compose final document
    if frontmatter:
        doc = f"---\n{frontmatter}\n---\n\n{body.rstrip()}\n"
    else:
        doc = body if body.endswith("\n") else body + "\n"

    if args.dry_run:
        sys.stdout.write(doc)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(doc)
        print(f"[wrote] {target} ({len(doc)} bytes)", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
