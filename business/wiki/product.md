# Product

## Cut AI coding token usage with a codebase knowledge graph

Claude Code (and similar AI coding tools) re-reads the whole codebase, file by file and function by function, every new session, burning thousands of tokens before you even ask a question.

Fix: run a tool like Graphify once over the repo. It scans files, functions, and architectural decisions and builds a compact knowledge graph (`GRAPH_REPORT.md` and `graph.json`). Point the AI assistant at that graph instead of raw files, and it navigates relationships instead of re-reading everything from scratch.

> "Every new Claude Code session, Claude rereads your entire codebase... Every single file and every function. That's thousands of tokens burned before you even ask a question."

> "It runs one time, scans your whole codebase, and builds a complete knowledge graph of everything inside it."

> "We're talking 70% less token consumption."

**Numbers:**
- Over 70% less total token usage; up to 71.5x fewer tokens per query on large codebases (tested at 52 files).
- Effectively turns a $17–20/month Pro plan into $100/month Max plan usage limits.

> "Your $20 plan basically turns into a $100 plan for free."

**How to apply:**
- Run Graphify (or equivalent) once on a repo before starting heavy AI coding sessions.
- Feed the AI agent the graph output instead of having it read raw source line-by-line.
- Relevant to keeping AI coding costs down while building Rekko's own stack.

## How AI models are trained: SFT vs RL

Two main ways AI models get post-trained:

- **Supervised Fine Tuning (SFT)** — the model mimics and copies correct answers from an annotated dataset. Best for one specific, predictable task.
- **Reinforcement Learning (RL)** — the model (agent) acts in an environment, gets rewarded or not for each action, and updates based on outcomes. Best for learning a broad range of general skills through trial and error.

> "You can think of an AI as a human in every sense of the word."

> "SFT is like teaching a child to mimic and copying the right answer, but RL is like tough love where you drop your kid into a playground..."

> "RL is better for learning a general variety of things, whereas SFT is better for learning a very specific task."

**How to apply:**
- Use SFT-style thinking when a Rekko feature needs specific, predictable output tied to clear examples (e.g. matching a client's exact tone from sample content).
- Use RL-style thinking when a feature needs to generalize across messy, varied situations (e.g. handling many different client industries/questions).
- Useful for explaining basic AI mechanics to clients or stakeholders in simple terms.

## Sources

- 2026-08-21-kayvon-jafarzadeh.md
- 2026-08-21-vardhan-agnihotri.md
