# erdos-co-researcher

A harness for running an orchestrator agent — your AI co-researcher — that coordinates across multiple reasoning models (GPT Pro, DeepThink, Codex, Gemini, Aristotle) to push on hard open problems.

The orchestrator keeps state clean, composes neutral math-first prompts, routes outputs through parallel adversarial verifiers, formalizes claims in Lean via Aristotle, and commits a permanent record per round. It does not solve the math — it builds the infrastructure that lets strong research models do their best work.

Emerged from a 60+ round research program on **Erdős Problem #872** (contributed to a ~0.190n upper bound). Generalizes to any long-horizon research effort where a single strong model isn't enough and you need multiple agents audited against each other.

## Getting started

```bash
git clone <this-repo> my-research
cd my-research
claude  # or your preferred Claude Code-compatible CLI
```

Then run `/onboard`. The skill interviews you on your problem, scaffolds your first problem directory, walks you through tool discovery, and gets you to your first dispatch.

## Suggested setup

The harness works best when your co-researcher can reach across agents on your behalf — read chat tabs, extract responses, file them into round docs — without you manually copy-pasting. Onboarding walks through options. The most common rough edges people tool around:

- **Browser automation** — pulling research outputs out of ChatGPT/Claude/Gemini tabs byte-faithfully. Good starting points: [Browser Use CLI](https://github.com/browser-use/browser-use), [Vercel Browser CLI](https://vercel.com/), Claude-in-Chrome MCP, or a Playwright-backed custom MCP. Anything that exposes "read tab content" + "fill textbox" primitives works.
- **Formal verification** — [Aristotle](https://harmonic.fun) for Lean 4 if your problem has theorem/lemma claims. Very high-signal filter before promoting claims to `Established`.
- **Your own MCPs** — add whatever makes the orchestrator's prompting + verification routing easier for your domain.

You're encouraged to explore and add your own tooling. The onboarding skill will help you evaluate what fits.

## How it works

Read [CLAUDE.md](CLAUDE.md). It's the orchestrator's full operating manual — the role, the research loop, the frontmatter discipline, the mandatory protocols that fire on every user paste, the long-horizon diagnostic frames for when research stalls.

## License

MIT for code. CC-BY 4.0 for docs and templates.
