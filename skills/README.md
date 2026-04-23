# Skills — curator-agent toolkit

Named workflows the orchestrator agent uses while coordinating a research program. Each skill captures a recurring user-request pattern with a specific sequence of actions and a set of gotchas.

## Skills

| Skill | Trigger pattern | Purpose |
|---|---|---|
| `onboard` | First run after clone | Scaffold a problem directory, interview on tooling, initial commit |
| `write-followup-prompt` | "write me a follow-up", "give me the follow-up" | Produce a follow-up prompt to a researcher model |
| `write-audit-prompt` | "write me an audit prompt", "give me the audit" | Produce an informal-audit prompt for verifier tabs |
| `write-codex-task` | "write me a codex task", "draft a codex prompt" | Produce a workspace-aware task for an in-repo agent |
| `add-round-doc` | User pastes researcher output + asks to save | Byte-faithful extract + YAML frontmatter + write |
| `sync-research-state` | "update our docs", "sync current state" | Targeted diff update to the state doc |
| `commit-round` | "commit", "push", "commit first" | Per-round scoped commit with named-file adds |
| `progress-zoom-out` | "help me zoom out", "where are we" | Honest synthesis of program status |
| `pre-compact-capture` | "im going to compact", "self-update" | Sweep for unpersisted state before compaction |
| `paper-review/` | "review this paper", "write a rebuttal" | 8-skill bundle for manuscript review + literature work (imported from LobeHub) |

## Install

Skills live here under `skills/` at the repo root. Claude Code reads them automatically from this location. If you fork this repo, keep the directory name as `skills/`.

## Conventions

- Keep each skill under ~100 lines. Cheat-sheets, not manuals.
- The `description` field in YAML frontmatter is load-bearing — it drives when Claude invokes the skill. Be specific about triggers, not generic.
- Gotchas are mandatory. Each one should map to a real failure mode observed during usage, not hypothetical edge cases.

## Provenance

These skills were distilled from a long-horizon research program applied to Erdős Problem #872. Every trigger pattern, gotcha, and failure mode corresponds to an observed transcript event — not hypothetical usage. The `paper-review/` bundle was imported from the LobeHub/wentorai plugin ecosystem.

## Customizing for your own domain

These skills generalize to other long-horizon AI research loops (theorem discovery, mechanism design, empirical investigation, policy analysis). Expect to:

1. Swap `current_state.md` references for your domain's state file if you diverge from the convention.
2. Replace Codex with whatever workspace-aware tool you use (Claude Code itself, Cursor Composer, etc.).
3. Adjust the "Pro" / "DeepThink" labels to your actual primary research model.
4. Keep the commit discipline + pre-compact sweep exactly as written — they're the durability layer.
