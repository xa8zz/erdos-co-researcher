# erdos-co-researcher

A harness for running an orchestrator agent that coordinates research across multiple reasoning models — GPT Pro, DeepThink, Codex, Gemini, Aristotle. Think of it as your AI co-researcher: it doesn't do the math, it handles state, prompt composition, verification routing, and commit discipline so the strong models can focus on reasoning.

Came out of a ~60-round push on Erdős #872 (got to ~0.190n upper bound). Works on any long-horizon research problem where a single model isn't enough.

## Getting started

```bash
git clone https://github.com/xa8zz/erdos-co-researcher my-research
cd my-research
claude   # or codex — anything that reads CLAUDE.md
```

Then run `/onboard` — walks you through your first problem and tool setup.

## Tooling

The orchestrator works best when it can actually reach across agents on its own. Hook up whatever makes that easier — [Browser Use CLI](https://github.com/browser-use/browser-use), [Vercel Browser](https://vercel.com/), Claude-in-Chrome MCP, Playwright, your own MCPs. Onboarding helps you pick. Also [Aristotle](https://harmonic.fun) if your problem has theorems to formalize.

`CLAUDE.md` explains how it all fits together.

License: MIT / CC-BY 4.0.
