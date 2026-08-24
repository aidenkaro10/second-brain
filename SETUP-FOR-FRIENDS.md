# Build Your Own Second Brain

Two parts: a prompt you paste into Claude Code (it builds everything), then manual steps only you can do (accounts, keys, and Mac permissions).

Works on Mac. Budget about an hour for the full setup.

---

## Part 0: Install Python first

The built-in Mac Python is too old for the video downloader.

1. Go to https://www.python.org/downloads/ and download the latest Python (3.12 or newer).
2. Open the installer and click through it.
3. Everything below uses `/usr/local/bin/python3` (that's the one you just installed).

---

## Part 1: The prompt

Open Claude Code in an empty folder and paste this whole block:

```
Build my "Second Brain" system in this folder. Read the whole spec, then build exactly this.

FOLDER STRUCTURE
- CLAUDE.md (master rules, root)
- school/, content/, business/ — each contains: raw/, raw/processed/, wiki/ (with index.md and overview.md), chats/, CLAUDE.md
- prompts/gemini-extraction.md
- scripts/ingest.py
- app/server.py and app/index.html (chat UI)
- .env.example, .gitignore (ignore .env, video files, __pycache__, scripts/.ingest_state.json, scripts/.ingest_lock), requirements.txt, README.md

MASTER CLAUDE.MD
Role: librarian for three vaults (school = courses/study material, content = social media hooks/formats/viral breakdowns, business = startup marketing/sales/ops/product/decisions). Routing: answer from one vault's wiki, read index.md first, ask one short question if the vault is ambiguous. Compile procedure: read new files in raw/, merge into wiki/ per the vault's CLAUDE.md, prefer updating existing files, add [[wikilinks]], update index.md, move processed raw files to raw/processed/. Each vault's wiki/overview.md is the owner's personal profile for that area (their plans, niche, services, schedule), NOT a summary of collected videos; it updates mainly from chats and is exempt from source citations. Constraints: never delete info while compiling, never invent facts, every other wiki claim cites its raw source filename under "## Sources", answer from wiki not general knowledge, present source disagreements explicitly. Style: short concise answers, numbered steps for how-tos, plain language, no em dashes.

VAULT CLAUDE.MDs
- content: organize by pattern type not creator (hooks/ folder with one file per hook type like curiosity-gap/contrarian/pov, formats.md, ctas.md, platform-tactics.md). Pattern files keep verbatim examples, a "why it works" breakdown, performance numbers when sources have them.
- school: organize by course then topic. Topic files: plain-language summary, key terms and formulas, likely exam questions, related topic links. Support "quiz me on X": ask one question at a time from wiki content, wait for the answer, grade it.
- business: organize by function (marketing, sales, ops, product, finance) plus mindset.md and decisions-log.md (dated decisions with reasoning, never rewrite past entries). Video breakdowns tagged #business: compile the LESSON with verbatim quotes into the matching function file, never stall waiting for input.

GEMINI EXTRACTION PROMPT (prompts/gemini-extraction.md)
Sent to Gemini with each video. Output markdown with exactly: FRONTMATTER (yaml: source_url, platform, creator, date_processed), HOOK (verbatim first 3 seconds, spoken + on-screen text), SCENE-BY-SCENE (timestamped visuals, cuts, overlays, pacing), FULL TRANSCRIPT (verbatim, no summarizing, mark unclear audio [inaudible]), WHY IT WORKS (max 5 bullets). Markdown only, no preamble.

INGEST SCRIPT (scripts/ingest.py, runs on /usr/local/bin/python3)
1. Lock file so two runs never overlap (skip if lock exists and is under 2 hours old, clean it via atexit).
2. Poll the Telegram bot getUpdates API (token + allowed chat id from .env). Each message = a link OR a photo (screenshot, slide, whiteboard, textbook page) + optional #school/#content/#business/#advice tag, default content. Photos: download via Telegram getFile, send bytes to Gemini with prompts/gemini-photo.md (verbatim text, what it shows, takeaways for the tagged purpose), save to the vault raw/. #advice saves to the content vault but uses a lesson-extraction prompt (for videos ABOUT making content) and compiles into strategy/ topic files. #mine is for the owner's OWN posted videos: saved as raw/mine-*.md with a prompt that adds an honest critique section, and compiled into wiki/my-videos.md as a running posting log (newest first, with a Performance line to fill in later) instead of being filed as pattern examples. Only accept the allowed chat id.
3. YouTube links: pass URL straight to Gemini (it accepts YouTube URLs natively). TikTok/Instagram: download with yt-dlp to a temp dir, upload the file to Gemini, delete the local file ONLY after Gemini returns non-empty output. Also delete the Gemini server-side copy after.
4. Instagram links need a logged-in session: pass yt-dlp the option cookiesfrombrowser = ("chrome", CHROME_PROFILE, None, None) where CHROME_PROFILE comes from .env (default "Default"). TikTok and YouTube need no login.
5. Append to the Gemini prompt: the video URL, today's real date, and the creator name from yt-dlp metadata (Gemini can't know these).
6. Model and keys from .env (GEMINI_MODEL, GEMINI_API_KEY).
7. Save output to the tagged vault's raw/ as YYYY-MM-DD-{creator-slug}.md, add -2/-3 suffix instead of overwriting.
8. After saving, run the claude CLI headless to compile: look for claude on PATH and also at ~/.local/bin/claude (cron has a minimal PATH). Command: claude -p "New files were added to raw/. Compile them per CLAUDE.md." --permission-mode acceptEdits, cwd repo root, 30 min timeout. If not found, log and skip.
9. Reply on Telegram: "Saved: filename (vault)" or the error. Wrap each link in try/except so one bad link never kills the run. Track processed message ids + last update id in scripts/.ingest_state.json.

CHAT APP (app/, Flask, single HTML page, no build step)
- Vault pills at top: School, Content, Business, All (default Content). Each vault keeps its OWN separate conversation; switching pills switches conversations. Messages middle, input bottom. Clean minimal responsive UI that works on phone screens, dark mode via prefers-color-scheme, tiny safe markdown renderer for answers (escape all HTML first).
- POST /api/chat: build context = root CLAUDE.md + selected vault's CLAUDE.md + wiki/index.md + wiki/overview.md always, plus ALL other wiki files ranked by keyword match to the query (cap total context ~100k chars). "All" = same across all three vaults, track which vault matched most. Send to the Anthropic API (key + model from .env), system prompt: answer ONLY from the provided wiki content, say so if the wiki lacks the answer, short concise style. Return the answer.
- After each answer, a background thread sends the exchange + the vault's overview.md to the Anthropic API: if the USER's message revealed something new and lasting about their own plans/niche/services/schedule/goals, rewrite overview.md with it merged in (replace outdated facts, don't stack). Output UNCHANGED sentinel if nothing new. Use a per-vault threading.Lock for the file write.
- A paperclip attach button: images, PDFs, and text files go with the message as native Anthropic image/document blocks (text files pasted as text). An "also save to vault" checkbox drops the raw file into the vault raw/ for the compiler. Only the newest turn carries attachments; history keeps a text note of the file names.
- Every answer gets a Save button: POST /api/save writes the Q&A as markdown to the vault's chats/ as YYYY-MM-DD-{slug}.md with date/vault frontmatter. When the pill was All, save to the vault the answer matched most, fallback business.
- No accounts, no database, chat history in memory only.
- Serve with host 0.0.0.0 port 5001 so phones on the same network can reach it.

CONFIG
- .env.example with comments: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, GEMINI_API_KEY, GEMINI_MODEL=gemini-3.6-flash, ANTHROPIC_API_KEY, ANTHROPIC_MODEL=claude-sonnet-5, CHROME_PROFILE=Default
- requirements.txt: requests, python-dotenv, yt-dlp (latest), google-genai, anthropic, flask
- README: beginner setup steps (install, BotFather, keys, cron every 15 min, first test) and the collect/compile/query explanation.

Then run: /usr/local/bin/python3 -m pip install --user -r requirements.txt, verify both python files compile, and git init + first commit.
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
3. For `TELEGRAM_CHAT_ID`: ask Claude Code to fetch it for you after you've messaged your bot (or open `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` in a browser and find `"chat":{"id":`).
4. Save. Never commit or share this file.

### Instagram (optional, skip if you only save TikToks/YouTube)

Instagram requires a logged-in account to download reels.

1. Know your Mac login password. If you don't, sort that first (restart → wrong password 3 times → reset via Apple Account).
2. Log into instagram.com in Chrome on your Mac and stay logged in.
3. Find your Chrome profile name: ask Claude Code to check which folder under `~/Library/Application Support/Google/Chrome/` has the newest `Cookies` file ("Default", "Profile 1", ...). Put that name in `.env` as `CHROME_PROFILE`.
4. The first Instagram ingest pops up a "Chrome Safe Storage" password box: type your Mac password and click **Always Allow**.

### Mac permissions (needed or the automation silently fails)

macOS blocks background programs from reading your files until you allow it:

1. System Settings → Privacy & Security → **Full Disk Access**.
2. Click **+**, press Cmd+Shift+G, type `/usr/sbin/cron`, Enter, Open.
3. Click **+** again, Cmd+Shift+G, paste the path to your installed Python's app bundle (ask Claude Code for it, looks like `/Library/Frameworks/Python.framework/Versions/3.XX/Resources/`, pick **Python.app**).
4. Both toggles on.

### Turn on the automation

1. Ask Claude Code: "add a cron job that runs scripts/ingest.py with /usr/local/bin/python3 every 15 minutes".
2. Install the Claude Code CLI if you don't have it and make sure it's logged in (run `claude` in Terminal once, it should greet you by name).
3. Test: send your bot a YouTube or TikTok link, run `/usr/local/bin/python3 scripts/ingest.py`, watch for the Telegram confirmation.
4. Chat with it: `/usr/local/bin/python3 app/server.py` then open http://localhost:5001.
5. Optional: ask Claude Code to "make the chat app auto-start on login with a LaunchAgent" so it survives restarts.

### Use it on your phone (optional)

Your phone can only reach the app if it can reach your Mac:

1. Easiest reliable way: install **Tailscale** (free) on both the Mac and your phone, log into both with the same Google account.
2. Ask Claude Code to "enable tailscale serve for port 5001" (it gives you an https link, approve the enable page it prints).
3. Open that link in Safari on your phone → Share → **Add to Home Screen**.

### Gotchas we hit so you don't have to

- School/office WiFi often blocks TikTok downloads entirely. Use a phone hotspot for TikToks.
- If Gemini errors with "model not available", update GEMINI_MODEL in .env to whatever model the error suggests.
- Your Mac must be on and awake for the 15-minute automation to run.
- Chrome must be properly installed (dragged into Applications), not run from the downloaded .dmg file.
- If a keychain popup rejects a password you're sure is right, your keychain is locked with an older password. Keychain Access → Settings → Reset Default Keychains, then log out and in.
- Don't send the same video twice from two platforms, you'll get duplicate notes.
