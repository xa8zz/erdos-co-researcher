---
name: write-audit-prompt
description: Produce an informal-audit prompt for verifier tabs (Claude / Gemini / separate GPT-thinking). Use when the user says "write me an audit prompt", "give me the audit", "informal audit prompt", "wanna draft the audit".
---

# Write audit prompt

## When to use

After a researcher response lands, the user wants an audit prompt to paste into verifier tabs (parallel, unbiased, cross-family).

## Purpose

Adversarial audit that pressures the response for weaknesses, hidden assumptions, and literature connections — distinct from summarization.

## Instructions

1. Use this default template unless the claim is being promoted to `Established`, in which case use the longer adversarial variant:

```
I gave this prompt on a math problem to an AI and it came back with the
response below. Can you audit and analyze their response critically? Be
adversarial — find what breaks, flag any unclear steps, hidden assumptions,
or computational claims that need independent verification.

Separately, check the response against existing mathematical literature:
does the argument connect to, extend, reprove, or contradict any published
result (theorem, technique, inequality, construction)? If so, cite the
reference and describe the relationship.

## Prompt
[PASTE PROMPT HERE]

## Response
[PASTE RESPONSE HERE]
```

2. Fill the prompt and response placeholders with the verbatim content — never paraphrase.
3. If the claim is about to be promoted to `Established`, use the structured variant with explicit weakest-link / hidden-assumption / implication-check sections.
4. Send the same prompt to all verifiers in parallel — never bias one with what another said.

## Output

Markdown audit prompt ready to copy into a verifier tab.

## Gotchas

- **Verbatim, not paraphrase.** Paraphrasing loses the exact step where an error lives.
- **Adversarial framing is load-bearing.** Default verifier output drifts toward "looks good to me" — the explicit "find what breaks" instruction counteracts it.
- **Literature check** — web-enabled verifiers sometimes surface real references. Always include the literature clause.
- **Same prompt to all three** verifiers. Don't tell verifier #2 what verifier #1 said.
- **Be wary of consensus** — three verifiers agreeing they see no issue is weaker signal than two agreeing on the same specific flaw. Look for convergent specific objections.
