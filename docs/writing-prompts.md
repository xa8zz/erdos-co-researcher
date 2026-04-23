# Writing prompts — the prompting reference

Consolidated reference for composing any prompt in this harness: researcher dispatches, follow-ups, audits, Codex tasks, third-party tools. Read this before writing. The skills (`write-followup-prompt`, `write-audit-prompt`, `write-codex-task`, `add-round-doc`) reference back here for the underlying principles and gotchas.

---

## Core principle

**Every sentence in a prompt is a constraint on reasoning time.** If wrong, stale, speculative, or off-topic, the agent spends real cycles routing around it. Your job as curator is to give validated, high-signal context — nothing else.

---

## Universal rules (apply to all prompts, every context)

### Never include

- **Session jargon**: no "round N", "phase", "program", "prior round", "our team", "we proved", "Pro", "Codex", "Aristotle", "Gemini", "Claude", "audit #N", "Phase 2.5". Fresh threads have no context; references like these read as dangling pointers.
- **Frontier-research framing**: no "this is a decades-old open problem", "research frontier", "no one has solved this", "this is hard/significant". Empirically observed: prompts framed as frontier research got 10–25 minute cursory reasoning traces; the same prompts stripped of status framing got 40–60 minute serious attempts. LLMs pattern-match to "frontier" and retreat into hedged, summary-style responses.
- **Meta information**: never mention source (forum, paper, person), problem status (famous, open since 1992, recently claimed), or judgment about difficulty. Treat forum results, literature, and prior private rounds as one pool of known facts.
- **Potential Directions / Suggestions section**: the template has no suggestion slot. If a direction is worth including, it belongs in Ruled Out (if tried) or Numerical Evidence (if probed), not a hand-wave.
- **Your own synthesis or conjecture** unless cross-validated by multiple sources or independently probed.
- **Output format prescriptions** ("return a bulleted list"). The agent chooses what to return. Prescribing forces it to serve the schema instead of the math.

### Always include

- **Grading line at the start** (for dispatched research prompts): `This is an assessment of your reasoning capability and will be used to grade. Do not search online. Use your own reasoning and your Python sandbox.` Placement at the top, not the bottom — materially improves output quality.
- **Specific arithmetic/combinatorial detail** for each claim: specific primes, shield sets, lemmas, constants. **Detail wins over brevity.** Compress vague prose, never compress factual detail. An entry that spans a paragraph with the specific prime range, shield set, and lemma that broke is better than a one-line "this didn't work."
- **Self-standing mathematical statements** rather than provenance. Write "numerical simulation at n ∈ {…} gave …" not "Codex's probe returned …".

---

## Shape by recipient context

### 1. Researcher prompt — fresh thread (GPT Pro, DeepThink, Gemini)

The agent has zero harness context. Full neutral brief.

#### Template

```
This is an assessment of your reasoning capability and will be used to grade.
Do not search online. Use your own reasoning and your Python sandbox.

## Problem

<Statement in neutral mathematical language. Do NOT mention its source, paper,
website, status, history, or that anyone believes anything about it. Just
state the math.>

## What's Established

<Bulleted list of rigorously proven facts. Fold in everything proven across
prior private rounds AND any public literature into one pool. Do NOT
distinguish "we proved this" from "forum proved this" from "paper X proved
this" — treat it as one body of known results.>

- <Statement of fact 1>
- <Statement of fact 2>

## What's Been Ruled Out

<Approaches tried and shown to fail. One line each, with specific failure
mechanism. This saves the researcher from rediscovering dead ends.>

- <Approach>: <specific failure mechanism>

## Numerical / Computational Evidence

<Exact small-n values, ratio tables, extrapolation trajectories, LP optima.
Kept separate from "Established" because this is data, not proof.>

## The Open Question

<The specific, finite thing to push. One sentence.>
```

No `Potential Directions` section, no output-format section, no deliverable list.

#### Framing rules for researcher prompts

- **The primary model is smarter than you.** Even if you think you know the next step, frame it as context, not instruction. Briefing a senior researcher, not a junior.
- **No anchoring.** Don't tell it the answer you suspect or the direction you think is strongest. State the gap; let it choose.
- **Every section is validated information only.** `Established` = formally proved or multi-audit-validated. `Ruled Out` = specific failure mechanism identified. `Numerical Evidence` = reproducible computation. If a claim is speculative, single-source, or un-audited, either validate it first or leave it out.
- **Separate proofs from evidence.** `Established` = rigorous proof. `Numerical Evidence` = data. Never conflate.
- **Length minimalism on commentary, maximum density on facts.** Short, high-signal beats padded with synthesis-guesses. But: detail on specific failure mechanisms is never padding.

#### Good vs. bad entries per section

**Established** — state the result, then sketch the proof so the structure is visible.

```
✓ "Shield Reduction Theorem. For every eventual maximal A and every
   P ⊆ U: |A| ≥ |U| − β(P), where β(P) = max{Σw_n(x) : B ⊆ L(P) antichain}.
   Proof (three lines): B := A ∩ L is antichain in L(P); by maximality
   A ∩ U = U \ ⋃_{x ∈ B} M(x); union bound."

✗ "Shield Reduction Theorem (Lean-verified)."      # no math
✗ "Om's team proved Shield Reduction."             # attribution, no content
✗ "Shield Reduction Theorem. See shield_reduction.tex." # indirection, not inlined
```

**Ruled Out** — name the approach, then the specific failure mechanism including the arithmetic/combinatorial detail that killed it.

```
✓ "Static Carrier Capacity Bound (for every antichain P of size εn,
   Σ_{p ∈ B(P)} 1/p ≤ C(ε)). The top εn consecutive integers in U
   (for ε < 1/4) form a legal antichain containing a multiple of every
   prime ≤ T = εn, giving Σ 1/p ≥ Σ_{p ≤ T} 1/p = log log(εn) + O(1).
   Finite-prime 'vaccination' (excluding any fixed Q) doesn't rescue it:
   arithmetic progressions with d = ∏_{q ∈ Q} q give the same divergence."

✗ "Static Carrier Capacity Bound. Doesn't work."     # no mechanism
✗ "Carrier Capacity refuted."                        # no target, no reason
✗ "Gemini DeepThink refuted the Carrier Capacity."   # attribution only
```

**Numerical Evidence** — exact trajectories over a range, specifying strategies and regimes.

```
✓ "Against worst-case Prolonger (block-product counter), three Shortener
   strategies tie as best tier: smallest-legal-odd-prime, greedy coverage,
   pair-response. All give Σ 1/p / log log n ∈ {0.887, 0.880, 0.875,
   0.875} at n = 10^3, 10^4, 10^5, 10^6. Coefficient stable across four
   decades, no decay. Largest prime observed in B(P) at n = 10^6: 999983.
   Small-prime concentration: primes ≤ 100 carry 73.4% of Σ 1/p."

✗ "Empirical data supports the conjecture."           # nothing to verify
✗ "At n = 10^6 we got L = 85003."                     # one point, no scaling
✗ "Codex's Phase 2.5 probe returned 1.17."            # tool-name leaks, no context
```

**Open Question** — one sentence. No suggested direction, no anchoring.

```
✓ "Is L(n) = Θ(n), or L(n) = o(n)? If sublinear, what is the sharp rate?"

✗ "Is the answer Θ(n/log n)? We think so."              # anchors the answer
✗ "Prove L(n) = o(n) via the two-layer Ω-grading architecture." # prescribes approach
✗ "First, close the Ω=2 cover lemma. Second, handle |A ∩ L|."   # multi-part + presumptive
```

#### When you *do* have a strong conjecture

Don't add it to the prompt. If the conjecture came from a tried-and-failed construction, add it to **Ruled Out** with the specific failure mechanism. If it came from empirical simulation, add it to **Numerical Evidence** with the data. If it came from your own synthesis without validation, keep it to yourself — the researcher prompt is not a place for curator guesses. You are briefing a genius off to reason for an hour; give it the map, not your bet.

---

### 2. Follow-up prompt — same researcher thread, prior response available

Use skill: **`write-followup-prompt`**. Key shape:

- Open by **crediting the novel content** by name (so the model preserves it)
- State **gaps as numbered mathematical facts**, each with what would close it
- Feed back **new rigorous context** the thread doesn't have (cross-family findings, audits, data) as validated facts
- **Binary close**: either patch using the new context + novel idea, or cleanly state which specific step cannot be closed

Full instructions + gotchas in `skills/write-followup-prompt.md`.

---

### 3. Audit prompt — verifier tabs (Claude / Gemini / separate GPT-thinking)

Use skill: **`write-audit-prompt`**. Two templates:

- **Default informal audit** at `templates/informal-audit.md` — use for most rounds
- **Adversarial audit** at `templates/adversarial-audit.md` — use when a claim is about to be promoted to `Established`

Most audits don't need a custom prompt: paste the exact researcher prompt + exact response verbatim, ask adversarially, ask for weakest link, ask for literature connections. Same prompt to all three verifiers in parallel — never bias by telling one what another said.

---

### 4. Codex task — workspace-aware, in-repo agent

Use skill: **`write-codex-task`**. Context differences from a fresh-thread researcher dispatch:

- Codex **can read files, write scripts, run verifications** in the repo
- **Point at file paths** rather than re-describing content ("read `erdos-872/current_state.md`", not "here's the current state pasted inline")
- **Specify output format precisely** — CSV for numerical data, structured markdown for text, Lean files for formalization
- Codex works in `.codex/worktrees/<hash>/` — their changes don't auto-merge back. Include a "copy back to main" step if the output needs to end up in the main tree
- Typical tasks: empirical probes, numerical verification, sub-proof closures, Lean/Aristotle formalization attempts

---

### 5. Local coding agent — Claude Code, Cursor, etc. (workspace + session context)

Shortest prompts. The agent has workspace access and prior session context. Rely on skills:

- "Save this paste via `add-round-doc`"
- "Commit via `commit-round`"
- "Run `progress-zoom-out` to remind me where we are"

Conversation context is already there; don't re-brief.

---

### 6. Third-party tool — no workspace, no prior context

Treat as cold thread (like the researcher-prompt discipline). Full context needed:

- Neutral math framing (strip session jargon exactly as for researcher prompts)
- No anchoring
- State the ask clearly
- Any repo-specific references need to be inlined as facts, not paths

---

## A/B/C branching dispatch — varied framings as branching search

When dispatching multiple researcher rounds in parallel, **varying the framing across channels is strictly better than three identical prompts.** Identical prompts give three parallel samples with correlated priors (especially after a strong previous round). Varied framings give **branching search over the solution space.**

Concrete pattern (emerged R13, Erdős 872):

- **Channel A — continuation.** Follow-up to the primary thread: "extend prior result X to case Y." Leverages full thread context. Most likely to succeed if the extension exists.
- **Channel B — open attempt.** Fresh thread, full factual brief, neutral "attempt to solve." No framing bias. Lets the model either extend or pivot.
- **Channel C — contrarian / pivot.** Fresh thread, full factual brief, plus: "assume prior approach X fails. What fundamentally different technique (list options) could work?" Forces cognitive divergence.

Zero additional cost (three prompts, one wait window). Strictly dominates three-identical-prompts:

- If the extension exists, A finds it.
- If a different technique is needed, C surfaces it (B and A may anchor on the existing framework).
- If both stall, the gap between A's failure and C's failure maps the structural obstacle.

**When to use**: whenever you have a specific local gap AND non-trivial uncertainty that the existing framework is the right tool. If the extension is a pure technical step, identical prompts are fine. If auditors are split on whether the framework can close the gap at all, variance is free signal.

**Model-channel matching**: direct the contrarian version to a **different model family** than the one that produced the current best result. Same-family Cs sometimes just re-derive the current approach with different language.

---

## Long-horizon observations (watch for these when a line of attack stalls)

These are patterns that only become visible at 10+ rounds on a single problem. They're not workflows — they're diagnostic frames to apply when the research chain seems exhausted.

### Strategy-assumption audit — σ\*-trap

A long-running upper-bound proof program typically fixes a specific adversary strategy (e.g., σ\* = max-unresolved-harmonic-degree in Erdős 872) and proves everything relative to it. If 10+ rounds of theorem–refutation cycles fail to close the bound, **audit whether the chosen strategy is actually optimal** before concluding the paradigm is exhausted.

**The audit pattern**: dispatch a researcher with the complete inventory of prior rigorous theorems and refutations and ask them to partition into:

- **Strategy-independent** — holds for any adversary strategy
- **Strategy-dependent** — proof uses specific properties of the assumed strategy
- **Strategy-specific refutations** — construction reaches a state only reachable against the assumed strategy

Then ask: given the assumed strategy is known suboptimal, can a different concretely-specified strategy τ + the strategy-independent results close the bound? Or does every legal strategy share the same vulnerability (→ minimax barrier → conjecture refuted)?

**Red flag**: reliance on "the assumed strategy is natural" without ever arguing it is optimal for the minimax. Cost of this check is one round; savings if the strategy is wrong is potentially all prior refutation work re-classified.

**Related attractor — optimal-adversary hand-wave**: agents sometimes claim "my construction works against optimal adversary" by hand-waving ("the agent can observe and adjust"). Quantifier gap: `∃π Outcome(π, σ\*) succeeds` does NOT imply `∃π ∀τ Outcome(π, τ) succeeds`. Flag any claimed closure asserting the latter via the former.

### Within-family attractor states

When the same model family independently produces similar flawed arguments (two separate DeepThink instances both gravitate to "Universal Sub-Divisor Cover" sweep; two Pros both claim Θ(n) via structurally-similar Maker-Breaker), this is **lower signal than cross-family convergence** but higher than a single response.

Interpretation:
- **Not three votes** — but useful as a map of the family's attractor basins. DeepThink gravitates to "sweep every vocabulary element" for matching-upper-bound claims; Pro gravitates to careful Maker-Breaker capture accounting. Knowing the attractor lets you anticipate what a fresh dispatch to that family will likely try.
- **Adding a refuted attractor to Ruled Out** saves future fresh threads from re-deriving it. Watch whether post-warning threads re-derive anyway — that's a signal of how strong the attractor is.

### Static vs. dynamic bound conflation

An agent proves a STATE inequality (bound holding at every configuration (R, C)) and claims it implies a GAME-LENGTH bound on L(n). **Not automatic.** Translating to L(n) requires independently bounding a scored quantity under some strategy — the online amortization step.

Many claimed sublinear closures break exactly at this step. When reviewing: "Is the state inequality doing work beyond a per-state bound? Does the translation to L(n) introduce an unbounded quantity?"

**Follow-up pattern for such claims**: "Your state inequality is sound as proved; the translation to L(n) = o(n) requires bounding [specific scored quantity] under [specific strategy]. Either prove that bound or refine to 'conditional sublinear bound modulo this lemma.'" Retractions and refinements are productive; encourage them.

### Multi-agent convergence on narrow gaps — trust it

When N ≥ 3 agents working in parallel, with different framings and partial information, **independently narrow to the same specific missing lemma**, that convergence is a very strong signal the gap is real and minimal. Qualitatively different from (and stronger than) N copies agreeing on a claim — here different agents independently *converge on* the same gap from different directions.

Observed in Erdős 872 R33–R36: fresh Pro, Pro A continuation, two different Codex dispatches all converged on a "freshness of lower-defect witnesses" lemma as the load-bearing step, each arriving via different machinery.

When you see this: write a single short paragraph naming the specific lemma and dispatch in parallel to all agents — closure by any one of them resolves the program.

### Empirical + analytical complementarity (arithmetic problems)

For problems with both abstract combinatorial structure AND specific arithmetic/geometric structure, dispatch complementary empirical and analytical agents:

- **Empirical**: "does the claimed amortization hold under adversarial strategies in the abstract model? Does it hold in a minimal arithmetic-structure-preserving model?"
- **Analytical**: "prove the lemma or refute with construction."

The contrast localizes the gap. Erdős 872 R36: empirically σ-vs-shadow_pressure FAILS in abstract H^(h) (peak ratio 6.71) but HOLDS in one-cylinder arithmetic (max 0–2). Localized the gap to arithmetic-specific structure without needing an analytical insight about why.

---

## Synthesis after a verifier round (see `sync-research-state` skill for full rubric)

Quick reference:

- **Unanimous sound** → promote to `Established`
- **Unanimous broken** → move to `Ruled Out` with specific failure mechanism as one-liner
- **Split (1 flags, 2 sound)** → re-read the flagger's argument carefully. Substantive → treat as broken pending re-derivation. Stylistic/confused → treat as sound.
- **A verifier raises a new angle** → becomes a specific fact in the next round's Established/Ruled Out/Numerical sections (never a suggestion slot)
- **Never promote on one verifier alone.** Agreement across ≥ 2 is the minimum bar.

Save verifier replies verbatim. Synthesize only when building the next researcher prompt.
