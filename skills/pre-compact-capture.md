---
name: pre-compact-capture
description: Sweep the current Claude Code session for anything not yet persisted (saves, commits, memory updates, doc syncs) before the user compacts or ends the session. Use when the user says "im going to compact", "self-update", "anything to capture before I compact", "im gonna compact any docs to update".
---

# Pre-compact capture

## When to use

User signals they're about to compact the session or step away. Typical triggers: "im gonna compact", "do a self-update", "anything to update before compacting", "i'm going to compact — anything to save".

## Purpose

Claude Code compaction discards session context. Anything not persisted to disk is irretrievable after compaction. A disciplined pre-compact sweep prevents silent data loss.

## Instructions

Run through each category, confirm or fix:

1. **Unsaved pasted content**
   - Check recent user messages for multi-paragraph pastes.
   - For each, verify the target file contains it (use `grep` on a distinctive phrase).
   - If missing, save via `add-round-doc` skill.

2. **Uncommitted changes**
   - Run `git status`.
   - If there are staged or unstaged changes related to the current round, commit them via `commit-round` skill.
   - Never leave a round's work saved-but-uncommitted.

3. **Concurrent-agent state drift**
   - Another Claude / Codex session may have modified shared files (CLAUDE.md, current_state.md, canonical prompt, skills/). This happens when the user runs multiple sessions in the same repo in parallel.
   - Run `git log --oneline -10` to see if recent commits came from another session.
   - Look at the latest `git diff HEAD~5 CLAUDE.md` (or similar key files) — if your context doesn't match the current file content, another agent edited it.
   - If drift is detected, re-read the shared files before proposing edits; don't overwrite another agent's work.

4. **Memory updates**
   - Any feedback, user preferences, project context, or reference pointers from this session that aren't yet in memory — save them now.
   - Use the format: type (user / feedback / project / reference) + descriptive name.
   - Update `MEMORY.md` index, never just add the underlying file.

5. **Doc syncs**
   - `current_state.md`, process.md, any problem-folder state docs.
   - If they're stale relative to recent rounds, update via `sync-research-state` skill.

6. **CLAUDE.md updates**
   - Any new rules or patterns the user indicated should become durable instructions (e.g., "from now on always do X").
   - Propose Edit tool calls — don't rewrite.

7. **Open todos**
   - Clean up irrelevant ones.
   - Surface blockers that should survive the compaction.

## Output

Brief summary: what was captured, what was skipped and why. Then the session is safe to compact.

## Gotchas

- **Don't skip the commit step.** Saving files without committing is a silent data-loss risk.
- **Memory > TodoWrite for durable rules.** Todos die with the session; memory crosses sessions.
- **Don't rewrite CLAUDE.md.** Propose targeted Edits.
- **Verify `git status` is clean** after the sweep. If anything remains, surface it explicitly.
- **Ask before saving anything sensitive** (API keys, unpublished private research). User may want to defer to .env or a private branch.
- **The compaction is the user's call, not yours.** Report readiness; don't compact on your own.
