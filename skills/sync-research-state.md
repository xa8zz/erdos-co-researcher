---
name: sync-research-state
description: Re-read the current research state document and recent round artifacts, then produce a targeted update diff — not a rewrite. Use when the user says "update our docs", "sync current state", "update the state doc", "we're a bit behind".
---

# Sync research state

## When to use

User asks for the state doc to be updated after new rounds have landed. Typical triggers: "update our docs", "sync current state", "we're a bit behind", "update the state doc with the new findings".

## Purpose

Keep the canonical state doc current without over-editorializing or losing historical ruled-out entries. Targeted diff, not rewrite.

## Instructions

1. Read the current state doc (usually `current_state.md` in the problem folder).
2. List recent artifacts by mtime — `researcher-*.md`, `verify-postresp-*.md`, `followup-*.md` — filtering to anything newer than the last state-doc modification.
3. For each new finding, classify:
   - **Established** — rigorously proven; either formally verified OR ≥ 2 verifier agreement with no substantive flag.
   - **Numerical evidence** — data, not proof.
   - **Ruled out** — refuted with a specific failure mechanism. Name the mechanism.
   - **Open / under audit** — landed but not yet verified.
4. Produce Edit-tool calls (one per section touched), not a Write of the whole doc.
5. For Established items: keep a short proof sketch inline — structural, not exhaustive.
6. For Ruled Out: name the approach + specific failure mechanism + round reference, not just "didn't work."
7. Preserve historical Ruled Out entries — they're the catalog of failure mechanisms, load-bearing for future rounds.

## Output

A series of Edit tool calls updating the state doc section by section.

## Synthesis rubric (after a verifier round)

When multiple verifiers have returned on a claim, decide where it lands:

1. **Unanimous "sound"** → promote to `Established`.
2. **Unanimous "broken"** → move to `Ruled Out` with the specific failure mechanism as the one-liner.
3. **Split (1 flags, 2 sound)** → re-read the flagger's argument carefully. If substantive, treat as broken pending re-derivation. If stylistic or confused, treat as sound.
4. **A verifier raises a new angle** → the angle becomes a specific fact in the next round's prompt: `Established` if validated, `Ruled Out` (with mechanism) if tried and refuted, `Numerical Evidence` if probed. Never a hand-waved suggestion.
5. **Never promote on one verifier alone.** Agreement across ≥ 2 is the minimum bar, and a formal-verifier pass (Aristotle, Lean) counts as one.

Save all verifier replies verbatim. Only synthesize when composing the next researcher prompt.

## Gotchas

- **Only promote to Established** with (a) ≥ 2 verifier agreement AND (b) formal proof OR honest best-effort formalization (e.g., Aristotle with sorries only in standard library imports).
- **Don't conflate proofs with numerical evidence.** Separate sections, different standards.
- **Don't delete Ruled Out items** even if they feel stale. They're the program's structural asset — researchers sense patterns across failures, and that cross-failure signal is what the next round often needs. A dense catalog of "X failed at step Y because of Z" is more valuable than a clean list of positives.
- **Ruled Out entries must encode the specific failure mechanism**, not "X didn't work." Include the arithmetic/combinatorial signature — the specific prime range, shield set, lemma, or constant that killed it. Vague entries are useless for pattern-matching; specific entries are the whole point.
- **Don't over-editorialize.** Facts + data + mechanisms. The state doc is ground truth, not commentary.
- **Sync before compaction, always.** Stale state is a silent loss vector.
