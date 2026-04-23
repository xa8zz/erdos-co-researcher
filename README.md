# erdos-co-researcher

Clone to set up a simple agent co-researcher for your own long-horizon research. Came out of work on Erdős #872 with Claude Code + Codex. The orchestrator doesn't do the math — it just handles the coordination, prompting, and commit discipline so the strong research models (Pro, DeepThink, etc.) can focus on reasoning.

```bash
git clone https://github.com/xa8zz/erdos-co-researcher my-research
cd my-research
claude   # or codex
```

Then run `/onboard`.

Worth hooking up browser automation so the co-researcher can read/write chat tabs on its own — [Browser Use CLI](https://github.com/browser-use/browser-use), [Vercel Browser](https://vercel.com/), Claude-in-Chrome, Playwright, whatever fits. Onboarding helps pick. Also [Aristotle](https://harmonic.fun) if you have theorems.

License: MIT / CC-BY 4.0.
