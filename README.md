# Second Brain

A personal AI knowledge base with three vaults: **school**, **content**, and **business**.

**How it works:** You send a video link to your Telegram bot. A script picks it up, has Gemini watch the video and write a full breakdown (hook, scene-by-scene, transcript, analysis), and saves that breakdown as a raw note in the right vault. Claude then compiles raw notes into a clean wiki, merging new information into existing notes and linking related ideas. When you want answers, a local chat app reads the relevant wiki files and asks Claude, so answers come from what you collected, not from generic AI knowledge. Collect, compile, query.

## Setup

### 1. Clone and install

1. Open Terminal.
2. Run:

```bash
git clone https://github.com/YOUR_USERNAME/second-brain.git
cd second-brain
pip3 install -r requirements.txt
```

### 2. Create your Telegram bot

1. Open Telegram and search for **BotFather**.
2. Send it `/newbot`.
3. Give the bot a name (e.g. `Second Brain`) and a username (e.g. `aiden_secondbrain_bot`).
4. Copy the token it gives you (looks like `123456789:AAF...`).
5. Open a chat with your new bot and send it any message (e.g. `hi`). This lets the script find your chat id.

### 3. Set up your keys

1. Copy the example env file:

```bash
cp .env.example .env
```

2. Open `.env` in any editor and paste your BotFather token after `TELEGRAM_BOT_TOKEN=`.
3. Get your chat id: open this URL in a browser (replace `<TOKEN>` with your bot token): `https://api.telegram.org/bot<TOKEN>/getUpdates`. Find `"chat":{"id":` and copy the number after it. Paste it after `TELEGRAM_CHAT_ID=`.
4. Get a Gemini API key at https://aistudio.google.com/apikey and paste it after `GEMINI_API_KEY=`.
5. Get an Anthropic API key at https://console.anthropic.com/settings/keys and paste it after `ANTHROPIC_API_KEY=`.

### 4. First run

1. Send your bot a TikTok, Instagram, or YouTube link. Add a tag to pick the vault: `#school`, `#content`, or `#business`. No tag means content.
2. Run the ingest script:

```bash
python3 scripts/ingest.py
```

3. The bot replies with the saved note's name. The breakdown is now in that vault's `raw/` folder, and if the `claude` CLI is installed, it compiles into the vault's `wiki/` automatically.

### 5. Run it automatically every 15 minutes (cron)

1. Run:

```bash
crontab -e
```

2. Press `i`, paste this line (fix the path if your folder lives somewhere else), then press Esc and type `:wq`:

```
*/15 * * * * cd /Users/Annabelle/Documents/projects/second-brain && /usr/bin/python3 scripts/ingest.py >> /tmp/secondbrain-ingest.log 2>&1
```

3. macOS note: the first time cron runs, macOS may ask to give `cron` access to your files. If nothing happens, open System Settings, then Privacy & Security, then Full Disk Access, and turn on `cron` (press Cmd+Shift+G in the file picker and type `/usr/sbin/cron`).

### 6. Chat with your second brain

1. Run:

```bash
python3 app/server.py
```

2. Open http://localhost:5001 in your browser.
3. Pick a vault from the dropdown (School, Content, Business, or All) and ask a question.
4. Click **Save** under any answer to keep it as a note in that vault's `chats/` folder.

### 7. Browse your vaults in Obsidian (optional)

1. Download Obsidian from https://obsidian.md.
2. Open Obsidian, click **Open folder as vault**, and pick this `second-brain` folder.
3. The `[[wikilinks]]` between notes become clickable, and the graph view shows how your knowledge connects.

## Compiling manually

If the `claude` CLI wasn't available during ingest, compile any time by running this in the repo folder:

```bash
claude -p "Compile new raw files per CLAUDE.md" --permission-mode acceptEdits
```

## Folder map

```
CLAUDE.md            master librarian rules
school/  content/  business/
  raw/               new Gemini breakdowns land here
  raw/processed/     raw files move here after compiling
  wiki/              the compiled knowledge (this is what gets queried)
  chats/             answers you saved from the chat app
  CLAUDE.md          how that vault's wiki is organized
prompts/             the extraction prompt sent to Gemini
scripts/ingest.py    the Telegram-to-vault pipeline
app/                 the local chat app
```
