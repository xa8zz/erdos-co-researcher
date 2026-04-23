---
name: write-codex-task
description: Produce a Codex task file for computation, verification, or sub-proof work in the repo workspace. Use when the user says "write me a codex task", "draft a codex prompt", "codex can do this", "yeah wanna make a codex task".
---

# Write Codex task

## When to use

User wants to hand off computation / verification / sub-proof work to Codex, which runs inside the repo workspace with file-level context.

## Purpose

Produce a self-contained Markdown task file Codex can execute without further clarification.

## Instructions

1. Classify the task:
   - **Empirical probe** — run simulation, tabulate, summarize
   - **Verification** — check a claimed numerical bound / identity / construction
   - **Sub-proof** — close a specific identified gap
   - **Formalization** — Lean or Aristotle attempt on a stated theorem
2. Create a markdown file at an appropriate path. Common locations: `phase<N>/CODEX_TASK_<name>.md` or `erdos-872/codex_backlog.md` (if adding to a larger queue).
3. Structure:

```markdown
# Codex task: <one-line goal>

## Goal
<one-sentence task>

## Context
<1-2 paragraphs of what's known, what the task advances, why this matters>

## Inputs
- File: <path> — <what's in it>
- Parameters: <specific values / ranges>
- Constraints: <what the answer must satisfy>

## What to produce
- Script: <path> — <what it should do, language (Python default)>
- Output: <path> — <format: CSV / JSON / markdown table>
- Summary: <path> — <short markdown summary of findings>

## Expected output format
<example — first few rows of CSV, or JSON structure, or markdown table>

## Reporting
When complete, append a short summary at <path>. Include:
- Headline result (one line)
- Any anomalies / edge cases encountered
- Next-step recommendations if relevant
```

4. Be specific about file paths. Not "write a script" but "write `scripts/verify_bound.py` reading `phase3/shortener_constants.csv` and outputting `phase3/verify_results.md`".

## Output

A `CODEX_TASK_*.md` file ready for the user to point Codex at.

## Gotchas

- **Codex works in `.codex/worktrees/<hash>/`**. Files there don't appear in the main repo without explicit copying. Include a "copy back" step if needed.
- **Check `git branch --show-current`** at session start — stale Codex-created branches may still be around.
- **Machine-parseable output** — CSV for numerical data, structured Markdown for text. Avoid free-form prose as the primary output.
- **Specific input paths** — no "read the state doc" but "read `erdos-872/current_state.md`".
- **Expect Codex to branch and commit** — you may need to cherry-pick or merge back.
- **Time estimate** — include one if the task is heavy ("~2 hours wall time for `n = 10^6` probe").
