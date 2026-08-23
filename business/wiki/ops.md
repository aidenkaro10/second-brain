# Ops

## Delegate ops work to persistent AI bots (Grok Bot)

Grok Bot (from the SpaceX AI team) isn't one chatbot, it's a suite of bots, each assigned a specific job (scriptwriter, app dev manager, influencer outreach, attorney, docusigner, etc). You don't re-prompt them each time. They keep persistent context on how you talk and run in the background while you do other work.

> "Grok Bot is from the SpaceX AI team. It's not a chatbot. You get bots. Each one has a job, and they actually do the work."

> "They don't prompt them. You just treat them like a person. They already know how you talk, so you're not starting over every time."

> "I had a bunch of bots that were actually managing my development team for my app, managing our influencer team and outreach to more influencers so that I can get all that work done while doing the most important thing, which is content."

**Tactics:**
- Assign one bot per operational role (Scripter, AI Researcher, Influencer Coordinator, Full Stack Developer, Attorney, Docusigner).
- Bots run continuously without re-prompting since they retain context and brand tone.
- Run multiple bots at once on background tasks (coordinating app deploys, drafting scripts, finding influencers hitting 100k+ views/video).
- Comment "Grok" on the source post to get access to the tool.

**How to apply:**
- Set up dedicated AI bots for distinct business roles that keep persistent context on tone and style.
- Delegate multi-step ops tasks (influencer research, dev coordination) to bots running simultaneously in the background.
- Keep personal time on high-leverage human work (content) while bots handle admin/management.

## Teach Claude Code a skill by feeding it YouTube tutorials

Claude Code can't watch video by default, but you can give it that ability in 3 steps, then feed it top YouTube tutorials on any skill (video editing, cold email, outreach) so it learns and replicates the best techniques.

> "Code any skill by giving it abilities to watch YouTube."

> "Claude Code cannot watch anything by default. You fix that by installing this YouTube skill from Github that lets it pull transcripts, analyze video content, and extract any knowledge from a YouTube video."

> "You get a free Gemini API key from Google AI Studio, and Gemini already natively understands YouTube links because Google owns both of them."

> "So now your agents have two layers of understanding: the raw transcript for every word that was said in the video, plus Gemini's native understanding of the visuals."

**Tactics:**
1. Install the `watch-claude-video` skill from GitHub (`bradautomates/claude-video`) into Claude Code — gives it transcript + timestamped text extraction.
2. Get a free Gemini API key from Google AI Studio, connect it via the `youtube-studio-mcp` MCP server — Gemini reads native video frames/audio while Claude reads the transcript, giving two layers of understanding.
3. Feed ~10 high-quality YouTube tutorials on one subject into Claude Code to build a dedicated agent that executes using the best techniques across those videos.
- Free tier of Gemini API handles YouTube links directly, no cost.

**How to apply:**
- Install the `bradautomates/claude-video` skill to unlock transcript parsing in Claude Code.
- Connect the free Gemini API via MCP for frame-by-frame visual/audio analysis alongside the transcript.
- Build a Rekko-specific agent by feeding it top tutorials on sales outreach, SEO, or video editing to replicate proven techniques.

## Related

- [[product]] — also AI tooling/workflow lessons, complements the bot-delegation and skill-building approach here.

## Sources

- 2026-08-22-owen-nurminen.md
- 2026-08-22-rui-fu.md
