#!/usr/bin/env python3
"""
Ingest script for the Second Brain.

What it does, in order:
1. Checks the Telegram bot for new messages (each message = a video link + optional tag).
2. Sends the video to Gemini for a full breakdown (hook, scenes, transcript, analysis).
3. Saves Gemini's markdown to the right vault's raw/ folder.
4. Asks the claude CLI to compile the new raw files into the wiki (if installed).
5. Replies to you on Telegram with what happened.

Run it manually:  python3 scripts/ingest.py
Or let cron run it every 15 minutes (see README).
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import date
from pathlib import Path

import requests
from dotenv import load_dotenv
import os

# ---------- Paths and config ----------

# The repo root is one folder up from this script.
ROOT = Path(__file__).resolve().parent.parent

# Load secrets from .env at the repo root.
load_dotenv(ROOT / ".env")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Where we remember which Telegram messages we already handled,
# so nothing gets processed twice.
STATE_FILE = ROOT / "scripts" / ".ingest_state.json"

# The extraction prompts we send to Gemini along with each video.
# Each vault has its own: content wants hooks/scenes, school wants study
# material, business wants the lesson. Falls back to the content one.
PROMPT_DIR = ROOT / "prompts"


def prompt_for_vault(vault):
    per_vault = PROMPT_DIR / ("gemini-extraction-%s.md" % vault)
    if per_vault.exists():
        return per_vault.read_text()
    return (PROMPT_DIR / "gemini-extraction.md").read_text()

# Valid tags and the default when a message has no tag.
VAULTS = ("school", "content", "business")
DEFAULT_VAULT = "content"

TELEGRAM_API = "https://api.telegram.org/bot{token}/{method}"


# ---------- Small helpers ----------

def load_state():
    """Read the state file, or start fresh if it doesn't exist."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_update_id": 0, "processed_message_ids": []}


def save_state(state):
    """Write the state file. Keep the processed-ids list from growing forever."""
    state["processed_message_ids"] = state["processed_message_ids"][-500:]
    STATE_FILE.write_text(json.dumps(state, indent=2))


def telegram(method, **params):
    """Call one Telegram Bot API method and return the JSON result."""
    url = TELEGRAM_API.format(token=TELEGRAM_BOT_TOKEN, method=method)
    resp = requests.post(url, json=params, timeout=30)
    data = resp.json()
    if not data.get("ok"):
        raise RuntimeError("Telegram API error: %s" % data)
    return data["result"]


def reply(text):
    """Send a message back to you on Telegram. Never crash the run over a reply."""
    try:
        telegram("sendMessage", chat_id=TELEGRAM_CHAT_ID, text=text)
    except Exception as e:
        print("Could not send Telegram reply: %s" % e)


def detect_platform(url):
    """Figure out which platform a link is from."""
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    if "tiktok.com" in url:
        return "tiktok"
    if "instagram.com" in url:
        return "instagram"
    return "unknown"


def slugify(text):
    """Turn any text into a safe lowercase filename piece like 'hormozi-clips'."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:40] or "video"


def ydl_opts_for(url):
    """
    Base yt-dlp options. Instagram requires a logged-in session, so for
    Instagram links we borrow the login cookies from Chrome on this Mac.
    """
    opts = {"quiet": True, "no_warnings": True}
    if "instagram.com" in url:
        # Instagram needs a logged-in session, borrowed from Chrome.
        # Which Chrome profile holds the login is set in .env.
        profile = os.getenv("CHROME_PROFILE", "Default")
        opts["cookiesfrombrowser"] = ("chrome", profile, None, None)
    return opts


def get_creator_slug(url):
    """
    Ask yt-dlp for the video's metadata (no download) to get the creator name.
    Falls back to a slug made from the URL if that fails.
    """
    try:
        from yt_dlp import YoutubeDL
        with YoutubeDL(ydl_opts_for(url)) as ydl:
            info = ydl.extract_info(url, download=False)
        creator = info.get("uploader") or info.get("channel") or info.get("uploader_id")
        if creator:
            return slugify(str(creator))
    except Exception:
        pass
    # Fallback: use the last meaningful chunk of the URL.
    tail = url.rstrip("/").split("/")[-1].split("?")[0]
    return slugify(tail)


def unique_path(folder, filename):
    """If the filename already exists, add -2, -3, ... so nothing is overwritten."""
    path = folder / filename
    counter = 2
    while path.exists():
        path = folder / ("%s-%d.md" % (filename[:-3], counter))
        counter += 1
    return path


# ---------- Gemini ----------

def gemini_client():
    from google import genai
    return genai.Client(api_key=GEMINI_API_KEY)


def response_text_or_reason(response):
    """Gemini's text, or a useful error naming WHY it came back empty."""
    text = response.text
    if text and text.strip():
        return text
    reason = "unknown"
    try:
        c = (response.candidates or [None])[0]
        if c is not None and c.finish_reason:
            reason = str(c.finish_reason)
    except Exception:
        pass
    raise RuntimeError("Gemini returned an empty response (finish reason: %s)" % reason)


def extract_youtube(url, prompt):
    """YouTube: Gemini accepts the URL directly, no download needed."""
    from google.genai import types
    client = gemini_client()
    last_err = None
    for attempt in range(2):  # one retry, empty responses are often flukes
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[
                    types.Part(file_data=types.FileData(file_uri=url)),
                    prompt,
                ],
            )
            return response_text_or_reason(response)
        except RuntimeError as e:
            last_err = e
            time.sleep(10)
    raise last_err


def extract_downloaded(url, prompt):
    """
    TikTok / Instagram: download the video with yt-dlp to a temp folder,
    upload the file to Gemini, and only delete the file AFTER Gemini
    returns output successfully.
    """
    from yt_dlp import YoutubeDL

    tmpdir = Path(tempfile.mkdtemp(prefix="secondbrain_"))
    video_path = None
    uploaded = None
    client = gemini_client()
    try:
        # 1. Download the video.
        opts = ydl_opts_for(url)
        opts["outtmpl"] = str(tmpdir / "%(id)s.%(ext)s")
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = Path(ydl.prepare_filename(info))

        # 2. Upload it to Gemini and wait until Gemini finishes processing it.
        uploaded = client.files.upload(file=str(video_path))
        while uploaded.state.name == "PROCESSING":
            time.sleep(5)
            uploaded = client.files.get(name=uploaded.name)
        if uploaded.state.name != "ACTIVE":
            raise RuntimeError("Gemini could not process the video file (state: %s)" % uploaded.state.name)

        # 3. Ask for the extraction.
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[uploaded, prompt],
        )
        text = response.text
        if not text or not text.strip():
            raise RuntimeError("Gemini returned an empty response")

        # 4. Only now is it safe to delete the local file.
        shutil.rmtree(tmpdir, ignore_errors=True)
        return text
    finally:
        # Clean up the copy stored on Gemini's servers (best effort).
        if uploaded is not None:
            try:
                client.files.delete(name=uploaded.name)
            except Exception:
                pass
        # If anything above failed, the temp folder may still exist.
        # We leave it only when the extraction failed mid-run is not useful,
        # so remove it here too (the video can always be re-downloaded).
        shutil.rmtree(tmpdir, ignore_errors=True)



# ---------- Photos ----------

def download_telegram_file(file_id):
    """Download a file the user sent to the bot. Returns (bytes, filename)."""
    info = telegram("getFile", file_id=file_id)
    file_path = info["file_path"]
    url = "https://api.telegram.org/file/bot%s/%s" % (TELEGRAM_BOT_TOKEN, file_path)
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return resp.content, file_path.split("/")[-1]


def process_photo(file_id, vault, kind, caption=""):
    """
    A photo/screenshot sent to the bot: download it, have Gemini read it
    (text verbatim + what it shows + takeaways), save to the vault's raw/.
    """
    from google.genai import types
    data, filename = download_telegram_file(file_id)
    ext = filename.rsplit(".", 1)[-1].lower()
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
            "webp": "image/webp", "gif": "image/gif"}.get(ext, "image/jpeg")

    purpose = {
        "school": "study material for a college class (concepts, formulas, definitions)",
        "business": "lessons for running a startup (tactics, numbers, strategy)",
        "advice": "advice about making social media content",
        "content": "social media content patterns (hooks, formats, what went viral)",
    }.get(kind, "general knowledge")

    prompt = (PROMPT_DIR / "gemini-photo.md").read_text()
    prompt += "\n\nToday's date is: %s\nThe purpose of saving this image: %s\n" % (
        date.today().isoformat(), purpose)
    if caption:
        prompt += "The sender's caption: %s\n" % caption

    client = gemini_client()
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[types.Part.from_bytes(data=data, mime_type=mime), prompt],
    )
    text = response.text
    if not text or not text.strip():
        raise RuntimeError("Gemini returned an empty response for the photo")

    # Name the note after the caption if there is one, else "photo".
    slug = slugify(re.sub(r"#\w+", "", caption)) if caption else "photo"
    if not slug or slug == "video":
        slug = "photo"
    path = unique_path(ROOT / vault / "raw", "%s-%s.md" % (date.today().isoformat(), slug))
    path.write_text(text)
    return path



def process_document(file_id, filename, vault, kind, caption=""):
    """
    A PDF or text file sent to the bot: Gemini reads it with the vault's
    extraction prompt (same sections as a video, minus the scene stuff).
    """
    from google.genai import types
    data, _ = download_telegram_file(file_id)
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    prompt = prompt_for_vault(kind) + (
        "\n\nNOTE: this is a document, not a video. Treat sections about "
        "spoken words, scenes, or timestamps as 'not applicable' and fill the "
        "rest from the document's content.\nToday's date is: %s\n" % date.today().isoformat())
    if caption:
        prompt += "The sender's caption: %s\n" % caption
    client = gemini_client()
    if ext == "pdf":
        part = types.Part.from_bytes(data=data, mime_type="application/pdf")
    else:
        part = data.decode("utf-8", errors="replace")[:200000]
    response = client.models.generate_content(model=GEMINI_MODEL, contents=[part, prompt])
    text = response.text
    if not text or not text.strip():
        raise RuntimeError("Gemini returned an empty response for the document")
    slug = slugify(filename.rsplit(".", 1)[0]) if filename else "document"
    path = unique_path(ROOT / vault / "raw", "%s-%s.md" % (date.today().isoformat(), slug))
    path.write_text(text)
    return path



def process_voice(file_id, mime, vault_hint=None):
    """
    A voice memo sent to the bot: Gemini transcribes it and decides which
    vault it belongs to (unless a #tag already said). Saves the transcript
    and key points as a note.
    """
    from google.genai import types
    data, _ = download_telegram_file(file_id)
    prompt = (PROMPT_DIR / "gemini-voice.md").read_text()
    prompt += "\nToday's date is: %s\n" % date.today().isoformat()
    client = gemini_client()
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[types.Part.from_bytes(data=data, mime_type=mime or "audio/ogg"), prompt],
    )
    text = response.text
    if not text or not text.strip():
        raise RuntimeError("Gemini returned an empty response for the voice note")

    # A #tag in a caption wins; otherwise use the vault Gemini picked.
    vault = vault_hint
    if not vault:
        m = re.search(r"#\s*VAULT\s*\n+\s*(school|business|content)", text, re.IGNORECASE)
        vault = m.group(1).lower() if m else DEFAULT_VAULT

    # Name the note after the first few transcript words.
    tm = re.search(r"#\s*TRANSCRIPT\s*\n+(.+)", text)
    slug = slugify(" ".join(tm.group(1).split()[:5])) if tm else "voice-note"
    path = unique_path(ROOT / vault / "raw", "%s-%s.md" % (date.today().isoformat(), slug or "voice-note"))
    path.write_text(text)
    return path, vault


# ---------- Compilation ----------

def trigger_compile():
    """
    Ask the claude CLI (headless mode) to compile new raw files into the wikis.
    If the CLI isn't installed, just log it; you can compile manually later.
    """
    # Find the claude CLI. Cron runs with a minimal PATH, so also check
    # the default install location (~/.local/bin).
    claude_bin = shutil.which("claude") or (
        str(Path.home() / ".local" / "bin" / "claude")
        if (Path.home() / ".local" / "bin" / "claude").exists() else None
    )
    if claude_bin is None:
        print("claude CLI not found. Skipping compilation. Run it manually: "
              'claude -p "Compile new raw files per CLAUDE.md"')
        return
    print("Triggering compilation via claude CLI...")
    try:
        subprocess.run(
            [
                claude_bin, "-p",
                "New files were added to one or more vaults' raw/ folders. "
                "Compile them into the wikis following the compile procedure in CLAUDE.md.",
                "--permission-mode", "acceptEdits",
            ],
            cwd=ROOT,
            timeout=1800,  # give it up to 30 minutes
        )
    except Exception as e:
        print("Compilation failed or timed out: %s" % e)


# ---------- Main flow ----------

def parse_message(text):
    """
    Pull the link and the tag out of a Telegram message.
    Returns (url, vault, kind). The kind picks the extraction prompt:
    #advice saves to the content vault but extracts lessons, not hooks.
    #mine also saves to the content vault: it is one of Aiden's OWN videos,
    logged into his posting record instead of studied as someone else's.
    """
    url_match = re.search(r"https?://\S+", text)
    url = url_match.group(0) if url_match else None
    vault, kind = DEFAULT_VAULT, DEFAULT_VAULT
    tag_match = re.search(r"#(school|content|business|advice|mine)", text.lower())
    if tag_match:
        tag = tag_match.group(1)
        vault = "content" if tag in ("advice", "mine") else tag
        kind = tag
    return url, vault, kind



def video_key(url):
    """
    A stable identity for a video so the same one never gets saved twice,
    even via different share links. Uses yt-dlp's extractor + video id;
    falls back to the URL itself.
    """
    try:
        from yt_dlp import YoutubeDL
        opts = ydl_opts_for(url)
        opts["skip_download"] = True
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False, process=False)
        if info and info.get("id"):
            return "%s:%s" % (info.get("extractor_key", "?"), info["id"])
    except Exception:
        pass
    return url.split("?")[0].rstrip("/")


def process_link(url, vault, kind=None):
    """Run the whole pipeline for one link. Returns the saved note's filename."""
    prompt = prompt_for_vault(kind or vault)
    # Give Gemini the facts it can't know on its own, for the frontmatter:
    # the source URL, today's real date, and the creator handle from yt-dlp.
    prompt = prompt + (
        "\n\nThe video URL is: %s\nToday's date is: %s\nThe creator is: %s\n"
        % (url, date.today().isoformat(), get_creator_slug(url))
    )

    platform = detect_platform(url)
    if platform == "unknown":
        raise RuntimeError("Unsupported link (need YouTube, TikTok, or Instagram): %s" % url)

    if platform == "youtube":
        markdown = extract_youtube(url, prompt)
    else:
        markdown = extract_downloaded(url, prompt)

    if not markdown or not markdown.strip():
        raise RuntimeError("Gemini returned an empty response")

    # Save to the vault's raw/ folder as YYYY-MM-DD-{creator-or-slug}.md
    creator = get_creator_slug(url)
    if kind == "mine":
        creator = "mine-%s" % creator   # my own posts are marked in the filename
    filename = "%s-%s.md" % (date.today().isoformat(), creator)
    path = unique_path(ROOT / vault / "raw", filename)
    path.write_text(markdown)
    return path


def main():
    # Only one ingest can run at a time. If another run is already going
    # (cron and a manual run at once), skip. This prevents duplicate notes.
    lock = ROOT / "scripts" / ".ingest_lock"
    if lock.exists():
        # A stale lock (from a crash) older than 2 hours is ignored.
        if time.time() - lock.stat().st_mtime < 7200:
            print("Another ingest is already running. Skipping.")
            return
    lock.write_text(str(os.getpid()))
    import atexit
    atexit.register(lambda: lock.unlink(missing_ok=True))

    # Fail fast if secrets are missing.
    missing = [name for name, val in [
        ("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN),
        ("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID),
        ("GEMINI_API_KEY", GEMINI_API_KEY),
    ] if not val]
    if missing:
        sys.exit("Missing in .env: %s" % ", ".join(missing))

    state = load_state()

    # Ask Telegram for anything newer than what we've already seen.
    updates = telegram("getUpdates", offset=state["last_update_id"] + 1, timeout=0)
    if not updates:
        print("No new messages.")
        return

    saved_any = False
    for update in updates:
        # Always move the offset forward, even for messages we skip,
        # so we never fetch the same update twice.
        state["last_update_id"] = max(state["last_update_id"], update["update_id"])

        message = update.get("message") or update.get("channel_post")
        if not message:
            continue

        # Only accept messages from your own chat.
        if str(message.get("chat", {}).get("id")) != str(TELEGRAM_CHAT_ID):
            continue

        # Skip anything already processed (belt and suspenders).
        msg_id = message["message_id"]
        if msg_id in state["processed_message_ids"]:
            continue

        text = message.get("text") or message.get("caption") or ""
        url, vault, kind = parse_message(text)

        # Photos: Telegram sends several sizes, the last one is the biggest.
        # Also accept images sent as files (uncompressed).
        photo_id = None
        if message.get("photo"):
            photo_id = message["photo"][-1]["file_id"]
        elif (message.get("document") or {}).get("mime_type", "").startswith("image/"):
            photo_id = message["document"]["file_id"]

        # Voice memos: transcribe and auto-route to the right vault.
        voice = message.get("voice") or message.get("audio") or {}
        if voice and not url:
            # Only trust the vault if the user actually typed a tag.
            hint = kind if re.search(r"#(school|content|business|advice)", text.lower()) else None
            if hint == "advice":
                hint = "content"
            try:
                print("Processing voice note")
                path, chosen = process_voice(voice["file_id"], voice.get("mime_type"), vault_hint=hint)
                reply("Saved voice note: %s (%s vault)" % (path.name, chosen))
                saved_any = True
            except Exception as e:
                print("Failed on voice note: %s" % e)
                reply("Failed on voice note\nError: %s" % e)
            state["processed_message_ids"].append(msg_id)
            save_state(state)
            continue

        # Documents: PDFs and text files get read by Gemini too.
        doc = message.get("document") or {}
        doc_mime = doc.get("mime_type", "")
        if doc and not photo_id and not url and (doc_mime == "application/pdf" or doc_mime.startswith("text/")):
            try:
                print("Processing document %s -> %s vault" % (doc.get("file_name"), vault))
                path = process_document(doc["file_id"], doc.get("file_name", "document"), vault, kind, caption=text)
                reply("Saved document: %s (%s vault)" % (path.name, vault))
                saved_any = True
            except Exception as e:
                print("Failed on document: %s" % e)
                reply("Failed on document\nError: %s" % e)
            state["processed_message_ids"].append(msg_id)
            save_state(state)
            continue

        if photo_id and not url:
            try:
                print("Processing photo -> %s vault" % vault)
                path = process_photo(photo_id, vault, kind, caption=text)
                reply("Saved photo: %s (%s vault)" % (path.name, vault))
                saved_any = True
            except Exception as e:
                print("Failed on photo: %s" % e)
                reply("Failed on photo\nError: %s" % e)
            state["processed_message_ids"].append(msg_id)
            save_state(state)
            continue

        if not url:
            reply("No link, photo, or file found in that message. Send a link, a photo, or a PDF, "
                  "optionally with #school, #content, #business, #advice, or #mine.")
            state["processed_message_ids"].append(msg_id)
            continue

        # One bad link must never kill the whole run.
        try:
            key = video_key(url)
            seen = state.setdefault("processed_videos", {})
            if key in seen:
                reply("Already saved that one as %s. Skipping." % seen[key])
                state["processed_message_ids"].append(msg_id)
                save_state(state)
                continue
            print("Processing %s -> %s vault" % (url, vault))
            path = process_link(url, vault, kind)
            seen[key] = path.name
            if len(seen) > 500:
                for k in list(seen)[:-500]:
                    del seen[k]
            reply("Saved: %s (%s vault)" % (path.name, vault))
            saved_any = True
        except Exception as e:
            print("Failed on %s: %s" % (url, e))
            reply("Failed on %s\nError: %s" % (url, e))

        state["processed_message_ids"].append(msg_id)
        # Save state after every message so a crash never causes reprocessing.
        save_state(state)

    save_state(state)

    # If we saved anything new, compile it into the wikis.
    if saved_any:
        trigger_compile()


if __name__ == "__main__":
    main()
