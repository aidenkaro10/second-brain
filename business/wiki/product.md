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

## Avoid "AI slop" UI in vibe-coded apps

AI-assisted ("vibe coded") apps often end up looking visually generic and unrefined. Use curated design resource sites to fix color, layout, and interactivity instead of shipping the default AI look.

> "how to make your app not feel like AI SLOP"

> "Does your vibe coded app look like this, when really you want it to look like this?"

**Tools:**
- **Coolors (coolors.co)** — generate or browse curated color palettes to replace generic UI themes.
- **Motion Sites (motionsites.ai)** — browse hero/landing page designs and copy the UI prompt straight into an AI coding agent.

  > "Second website is motionsites.ai which has a bunch of unique heroes and landing pages which you can use to get inspiration and even copy the prompt right into your AI agent."

- **21st.dev** — thousands of plug-and-play React components to make an app feel more alive.

  > "Third is 21st.dev which has thousands of React components that you can use to make your app feel more alive and plug right into anything you build."

- **Layer** — micro-interactions, animations, and UI component inspiration for a more personal feel.

**How to apply:**
- Swap default/generic color themes for a palette pulled from Coolors.
- Copy a Motion Sites layout prompt into the coding agent instead of letting it default to a generic hero section.
- Pull in 21st.dev components and Layer micro-animations for Rekko's UI instead of leaving default AI-generated interactions.

## Avoid "AI slop" UI via agent skills + MCP

Same "AI slop" problem as above, different fix: instead of pulling design inspiration from websites, equip the AI coding agent itself (Claude, Codex) with skills and MCP integrations that enforce design rules and pull real components, so it stops generating generic UI in the first place.

> "This is what AI slop looks like now. And if you think you can just ask Claude to make it look better, well, you're just wasting your time."

**Tools:**
- **Impeccable skill** — detects anything that looks like AI slop on your UI and fixes it (commands like `/polish`, `/distill`, `/clarify`).
  > "This skill will literally detect anything that looks like AI slop on your UI and fix it for you."
- **21st.dev MCP** — plug into Codex or Claude so it pulls pre-built, high-quality UI components instead of writing everything from scratch.
  > "Then use the 21st dev MCP. You can plug it into Codex or Claude, and it will pull beautiful UI components instead of writing everything from scratch."
- **Vercel Web Interface Guidelines skill** — gives the agent a checklist for UX/accessibility standards on every UI it builds.
  > "It will basically give your agent a checklist for everything it needs to get a clean UI."

**How to apply:**
- Run the Impeccable skill on existing AI-generated UI to audit and refactor it.
- Connect 21st.dev via MCP so the agent sources real components instead of freestyling.
- Add Vercel's Web Interface Guidelines as agent context so it follows UX/accessibility standards by default.

See also "Avoid 'AI slop' UI in vibe-coded apps" above — same problem, this fix lives inside the AI agent's workflow instead of being a website you copy from.

## The 3 levels of vibe coders

AI-assisted coding ("vibe coding") splits into three skill levels, from generic AI output to production-quality code.

> "The 3 Levels of Vibe Coders"

- **Level 1** — basic prompts, no planning, no guidance files. Produces "AI slop": generic gradient text, scroll animations, side-tap borders.
  > "That landing page has typical patterns of AI like gradient text, scroll animations, and side tap borders."
  - Doesn't use `Agent.md` files or custom AI skills to steer the model.
  - Skips plan mode before implementing new features.

- **Level 2** — adds structure: a UI design base, basic AI skills, and plan-before-execute mode.
  > "Use shadcn for the base of the UI"
  - Builds UI on a design system like `shadcn` so the AI isn't rebuilding UI logic from scratch.
  - Adds basic AI skills via CLI (e.g. `npx skills add ... --skill frontend-design` or `--skill shadcn`).
  - Uses Plan Mode for complex features: 1) Plan Mode, 2) Read/review plan, 3) Approve plan before it runs.
  > "Plan mode for complex features: 1. Plan Mode, 2. Read/Review Plan, 3. Approve Plan"

- **Level 3** — advanced AI agent skills, tech-specific skill extensions, and proven libraries instead of custom-built logic.
  - Integrates advanced skill libraries (e.g. Matt Pocock skills, Anthropic's Claude Code security review plugin).
  - Installs official skills for the exact stack in use (e.g. Supabase agent skills, Convex agent skills).
  > "Add official skills for installed tech"
  - Searches for existing proven libraries rather than having the AI rebuild everything from scratch.
  > "They try to search for existing proven libraries rather than have AI rebuild everything from scratch."

**How to apply:**
- Set up a `shadcn` (or similar) UI base before generating any screens, so the AI styles within a system instead of freestyling.
- Turn on plan mode for any non-trivial feature: make Claude Code plan first, read the plan, then approve before it writes code.
- Install official Claude Code skills for whatever backend Rekko is actually using (Supabase, Convex, etc.) instead of letting the AI hand-roll that logic.
- Before asking AI to build something from scratch, check if a proven library already does it.

See also "Avoid AI slop UI in vibe-coded apps" above — same problem (generic AI output), different fix (workflow discipline vs. design resources).

## Sources

- 2026-08-21-kayvon-jafarzadeh.md
- 2026-08-21-vardhan-agnihotri.md
- 2026-08-24-ranveer-singh.md
- 2026-08-24-nico-burkart.md
- 2026-08-25-aimn.md
