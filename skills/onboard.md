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

### Step 7 — Next-steps summary

Give the user a compact pointer list:

1. **Read `CLAUDE.md`** — the orchestrator's full operating manual. Budget ~10 min; it has the research loop, the paste-save protocol, the stuck-research heuristic.
2. **First dispatch** — use `docs/writing-prompts.md` as the prompting reference. CLAUDE.md has the researcher prompt shape and the frontmatter template for round docs (in the paste-save protocol section).
3. **Saving responses** — when a research output lands, run `/add-round-doc` (the skill handles byte-faithful extraction + frontmatter write).
4. **Compile state as you go** — `scripts/compile_rounds.py --root <slug>/ --out <slug>/state_compiled.md`. Do this before every dispatch so prompts reflect the current state view, not your memory.

## Output

Interactive walkthrough. Concrete artifacts produced: scaffolded `<slug>/` directory, personalized README, one initial commit.

## Gotchas

- **One question at a time.** Batch questions get partially answered; you'll then forget which ones you still need.
- **Don't pre-scaffold before Step 2.** The problem slug comes from the user. Creating the directory before asking commits their future work to your guess.
- **Tool recommendations are menus, not prescriptions.** The user's setup is personal. Don't push a specific CLI if they haven't said they want it. Your job is to enumerate options; their job is to pick.
- **Don't touch `scripts/`, `templates/`, `docs/`.** These are infrastructure. Editing them means their copy diverges from upstream; if they later want to pull harness improvements, they'll have merge conflicts they didn't plan for.
- **Commit the scaffold before anything else.** A dirty working tree on a fresh clone is a confusing starting state, and the user should own their first commit cleanly.
- **Don't run `git config --global`.** Any git identity changes are scoped to this repo with `--local` (the default when run inside the repo). Global changes affect all of the user's projects.
