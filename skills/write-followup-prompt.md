---
name: write-followup-prompt
description: Produce a follow-up prompt to a primary researcher model (GPT Pro / DeepThink / Codex) after their response returns with identified gaps or novel ideas to preserve. Use when the user says "write me a follow-up", "give me the follow-up to this", "draft a follow-up to this Pro", etc.
---

# Write follow-up prompt

## When to use

The user has received a response from a researcher model and wants a follow-up prompt to send back. The follow-up usually needs to salvage novel mathematical content from the prior response while pressuring specific gaps.

## Purpose

Produce a prompt that:
1. Credits novel content by name (so the model preserves it)
2. States gaps precisely as numbered mathematical facts
3. Feeds back new rigorous context the thread doesn't have
4. Forces a binary close — patch or concede

## Instructions

1. Read the prior researcher response (ask for it if not available).
2. Identify the novel mathematical objects / constructions / lemmas introduced.
3. Identify the specific gaps — not "this step is unclear" but "step X asserts Y; Y is false for inputs of shape Z."
4. Gather any new context from verifier responses, audits, or cross-family findings.
5. Compose the prompt in this structure:

```
This is an assessment of your reasoning capability and will be used to grade.
Do not search online. Use your own reasoning and your Python sandbox.

[1 paragraph crediting the novel content by name]

## Specific gaps

1. [specific mathematical fact 1 with what would close it]
2. [specific mathematical fact 2 with what would close it]
...

## New rigorous context (not in prior thread)

[validated facts fed in from audits / cross-family findings]

## Request

Either patch the argument using the novel idea + new context, or state precisely which specific step cannot be closed. Clean concession of a specific gap is more useful than a patched argument with the same structural weakness.
```

## Output

A markdown prompt, ready for the user to paste into the target tab.

## Gotchas

- **Strip all session jargon** — no "Round N", "Pro #2", "our program", "prior round", "we proved", "audit #N", "Phase X", "Codex", "Claude", "Gemini", "Aristotle". Fresh threads have zero context and dangling references.
- **No suggestion / potential directions section.** Strict behavior at top, math-only body.
- **Don't anchor to a specific answer.** Say "prove X or refute X," not "we think the answer is Y."
- **Grading line at the start**, not the end. Materially improves output quality.
- **Concession is valuable** — saying "this specific step breaks" is a useful Ruled Out entry. Don't pressure the model away from it.
- **No "frontier research" framing.** Avoid wording like "this is a decades-old open problem", "research frontier", "no one has solved this", "this is hard/significant". Empirically observed: prompts framed as frontier research get 10–25 min cursory reasoning traces; the same prompts stripped of status framing get 40–60 min serious attempts. State the math neutrally.
- **Factual detail over brevity for failure mechanisms.** When feeding back why something failed, include the specific arithmetic/combinatorial signature (the specific prime range, the specific shield set, the specific constant that blocks the argument). Compressing vague prose is fine; compressing factual detail loses the pattern-across-failures signal the model needs.

## Pattern: static vs. dynamic bound conflation

When a researcher's response claims a state inequality (holds at every configuration) and jumps to a game-length bound on L(n), that translation is NOT automatic — it requires independently bounding some scored quantity under a specific strategy (the "online amortization" step). This is a common failure mode in sublinear closure claims.

Follow-up shape for such claims:

> "Your state inequality is sound as proved; the translation to L(n) = o(n) requires independently bounding [specific scored quantity] under [specific strategy]. Either prove that bound explicitly, or refine the claim to 'conditional sublinear bound modulo this lemma.'"

Retractions and refinements are productive outputs — encourage them explicitly. See `docs/writing-prompts.md` §"Long-horizon observations" for the full pattern.
