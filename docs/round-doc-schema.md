# Round doc schema

Every research-round artifact has YAML front-matter. **The front-matter is immutable** — once written, never edited. `status` is never a field; it's always derived by the compile script from the `action` graph.

This is the same pattern as ADR supersedes, Git commits, academic citation: old records don't mutate; newer records override via relationships.

---

## Required fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Stable identifier, format `R<round>-<slug>`. Example: `R56-tau-sf-refuted`. |
| `type` | enum | `research` / `verification` / `refutation` / `synthesis` / `diagnostic` |
| `date` | date | ISO date when round was written. YYYY-MM-DD. |
| `intent` | string | 1–2 sentences on what this round aimed to answer. |
| `predecessors` | list of ids | Prior rounds this builds on. `[]` if standalone. |
| `claim` | string | The specific mathematical statement this round asserts. Dense, concrete. |

## Action field (relationship to prior work)

```yaml
action:
  kind: refutes         # standalone | refutes | supersedes | extends | confirms | orthogonal
  target: R52-sep-first # id being refuted/superseded/extended (omit for standalone / orthogonal)
```

This is the **only** mechanism by which a round affects another round's status. You never edit the target file. A new round with `action.kind=refutes` pointing at R52 is what "refutes R52."

## Optional fields

| Field | Type | Used for |
|---|---|---|
| `failure_mechanism` | string | **Required whenever `action.kind ∈ {refutes, supersedes}`, regardless of `type`.** The specific arithmetic/combinatorial feature that killed the target claim. Include constants, prime ranges, shield sets, lemmas. A `type: verification` doc with `action.refutes` carries `failure_mechanism` just like a `type: refutation`. |
| `implications` | list | Concrete consequences (e.g., "narrows attack space to X"). |
| `verifiers_at_time` | list | `[[verifier_id, verdict], ...]` where verdict ∈ `{agrees, disagrees, partial}`. |
| `confidence_at_time` | enum | `low` / `medium` / `high`. |
| `strategy_dependence` | string | Problem-specific axis (e.g., `independent` / `sigma-star-dependent` / `sigma-star-specific`). |
| `numerics` | list | For empirical rounds: `[{regime: "n=10^6", value: 0.887}, ...]`. |
| `prompt` | path | Repo-relative path to the prompt doc that produced this round (e.g., `erdos-872/prompts/researcher-R56-sep-first.md`). Skip if unknown or not applicable. |
| `siblings` | list of ids | For parallel dispatches to the same prompt (e.g., `pro-1`, `pro-2`, `pro-3`, `pro-4` all answering the same round), list the other instance ids. These are **not** `predecessors` — they have no causal dependency. Skip if no sibling dispatches. |

All optional fields are also immutable once written.

## Compile rules (how current state is derived)

1. Walk all round docs in `date` order.
2. For each round with `action.kind ∈ {refutes, supersedes}`: mark the target as refuted/superseded.
3. Later rounds can overturn an earlier verdict (e.g., R58 refutes R56's refutation of R52). Renderer shows the full chain.
4. Rounds with no later `refutes`/`supersedes` → **Established**.
5. Rounds with `type: refutation` and no later refutation → their **target** becomes **Ruled Out** in the state view (the target's original claim is preserved alongside the refutation's `failure_mechanism`).

## Full example

```yaml
---
id: R56-tau-sf-refuted
type: refutation
date: 2026-04-19
intent: >
  Determine whether τ_SF (separator-first Shortener strategy) can achieve
  O(r_1(n)) as proposed in R52.
predecessors: [R52-separator-first-hypothesis, R54-sigma-star-audit, R55-hidden-packet-collapse]
prompt: erdos-872/prompts/researcher-R56-tau-sf-probe.md
action:
  kind: refutes
  target: R52-separator-first-hypothesis
claim: >
  τ_SF fails as a full-game Shortener strategy. Prolonger can force
  L ≥ cn = ω(r_1(n)) via upper-half dyadic shielding.
failure_mechanism: >
  Prolonger plays an even element of U = (n/2, n] (killing prime 2), then
  preempts each separator s_Q with 2^a · s_Q ∈ U before Shortener can play
  it. Total cost: n^(1/8+o(1)) separator moves + O(n/log n) prime-block
  moves = o(r_1). After this phase, ≥ cn composites in U are untouched
  but τ_SF has no legal move.
implications:
  - Any separator-first Shortener needs a composite fallback rule to reach r_1.
  - Narrows remaining attack space: pure-separator strategies exhausted.
verifiers_at_time:
  - [claude-R56-audit, agrees]
  - [gemini-R56-audit, agrees]
confidence_at_time: high
strategy_dependence: tau-SF-specific
---

## Background

(full derivation of the refutation follows)
```

## Why never a `status` field

Mutability breaks auditability. If R52 is claimed, then refuted by R56, then reinstated under condition X by R58:

- With mutable `status`: R52's file has been written three times. The "why" of each flip is in free-text body. Hard to query, easy to lose.
- With immutable front-matter + action graph: R52 stays as originally written. R56 and R58 carry the verdict changes as first-class relationships. Full chain queryable.

This is the lab-notebook discipline. Don't erase the past; overwrite it with a later entry.

## Compile output shape (what the script produces)

```markdown
# Current state (compiled 2026-04-20)

## Established
- **R3-shield-reduction** (2026-04-17): Shield Reduction Theorem...
  Confirmed: [claude-R3, gemini-R3]. Confidence: high.
- ...

## Ruled Out
- **R52-separator-first-hypothesis** claimed τ_SF achieves O(r_1). Refuted by **R56-tau-sf-refuted** (2026-04-19).
  Failure mechanism: upper-half dyadic shielding — Prolonger plays an even...
- ...

## Open / Partial
- **R44-sflu-e** — conditional theorem, core step unproven.
- ...

## Active chains (verdict flips)
- R52 → refuted by R56 → reinstated under condition X by R58.

## Indices
- By type, by strategy dependence, by date — produced as separate tables.
```

Hyperlinks point to the full round doc for each entry. The compile output is regenerable — you never commit stale state.
