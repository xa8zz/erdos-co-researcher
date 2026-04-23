#!/usr/bin/env python3
"""Compile round docs (files with YAML front-matter) into a current state view.

Walks all markdown files under a root directory, parses front-matter (minimal
YAML subset sufficient for the round-doc schema at `docs/round-doc-schema.md`),
walks the `action` graph to derive status, and writes a compiled Markdown view.

Usage:
    scripts/compile_rounds.py --root erdos-872/ --out erdos-872/state_compiled.md
    scripts/compile_rounds.py --root erdos-872/ --out -          # stdout

The compiler is intentionally dependency-light: it uses a minimal YAML parser
for the flat + list + block-scalar subset the schema uses.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path
from collections import defaultdict
from datetime import date


# ---------- minimal YAML parser (flat keys, lists, block scalars >) ----------


def _strip_yaml_comment(line: str) -> str:
    # Remove trailing comments not inside quotes. Naive but works for our schema.
    out, in_str, quote = [], False, ""
    for c in line:
        if in_str:
            out.append(c)
            if c == quote:
                in_str = False
        else:
            if c in ("'", '"'):
                in_str = True
                quote = c
                out.append(c)
            elif c == "#":
                break
            else:
                out.append(c)
    return "".join(out).rstrip()


def parse_frontmatter(text: str) -> dict:
    """Parse the subset of YAML used by round-doc schema.

    Supported: top-level key: value, nested 1-level (action.kind/target),
    lists `[a, b]` inline, block lists with `-` items, block scalars with `>`
    (folded to single-line + spaces).
    """
    result: dict = {}
    lines = text.splitlines()
    i = 0

    def parse_inline_list(s: str) -> list:
        s = s.strip()
        if not (s.startswith("[") and s.endswith("]")):
            return [s]
        inner = s[1:-1].strip()
        if not inner:
            return []
        # Naive split on comma not inside nested brackets
        parts, depth, buf = [], 0, ""
        for c in inner:
            if c == "[":
                depth += 1
                buf += c
            elif c == "]":
                depth -= 1
                buf += c
            elif c == "," and depth == 0:
                parts.append(buf.strip())
                buf = ""
            else:
                buf += c
        if buf.strip():
            parts.append(buf.strip())
        return [_coerce(p) for p in parts]

    def _coerce(v: str):
        v = v.strip()
        if v.startswith("'") and v.endswith("'"):
            return v[1:-1]
        if v.startswith('"') and v.endswith('"'):
            return v[1:-1]
        if v.lower() in ("true", "false"):
            return v.lower() == "true"
        if v.lower() == "null":
            return None
        # Keep numbers as strings — schema treats them as tokens.
        return v

    while i < len(lines):
        raw = lines[i]
        line = _strip_yaml_comment(raw)
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        # Nested 1-level (indented 2 spaces)
        if line.startswith("  ") and ":" in line:
            # Handled by parent; skip
            i += 1
            continue
        if ":" in line:
            key, _, rest = line.partition(":")
            key = key.strip()
            rest = rest.strip()
            if not rest:
                # Could be a nested dict or a block list
                # Peek next line
                j = i + 1
                nested: dict = {}
                block_list: list = []
                while j < len(lines):
                    nl = _strip_yaml_comment(lines[j])
                    if not nl.strip():
                        j += 1
                        continue
                    if nl.startswith("  ") and ":" in nl and not nl.strip().startswith("- "):
                        nk, _, nv = nl.strip().partition(":")
                        nested[nk.strip()] = _coerce(nv.strip())
                        j += 1
                    elif nl.strip().startswith("- "):
                        item = nl.strip()[2:].strip()
                        # Inline list of lists: e.g. [claude-audit, agrees]
                        if item.startswith("[") and item.endswith("]"):
                            block_list.append(parse_inline_list(item))
                        else:
                            block_list.append(_coerce(item))
                        j += 1
                    else:
                        break
                if nested:
                    result[key] = nested
                elif block_list:
                    result[key] = block_list
                else:
                    result[key] = None
                i = j
                continue
            if rest.startswith(">"):
                # Block scalar, folded. Collect subsequent indented lines.
                i += 1
                collected = []
                while i < len(lines):
                    ln = lines[i]
                    if ln.startswith("  ") or not ln.strip():
                        collected.append(ln[2:] if ln.startswith("  ") else "")
                        i += 1
                    else:
                        break
                result[key] = " ".join(l.strip() for l in collected if l.strip())
                continue
            if rest.startswith("["):
                result[key] = parse_inline_list(rest)
                i += 1
                continue
            result[key] = _coerce(rest)
            i += 1
            continue
        i += 1

    return result


def extract_frontmatter(path: Path) -> dict | None:
    """Return parsed front-matter dict if the file starts with `---` fence; else None."""
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        return None
    if not text.startswith("---\n"):
        return None
    rest = text[4:]
    end = rest.find("\n---")
    if end < 0:
        return None
    fm_text = rest[:end]
    try:
        return parse_frontmatter(fm_text)
    except Exception as e:
        print(f"WARN: front-matter parse failed in {path}: {e}", file=sys.stderr)
        return None


# ---------- compile ----------


def collect_rounds(root: Path) -> list[dict]:
    rounds = []
    for path in sorted(root.rglob("*.md")):
        fm = extract_frontmatter(path)
        if not fm:
            continue
        if "id" not in fm:
            print(f"WARN: {path} has front-matter but no `id` field; skipping", file=sys.stderr)
            continue
        fm["_path"] = path
        rounds.append(fm)
    return rounds


def validate_rounds(rounds: list[dict]) -> int:
    """Emit warnings for missing required fields + conditional requirements.
    Rendering continues regardless; returns warning count for the caller.
    """
    by_id = {r["id"]: r for r in rounds if "id" in r}
    warnings = 0
    required = ["type", "date", "intent", "claim"]
    for r in rounds:
        rid = r.get("id", "?")
        for field in required:
            if not r.get(field):
                print(f"WARN: [{rid}] missing required field: {field}", file=sys.stderr)
                warnings += 1
        if "predecessors" not in r:
            print(f"WARN: [{rid}] missing `predecessors` (use [] if standalone)", file=sys.stderr)
            warnings += 1
        action = r.get("action")
        if not isinstance(action, dict):
            print(f"WARN: [{rid}] missing or malformed `action` block", file=sys.stderr)
            warnings += 1
            continue
        akind = action.get("kind")
        if not akind:
            print(f"WARN: [{rid}] action.kind missing", file=sys.stderr)
            warnings += 1
        elif akind in ("refutes", "supersedes"):
            if not action.get("target"):
                print(f"WARN: [{rid}] action.kind={akind} requires action.target", file=sys.stderr)
                warnings += 1
            if not r.get("failure_mechanism"):
                print(f"WARN: [{rid}] action.kind={akind} requires failure_mechanism", file=sys.stderr)
                warnings += 1
        elif akind in ("extends", "confirms"):
            if not action.get("target"):
                print(f"WARN: [{rid}] action.kind={akind} requires action.target", file=sys.stderr)
                warnings += 1
    return warnings


def derive_status(rounds: list[dict]) -> dict[str, list[dict]]:
    """Walk the action graph; return mapping from each round id to a list of
    later rounds that refute / supersede it (chronologically ordered)."""
    by_id = {r["id"]: r for r in rounds if "id" in r}
    overrides: dict[str, list[dict]] = defaultdict(list)
    for r in sorted(rounds, key=lambda r: str(r.get("date", ""))):
        action = r.get("action") or {}
        if not isinstance(action, dict):
            continue
        kind = action.get("kind")
        tgt = action.get("target")
        if kind in ("refutes", "supersedes") and tgt and tgt in by_id:
            overrides[tgt].append(r)
    return overrides


def bucket(rounds: list[dict], overrides: dict[str, list[dict]]) -> dict[str, list[dict]]:
    by_id = {r["id"]: r for r in rounds if "id" in r}
    buckets: dict[str, list] = {
        "Established": [],
        "Ruled Out": [],
        "Open / Partial": [],
        "Retracted chains": [],
        "Pending-target refutations": [],
    }
    for r in sorted(rounds, key=lambda r: str(r.get("date", ""))):
        rid = r["id"]
        overriders = overrides.get(rid, [])
        t = r.get("type", "research")
        action = r.get("action") or {}
        if not isinstance(action, dict):
            action = {}
        akind = action.get("kind")
        atgt = action.get("target")

        # If this round refutes/supersedes a target that isn't in the corpus
        # yet, surface it in its own bucket so the verdict isn't silently lost
        # during incremental backfill.
        if akind in ("refutes", "supersedes") and atgt and atgt not in by_id:
            buckets["Pending-target refutations"].append(r)
            continue

        if overriders:
            # Walk chain — was the overrider itself overridden?
            chain_tail = overriders[-1]
            re_overridden = overrides.get(chain_tail["id"])
            if re_overridden:
                buckets["Retracted chains"].append({"round": r, "chain": overriders + [c for c in re_overridden]})
                continue
            # Regular refute/supersede
            if t == "refutation":
                # A refutation that was itself refuted -> add as Established if single-step
                buckets["Established"].append(r)
            else:
                buckets["Ruled Out"].append({"round": r, "refuted_by": overriders[-1]})
            continue
        if t == "refutation":
            # Refutation stands; its *target* appears as Ruled Out (handled via overrides above)
            continue
        if t in ("research", "synthesis", "verification", "diagnostic"):
            buckets["Established"].append(r)
        else:
            buckets["Open / Partial"].append(r)
    return buckets


def render(buckets: dict[str, list[dict]], rounds: list[dict]) -> str:
    today = date.today().isoformat()
    lines = [f"# Current state (compiled {today})", ""]

    # Established
    lines.append("## Established")
    lines.append("")
    if not buckets["Established"]:
        lines.append("_none yet_")
    else:
        for r in buckets["Established"]:
            lines.append(_format_established(r))
    lines.append("")

    # Ruled out
    lines.append("## Ruled Out")
    lines.append("")
    if not buckets["Ruled Out"]:
        lines.append("_none yet_")
    else:
        for item in buckets["Ruled Out"]:
            lines.append(_format_ruled_out(item["round"], item["refuted_by"]))
    lines.append("")

    # Retracted chains
    if buckets["Retracted chains"]:
        lines.append("## Active chains (verdict flips)")
        lines.append("")
        for item in buckets["Retracted chains"]:
            lines.append(_format_chain(item["round"], item["chain"]))
        lines.append("")

    # Pending-target refutations (targets not yet backfilled)
    if buckets["Pending-target refutations"]:
        lines.append("## Pending-target refutations")
        lines.append("")
        lines.append(
            "_These rounds refute or supersede a target that isn't yet in the "
            "corpus. Expected during incremental backfill; will resolve once "
            "the target is added._"
        )
        lines.append("")
        for r in buckets["Pending-target refutations"]:
            lines.append(_format_pending_refutation(r))
        lines.append("")

    # Indices
    lines.append("## Indices")
    lines.append("")
    lines.append("### By type")
    type_counts = defaultdict(int)
    for r in rounds:
        type_counts[r.get("type", "?")] += 1
    for t, n in sorted(type_counts.items()):
        lines.append(f"- {t}: {n}")
    lines.append("")

    lines.append("### By strategy dependence")
    sd_counts = defaultdict(int)
    for r in rounds:
        sd_counts[r.get("strategy_dependence", "—")] += 1
    for s, n in sorted(sd_counts.items()):
        lines.append(f"- {s}: {n}")
    lines.append("")

    return "\n".join(lines) + "\n"


def _format_established(r: dict) -> str:
    path = r["_path"]
    rid = r["id"]
    claim = r.get("claim", "")
    date_s = r.get("date", "")
    ver = r.get("verifiers_at_time", [])
    conf = r.get("confidence_at_time", "")
    prompt = r.get("prompt", "")
    vs = ", ".join(v[0] if isinstance(v, list) and v else str(v) for v in ver) if ver else ""
    parts = [f"- **[{rid}]({path})** ({date_s}): {claim}"]
    meta = []
    if vs:
        meta.append(f"verified by {vs}")
    if conf:
        meta.append(f"confidence {conf}")
    if prompt:
        meta.append(f"prompt: [{prompt}]({prompt})")
    if meta:
        parts.append("  — " + "; ".join(meta))
    return "\n".join(parts)


def _format_ruled_out(r: dict, refuter: dict) -> str:
    path = r["_path"]
    rid = r["id"]
    claim = r.get("claim", "")
    rp = refuter["_path"]
    rfid = refuter["id"]
    rdate = refuter.get("date", "")
    fm = refuter.get("failure_mechanism", "")
    prompt = r.get("prompt", "")
    ref_prompt = refuter.get("prompt", "")
    parts = [f"- **[{rid}]({path})** claimed: {claim}"]
    parts.append(f"  Refuted by **[{rfid}]({rp})** ({rdate}).")
    if fm:
        parts.append(f"  Failure mechanism: {fm}")
    prompt_bits = []
    if prompt:
        prompt_bits.append(f"original prompt: [{prompt}]({prompt})")
    if ref_prompt:
        prompt_bits.append(f"refutation prompt: [{ref_prompt}]({ref_prompt})")
    if prompt_bits:
        parts.append("  " + "; ".join(prompt_bits))
    return "\n".join(parts)


def _format_chain(r: dict, chain: list[dict]) -> str:
    rid = r["id"]
    ids = " → ".join([rid] + [c["id"] for c in chain])
    return f"- {ids}"


def _format_pending_refutation(r: dict) -> str:
    path = r["_path"]
    rid = r["id"]
    claim = r.get("claim", "")
    action = r.get("action") or {}
    if not isinstance(action, dict):
        action = {}
    tgt = action.get("target", "?")
    akind = action.get("kind", "refutes")
    fm = r.get("failure_mechanism", "")
    date_s = r.get("date", "")
    prompt = r.get("prompt", "")
    parts = [f"- **[{rid}]({path})** ({date_s}): {akind} `{tgt}` (target not yet in corpus)"]
    if claim:
        parts.append(f"  Claim: {claim}")
    if fm:
        parts.append(f"  Failure mechanism: {fm}")
    if prompt:
        parts.append(f"  Prompt: [{prompt}]({prompt})")
    return "\n".join(parts)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True, help="Directory to scan for round docs")
    p.add_argument("--out", default="-", help="Output path (use `-` for stdout)")
    args = p.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"ERROR: root not found: {root}", file=sys.stderr)
        return 2

    rounds = collect_rounds(root)
    print(f"[scan] {len(rounds)} round docs with front-matter", file=sys.stderr)

    warnings = validate_rounds(rounds)
    if warnings:
        print(f"[validate] {warnings} warning(s) — rendering continues", file=sys.stderr)

    overrides = derive_status(rounds)
    buckets = bucket(rounds, overrides)
    output = render(buckets, rounds)

    if args.out == "-":
        sys.stdout.write(output)
    else:
        outp = Path(args.out)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(output)
        print(f"[wrote] {outp} ({len(output)} bytes)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
