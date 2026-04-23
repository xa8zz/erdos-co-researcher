---
name: progress-zoom-out
description: Produce an honest "where are we" synthesis on the research program — what's proven, what's open, distance from final solution, obstructions. Use when the user says "help me zoom out", "where are we", "visualize progress", "0-100 rating", "be honest about where we are".
---

# Progress zoom-out

## When to use

User asks for program-level synthesis, distinct from individual-round recap. Typical triggers: "help me zoom out", "where are we", "visualize progress", "rate us 0-100", "be honest — how close are we".

## Purpose

Honest, specific progress assessment. Counteract the curator's tendency to reframe progress optimistically and the agent's tendency to reassure.

## Instructions

1. Read the current state doc + the most recent 3–5 round artifacts.
2. Produce a structured snapshot with four sections:
   - **Established** — rigorously proven, with key constants. Specific, not summary.
   - **Open question** — the precise current open question, one sentence.
   - **Obstructions** — what's been ruled out and why. Reference specific failure mechanisms.
   - **Distance from final solution** — what specific thing would close it. If a specific lemma or object has been named (e.g., "attention-lag parameter", "online covering-design interdiction"), name it.
3. If the user asks for 0-100 ratings, give two separate numbers:
   - **Novel math** — how much genuinely new structure the program has produced (theorems, lemmas, failure-mechanism catalog).
   - **Main-problem closure** — how close the central conjecture is to resolution.
   Justify each number with a one-line reason.
4. If asked to visualize as a graph, describe: x-axis as rounds (1 to N), y-axis as distance-to-closure. Mark forks at branching rounds, backtracks at refutations, plateaus where the same obstacle blocks multiple attempts.

## Output

Structured prose. ~4-6 sentences per section, not paragraphs. If ratings were requested, two numbers with justification.

## Gotchas

- **Be honest — don't reframe progress to sound better.** The user will catch it, as observed: *"I feel like you are being nice to me and trying to reframe progress."*
- **Novel math and closure progress are separable.** A program can produce highly novel structure (strong on novel-math axis) without closing the main problem (weak on closure axis). Say so.
- **Specific over vague.** "We're 70% there" means nothing. "We have sandwich bounds `c·n(log log n)²/log n ≤ L(n) ≤ 0.190n` and the remaining gap requires a new object (online covering-design interdiction) not derivable from current tools" means something.
- **Avoid false precision.** If the user asks for a rating, ground it in the state doc's specific evidence, not a made-up number.
- **Distinguish strategy-dependent from strategy-independent progress.** A theorem conditional on a specific adversary strategy is not the same as an unconditional result.
