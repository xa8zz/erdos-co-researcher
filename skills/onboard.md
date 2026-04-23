---
name: onboard
description: Set up a fresh clone of this harness for the user's own research program. Interviews the user on their problem, walks them through tool discovery for their co-researcher, scaffolds a problem directory, and commits the initial state. Run once after cloning.
---

# Onboard

## When to use

User has just cloned this starter repo and wants to set up their first research program. Typical triggers: "onboard me", user running `/onboard` directly after cloning, "help me get started", "set up my first problem".

## Purpose

Take a fresh clone from empty template to first-dispatch-ready. Concrete outputs:

1. A scaffolded problem directory at `<slug>/` with the minimum a harness needs
2. A personalized README and (optionally) git identity
3. A tooling inventory — what the user has vs what's recommended for their workflow
4. A committed initial state

## Instructions

### Step 1 — Introspect the fresh clone

```bash
ls -la
git log --oneline -5
git remote -v
```

Confirm the user has a clean clone. Note any remote they've already set — if they've cloned for their own use, they may want to point `origin` at their own fork.

### Step 2 — Interview (one question at a time)

Do **not** batch questions. One at a time, wait for each answer. The point is to build a clear picture interactively, not to overwhelm.

1. **Your name / GitHub handle?** Used for the README authorship block and optionally `git config user.name` for this repo.
2. **What problem are you working on?** Get two things: a kebab-case slug (e.g. `collatz`, `rh-zeros`, `my-conjecture`) for the directory name, and a one-line neutral mathematical statement of the problem.
3. **Which reasoning models will you dispatch to?** Common: GPT Pro (with extended thinking), DeepThink, Gemini 2.5 Pro, Claude Opus, Codex. Note: this harness is designed for **multi-model parallel dispatch**, not single-model chaining. Encourage picking at least 2 research models so cross-family adversarial audits are possible.
4. **Formal verification?** If the problem has theorem/lemma claims, Aristotle (Harmonic, Lean 4) is a very strong filter before promoting to `Established`. Skip if the work is empirical/computational without proof obligations.

### Step 3 — Tool your co-researcher up

This harness is most effective when the orchestrator (the curator agent) can actually reach across research agents and pull their work back on its own — compose prompts, paste them into chat tabs, extract responses byte-faithfully, file them into round docs. Think of this step as **equipping your co-researcher** with the tools it needs to do its job.

Walk the user through the categories. After each, ask if they want to set something up now or if they're already covered — don't push a specific CLI if they haven't asked.

- **Browser automation** — the most common rough edge. You'll want to read and write research-model chat tabs without manually copy-pasting. Good starting points:
  - [Browser Use CLI](https://github.com/browser-use/browser-use) — versatile, good primitives
  - [Vercel Browser CLI](https://vercel.com/) — lightweight, good for simple read/write flows
  - [Claude-in-Chrome MCP](https://claude.ai/) — if you're running Chrome with Claude Code
  - Playwright + a custom MCP wrapper — full control, more setup
  - Roll your own — anything that exposes "read tab content" + "fill textbox" + "click button" primitives works

  The user is encouraged to explore. Their setup is personal.

- **Formal verification** (Aristotle) — if they said yes earlier:
  - `pip3 install --user --break-system-packages aristotlelib`
  - Request an API key from Harmonic (https://harmonic.fun)
  - Store in `.env` at repo root; `.gitignore` already excludes it

- **MCP servers** — this starter does not ship MCPs. The user adds their own to `.mcp.json`. Common additions:
  - Linear / Notion / Google Docs MCPs for writeups
  - Domain-specific MCPs (browser automation, data sources, custom tooling)

### Step 4 — Scaffold the problem directory

Create `<slug>/` with the minimum a harness needs:

```
<slug>/
  current_state.md
  prompts/
```

`current_state.md` starts as:

```markdown
# <Problem name>

<One-line neutral math statement.>

## What's Established

_none yet_

## What's Been Ruled Out

_none yet_

## Numerical / Computational Evidence

_none yet_

## The Open Question

<What you're trying to push.>
```

Commit this scaffold immediately, even though it's empty — the first commit on the user's work should be scoped to their problem setup, cleanly separated from any later research dispatches.

### Step 5 — Personalize

- Update README.md author block with the user's name/handle (replace the generic mentions with their identity)
- Optionally `git config user.name "<Name>"` and `git config user.email "<email>"` — ask first before running

### Step 6 — Commit the scaffold

Named-file `git add` of `<slug>/` + the README edit. Never `-A`. Commit message:

```
Initial setup: <slug>
```

### Step 7 — Quick tour: how the research loop works

Don't just point at `CLAUDE.md` — walk the user through the shape of a round so they know what they're signing up for. Keep it tight.

One round = one full cycle:

1. **Refresh state** — `scripts/compile_rounds.py --root <slug>/ --out <slug>/state_compiled.md` regenerates the view from all committed round docs. Do this before every dispatch — the prompt should come from the compiled state, not session memory.
2. **Pre-send verification** — paste the drafted researcher prompt into ≥ 2 verifier tabs before dispatching. Catches anchoring and missing context.
3. **Dispatch** — send to a fresh thread on the primary research model (Pro / DeepThink / Codex / etc.).
4. **Save the return** via `add-round-doc` — byte-faithful extraction from session jsonl + YAML frontmatter in one call.
5. **Informal audits** — paste exact prompt + exact response into ≥ 2 verifier tabs in parallel via `write-audit-prompt`. Never bias one with another's output.
6. **Formal verification** (optional) — send theorem/lemma claims to Aristotle for Lean 4 formalization.
7. **Synthesize** — promote / demote by composing new round docs with `action: refutes | supersedes | extends | confirms`. Never edit past round docs — status is derived from the action graph, not stored.

Commit per round. Git is the durability layer — saved-but-uncommitted is as lost as non-existent.

### Step 8 — The skills you'll reach for most

Skills are invoked by conversational trigger phrases (saying "write me a follow-up" fires `write-followup-prompt`; `/<name>` also works). Walk the user through the core set:

| Skill | When it fires |
|---|---|
| `add-round-doc` | Every time the user pastes a researcher or verifier response. Most-used skill. |
| `write-audit-prompt` | Once per round — produces the adversarial prompt for verifier tabs. |
| `write-followup-prompt` | When a specific gap in a running thread needs pressure. |
| `write-codex-task` | Handing off computation / verification / sub-proofs to an in-repo agent. |
| `commit-round` | End of every round. Per-round scope, named-file `git add`. |
| `sync-research-state` | When new rounds have landed and the state doc needs a targeted refresh. |
| `progress-zoom-out` | When research stalls or the user asks "where are we." Honest, not reframed. |
| `pre-compact-capture` | Before compacting the session. Catches unpersisted pastes and uncommitted work. |
| `paper-review/` bundle | When working on a manuscript — peer review, rebuttals, critique framework, literature reviews (8 skills). |

### Step 9 — Three principles to internalize

1. **Frontmatter is immutable.** Once a round doc is written, it's never edited. Status is derived by `compile_rounds.py` from the `action` graph — never stored as a field. Overturn via a new round doc with `action.kind: refutes | supersedes` pointing at its `id`.

2. **Commit per round.** Git is the durability layer. Saved-but-uncommitted files are just as lost as non-existent ones.

3. **Prompt from compiled state, not memory.** When a research dispatch feels stuck, the problem is almost always upstream of the agent — stale state, anchored framing, session jargon leakage, missing failure mechanism, or frontier-research framing. Recompile, re-read, re-draft. Details in `docs/writing-prompts.md`.

### Step 10 — Ready?

That's the tour. Full depth in `CLAUDE.md` — budget ~10 min when the user has quiet time. Offer: "Want to compose your first researcher prompt together now, or is there more setup to handle first?"

### Step 11 — Make it yours

Important closing note — tell the user this directly:

The skills and setup here were built during one specific research program by someone (arguably a noob) figuring it out as they went. They represent what worked at one point in time with the models available then — not the final answer.

Models will keep getting better. Your workflow will evolve. Some of these skills will stop fitting you. That's expected. **Tweak them, delete ones you don't use, write new ones, rewrite CLAUDE.md in your own voice.** The harness gets better when you shape it to your own style.

Only the core principles are load-bearing — immutable records, per-round commits, prompt-from-compiled-state, curator-not-solver. Everything else is adjustable.

Encourage the user out loud: "Don't treat this as a fixed setup. You should end up with something that feels like yours within a few weeks."

## Output

Interactive walkthrough. Concrete artifacts produced: scaffolded `<slug>/` directory, personalized README, one initial commit.

## Gotchas

- **One question at a time.** Batch questions get partially answered; you'll then forget which ones you still need.
- **Don't pre-scaffold before Step 2.** The problem slug comes from the user. Creating the directory before asking commits their future work to your guess.
- **Tool recommendations are menus, not prescriptions.** The user's setup is personal. Don't push a specific CLI if they haven't said they want it. Your job is to enumerate options; their job is to pick.
- **Don't touch `scripts/`, `templates/`, `docs/`.** These are infrastructure. Editing them means their copy diverges from upstream; if they later want to pull harness improvements, they'll have merge conflicts they didn't plan for.
- **Commit the scaffold before anything else.** A dirty working tree on a fresh clone is a confusing starting state, and the user should own their first commit cleanly.
- **Don't run `git config --global`.** Any git identity changes are scoped to this repo with `--local` (the default when run inside the repo). Global changes affect all of the user's projects.
