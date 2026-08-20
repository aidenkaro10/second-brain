# Build Your Own Second Brain

Two parts: a prompt you paste into Claude Code (it builds everything), then manual steps only you can do (accounts and keys).

---

## Part 1: The prompt

Open Claude Code in an empty folder and paste this whole block:

```
Build my "Second Brain" system in this folder. Read the whole spec, then build exactly this.

FOLDER STRUCTURE
- CLAUDE.md (master rules, root)
- school/, content/, business/ — each contains: raw/, raw/processed/, wiki/ (with index.md), chats/, CLAUDE.md
- prompts/gemini-extraction.md
- scripts/ingest.py
- app/server.py and app/index.html (chat UI)
- .env.example, .gitignore (ignore .env, video files, __pycache__, scripts/.ingest_state.json, scripts/.ingest_lock), requirements.txt, README.md

MASTER CLAUDE.MD
Role: librarian for three vaults (school = courses/study material, content = social media hooks/formats/viral breakdowns, business = startup marketing/sales/ops/product/decisions). Routing: answer from one vault's wiki, read index.md first, ask one short question if the vault is ambiguous. Compile procedure: read new files in raw/, merge into wiki/ per the vault's CLAUDE.md, prefer updating existing files, add [[wikilinks]], update index.md, move processed raw files to raw/processed/. Constraints: never delete info while compiling, never invent facts, every wiki claim cites its raw source filename under "## Sources", answer from wiki not general knowledge, present source disagreements explicitly. Style: short concise answers, numbered steps for how-tos, plain language, no em dashes.

VAULT CLAUDE.MDs
- content: organize by pattern type not creator (hooks/ folder with one file per hook type like curiosity-gap/contrarian/pov, formats.md, ctas.md, platform-tactics.md). Pattern files keep verbatim examples, a "why it works" breakdown, performance numbers when sources have them.
- school: organize by course then topic. Topic files: plain-language summary, key terms and formulas, likely exam questions, related topic links. Support "quiz me on X": ask one question at a time from wiki content, wait for the answer, grade it.
- business: organize by function (marketing, sales, ops, product, finance) plus mindset.md and decisions-log.md (dated decisions with reasoning, never rewrite past entries). Video breakdowns tagged #business: compile the LESSON with verbatim quotes into the matching function file, never stall waiting for input.

GEMINI EXTRACTION PROMPT (prompts/gemini-extraction.md)
Sent to Gemini with each video. Output markdown with exactly: FRONTMATTER (yaml: source_url, platform, creator, date_processed), HOOK (verbatim first 3 seconds, spoken + on-screen text), SCENE-BY-SCENE (timestamped visuals, cuts, overlays, pacing), FULL TRANSCRIPT (verbatim, no summarizing, mark unclear audio [inaudible]), WHY IT WORKS (max 5 bullets). Markdown only, no preamble.

INGEST SCRIPT (scripts/ingest.py, python3)
1. Lock file so two runs never overlap (skip if lock exists and is under 2 hours old, clean it via atexit).
2. Poll the Telegram bot getUpdates API (token + allowed chat id from .env). Each message = a link + optional #school/#content/#business tag, default content. Only accept the allowed chat id.
3. YouTube links: pass URL straight to Gemini (it accepts YouTube URLs natively). TikTok/Instagram: download with yt-dlp to a temp dir, upload the file to Gemini, delete the local file ONLY after Gemini returns non-empty output. Also delete the Gemini server-side copy after.
4. Append to the Gemini prompt: the video URL, today's real date, and the creator name from yt-dlp metadata (Gemini can't know these).
5. Model and keys from .env (GEMINI_MODEL, GEMINI_API_KEY).
6. Save output to the tagged vault's raw/ as YYYY-MM-DD-{creator-slug}.md, add -2/-3 suffix instead of overwriting.
7. After saving, run the claude CLI headless to compile: look for claude on PATH and also at ~/.local/bin/claude (cron has a minimal PATH). Command: claude -p "New files were added to raw/. Compile them per CLAUDE.md." --permission-mode acceptEdits, cwd repo root, 30 min timeout. If not found, log and skip.
8. Reply on Telegram: "Saved: filename (vault)" or the error. Wrap each link in try/except so one bad link never kills the run. Track processed message ids + last update id in scripts/.ingest_state.json.

CHAT APP (app/, Flask, single HTML page, no build step)
- Dropdown: School, Content, Business, All (default Content). Chat box, messages in the middle, input at bottom. Clean minimal UI.
- POST /api/chat: build context = root CLAUDE.md + selected vault's CLAUDE.md + wiki/index.md + wiki files keyword-matched to the query (cap total context ~100k chars). "All" = same across all three vaults, and track which vault matched most. Send to the Anthropic API (key + model from .env), system prompt says: answer ONLY from the provided wiki content, say so if the wiki lacks the answer, short concise style. Return the answer.
- Every assistant answer gets a Save button: POST /api/save writes the Q&A as markdown to the vault's chats/ as YYYY-MM-DD-{slug}.md with date/vault frontmatter. When the dropdown was All, save to the vault the answer matched most, fallback business.
- No accounts, no database, history in memory only.
- Serve on http://127.0.0.1:5001.

CONFIG
- .env.example with comments: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, GEMINI_API_KEY, GEMINI_MODEL=gemini-3.6-flash, ANTHROPIC_API_KEY, ANTHROPIC_MODEL=claude-sonnet-5
- requirements.txt pinned: requests, python-dotenv, yt-dlp, google-genai, anthropic, flask
- README: beginner setup steps (install, BotFather, keys, cron every 15 min, first test) and the collect/compile/query explanation.

Then run: pip3 install --user -r requirements.txt, verify both python files compile, and git init + first commit.
```

---

## Part 2: Manual steps (accounts and keys)

Claude can't make accounts for you. Do these yourself:

### Telegram bot

1. Install Telegram on your phone and sign up.
2. Search **BotFather** (blue checkmark), tap Start.
3. Send `/newbot`. Give it a name, then a username ending in `bot`.
4. Copy the token it replies with (looks like `8123456789:AAF...`).
5. Tap the `t.me/...` link to your new bot, press Start, send it `hi`.

### API keys

1. Gemini key: https://aistudio.google.com/apikey → Create API key → copy.
2. Anthropic key: https://console.anthropic.com/settings/keys → Create Key → copy. (Needs an Anthropic account with billing set up.)

### The .env file

1. In your project folder, copy the example: `cp .env.example .env`
2. Open `.env` in any editor and paste each value after its `=` sign. No spaces, no quotes.
3. For `TELEGRAM_CHAT_ID`: open `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` in a browser (replace `<YOUR_TOKEN>`), find `"chat":{"id":` and copy the number. Or just ask Claude Code to fetch it for you.
4. Save. Never commit or share this file.

### Turn on the automation

1. Ask Claude Code: "add a cron job that runs scripts/ingest.py every 15 minutes" (or see the README for the crontab line).
2. Install the Claude Code CLI if you don't have it, and make sure it's logged in (run `claude` in Terminal once).
3. Test: send your bot a YouTube or TikTok link, run `python3 scripts/ingest.py`, watch for the Telegram confirmation.
4. Chat with it: `python3 app/server.py` then open http://localhost:5001.

### Gotchas we hit so you don't have to

- School/office WiFi often blocks TikTok downloads. Use a hotspot.
- If Gemini errors with "model not available", update GEMINI_MODEL in .env to whatever model name the error suggests.
- Your Mac must be awake for the 15-minute automation to run.
