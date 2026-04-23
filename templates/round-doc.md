---
id: R<NN>-<slug>
type: research                    # research | verification | refutation | synthesis | diagnostic
date: 2026-MM-DD
intent: >
  <1-2 sentence statement of what this round aimed to answer>
predecessors: []                  # list of prior round ids this builds on
# prompt: <path>                  # optional: repo-relative path to the prompt that produced this round
action:
  kind: standalone                # standalone | refutes | supersedes | extends | confirms | orthogonal
  # target: R<NN>-<slug>          # required when kind != standalone and kind != orthogonal
claim: >
  <the specific mathematical statement this round asserts>
# failure_mechanism: >            # required for type: refutation
#   <specific arithmetic/combinatorial feature that killed the target claim,
#    with constants, prime ranges, shield sets, lemmas>
# implications:
#   - <concrete consequence>
# verifiers_at_time:
#   - [claude-<round>-audit, agrees]
#   - [gemini-<round>-audit, agrees]
# confidence_at_time: medium      # low | medium | high
# strategy_dependence: independent # problem-specific
# numerics:
#   - { regime: "n=10^6", value: 0.887 }
---

## <Section heading>

<Full content of the round doc — prose proof, analysis, verbatim model output,
whatever fits the round type.>
