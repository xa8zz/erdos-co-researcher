# Adversarial audit prompt template

Use when a claim is about to be promoted to `Established` and you want a structured stress test. For most audits, use the shorter `templates/informal-audit.md` instead.

```
Below is the current state of a problem plus a new claim from a primary
researcher. Rigorously audit the new claim. Be adversarial — your job is to
find what breaks.

## Problem

<Same neutral statement as the researcher prompt.>

## Established Facts

<Same bulleted list as the researcher prompt, abridged is fine.>

## The New Claim

<Verbatim excerpt from the researcher's latest output. Do NOT paraphrase —
the verifier needs to see what the researcher actually wrote.>

## Your job

- Does the argument hold as stated?
- What is the weakest link?
- Are there computational claims that need independent verification?
- Are there hidden assumptions the researcher didn't flag?
- Does the claim actually imply what the researcher says it implies?
- What would a skeptic push back on?

Separately, check the claim against existing mathematical literature: does the
argument connect to, extend, reprove, or contradict any published result? If
so, cite the reference.

If the claim is sound, say so plainly. If broken, explain precisely where.
```

## When to use this vs the informal audit

- **Informal audit** (default, `templates/informal-audit.md`): for routine per-round verifications. Shorter, paste-prompt-and-response shape.
- **Adversarial audit** (this file): for promotion-grade claims where the state doc would change materially if the claim survives. Structured weakest-link + implication + skeptic-pushback framing.

## Gotchas

- **Verbatim excerpt, not paraphrase.** Paraphrasing loses the exact step where an error might live.
- **Same prompt to all verifiers in parallel.** Don't tell one verifier what another said — unbiased convergence is the signal.
- **Ask for the weakest link explicitly.** Otherwise verifiers default to summarization.
- **Ask for literature connections.** Web-enabled verifiers sometimes surface real references.
