#!/usr/bin/env python3
"""
Second Brain chat app.

A small Flask server with one page. You pick a vault, ask a question,
and the server sends your question plus the relevant wiki files to Claude.
Answers can be saved as markdown notes in the vault's chats/ folder.

Run it:  python3 app/server.py   then open http://localhost:5001
"""

import base64
import os
import re
import threading
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

# The repo root is one folder up from this file.
ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5")

VAULTS = ("school", "content", "business")

# Keep the context we send to Claude under roughly this many characters
# so we never blow past the model's input limit. Roughly 4 chars per token,
# so 320k chars is about 80k tokens: plenty of room, still affordable.
MAX_CONTEXT_CHARS = 320_000

# No single file may eat more than this much of the budget. Without this,
# one huge file (like a whole book's notes) starves every other file and
# the wiki looks half-missing to the model.
MAX_CHARS_PER_FILE = 40_000

app = Flask(__name__)


# ---------- Context building ----------

def read_if_exists(path):
    """Return a file's text, or empty string if it doesn't exist."""
    try:
        return path.read_text()
    except FileNotFoundError:
        return ""


def score_file(path, query_words):
    """
    Score how relevant a wiki file is to the question.
    Simple keyword matching: count how often the question's words appear
    in the filename and the file's text. Filename hits count extra.
    """
    text = read_if_exists(path).lower()
    name = path.stem.lower().replace("-", " ")
    score = 0
    for word in query_words:
        score += name.count(word) * 5   # filename match is a strong signal
        score += text.count(word)
    return score


def matched_wiki_files(vault, query):
    """Return this vault's wiki files sorted by relevance to the question."""
    wiki = ROOT / vault / "wiki"
    if not wiki.exists():
        return []
    # Words of 3+ letters from the question, lowercased.
    query_words = [w for w in re.findall(r"[a-z0-9]{3,}", query.lower())]
    files = [p for p in wiki.rglob("*.md") if p.name not in ("index.md", "overview.md")]
    scored = [(score_file(p, query_words), p) for p in files]
    # Include ALL files, best matches first. The vaults are small enough to
    # send everything; the context cap in build_context trims if needed.
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return scored


def build_context(vault, query):
    """
    Build the context block for one vault: its CLAUDE.md and index.md always,
    plus the wiki files that match the question.
    Returns (context_text, total_match_score).
    """
    parts = []
    base = ROOT / vault
    # These three always go in: the rules, the map, and his profile.
    parts.append("### %s/CLAUDE.md\n\n%s" % (vault, read_if_exists(base / "CLAUDE.md")))
    parts.append("### %s/wiki/index.md\n\n%s" % (vault, read_if_exists(base / "wiki" / "index.md")))
    parts.append("### %s/wiki/overview.md\n\n%s" % (vault, read_if_exists(base / "wiki" / "overview.md")))

    used = sum(len(p) for p in parts)
    total_score = 0

    # Every wiki file, best match first, until the budget runs out.
    # A single oversized file gets trimmed instead of crowding out the rest.
    for score, path in matched_wiki_files(vault, query):
        text = read_if_exists(path)
        if len(text) > MAX_CHARS_PER_FILE:
            text = (text[:MAX_CHARS_PER_FILE]
                    + "\n\n[... file trimmed here to leave room for other notes. "
                      "Say so if the answer needs the rest of this file.]")
        rel = path.relative_to(ROOT)
        block = "### %s\n\n%s" % (rel, text)
        if used + len(block) > MAX_CONTEXT_CHARS:
            continue   # too big for what's left; smaller files may still fit
        parts.append(block)
        used += len(block)
        total_score += score

    return "\n\n---\n\n".join(parts), total_score


# ---------- Living overviews ----------

# One lock per vault so two updates never write the same file at once.
_overview_locks = {v: threading.Lock() for v in VAULTS}


def update_overview_from_chat(vault, question, answer):
    """
    Runs in the background after each chat answer. If the exchange reveals
    something new about Aiden's projects or goals in this area, fold it
    into the vault's overview.md. Silent no-op otherwise.
    """
    try:
        import anthropic
        path = ROOT / vault / "wiki" / "overview.md"
        current = read_if_exists(path)
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        prompt = (
            "Below is Aiden's personal %s profile file, followed by one exchange "
            "from his chat app. If HIS message (not the assistant's) reveals "
            "something new and lasting about his own plans, niche, services, "
            "schedule, goals, or state, merge it into the matching section and "
            "output the complete updated file. Replace 'not saved yet' "
            "placeholders when real info arrives. If he shares a full plan "
            "(like a 30 day content plan), save the whole thing. Keep the file "
            "clean and current; outdated facts get replaced, not stacked. "
            "If nothing new or lasting was revealed, output exactly: UNCHANGED\n\n"
            "==== CURRENT PROFILE ====\n%s\n\n"
            "==== EXCHANGE ====\nAiden: %s\nAssistant: %s"
            % (vault, current, question, answer)
        )
        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(b.text for b in response.content if b.type == "text").strip()
        if text and text != "UNCHANGED" and text.startswith("#"):
            with _overview_locks[vault]:
                path.write_text(text + "\n")
    except Exception as e:
        print("Overview update skipped: %s" % e)



# ---------- Attachments ----------

IMAGE_TYPES = ("image/jpeg", "image/png", "image/gif", "image/webp")


def attachment_blocks(attachments):
    """
    Turn uploaded files into Anthropic message content blocks.
    Images and PDFs go in natively; text-like files are pasted as text.
    """
    blocks = []
    for a in attachments or []:
        mime = a.get("mime", "")
        data = a.get("data", "")
        name = a.get("name", "file")
        if mime in IMAGE_TYPES:
            blocks.append({"type": "image",
                           "source": {"type": "base64", "media_type": mime, "data": data}})
        elif mime == "application/pdf":
            blocks.append({"type": "document",
                           "source": {"type": "base64", "media_type": "application/pdf", "data": data},
                           "title": name})
        else:
            # Anything else: treat as text (md, txt, csv, code).
            try:
                text = base64.b64decode(data).decode("utf-8", errors="replace")
            except Exception:
                text = "(could not read %s)" % name
            blocks.append({"type": "text", "text": "Attached file %s:\n\n%s" % (name, text[:60000])})
    return blocks


def save_attachment_to_vault(vault, a):
    """Drop an uploaded file into the vault's raw/ so the compiler picks it up."""
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", a.get("name", "file")).strip("-") or "file"
    folder = ROOT / vault / "raw"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / ("%s-%s" % (date.today().isoformat(), name))
    counter = 2
    while path.exists():
        stem, dot, ext = name.rpartition(".")
        path = folder / ("%s-%s-%d%s%s" % (date.today().isoformat(), stem or ext, counter, dot, ext if stem else ""))
        counter += 1
    path.write_bytes(base64.b64decode(a.get("data", "")))
    return path


# ---------- Routes ----------

@app.route("/")
def home():
    return send_from_directory(Path(__file__).resolve().parent, "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    vault = data.get("vault", "content")
    messages = data.get("messages", [])
    if not messages:
        return jsonify({"error": "No messages"}), 400

    question = messages[-1].get("content", "")
    attachments = data.get("attachments") or []
    add_to_vault = bool(data.get("add_to_vault"))

    # Build context from the selected vault, or all three for "all".
    if vault == "all":
        blocks = []
        scores = {}
        for v in VAULTS:
            ctx, score = build_context(v, question)
            blocks.append("## VAULT: %s\n\n%s" % (v, ctx))
            scores[v] = score
        context = "\n\n====\n\n".join(blocks)
        # The vault with the most matching wiki content is where a saved
        # note would belong. Ties and no-matches fall back to business.
        suggested_vault = max(scores, key=lambda v: scores[v]) if any(scores.values()) else "business"
    else:
        if vault not in VAULTS:
            return jsonify({"error": "Unknown vault"}), 400
        context, _ = build_context(vault, question)
        suggested_vault = vault

    # Safety net only; build_context already keeps each vault in budget.\n    context = context[:MAX_CONTEXT_CHARS * 3]

    system_prompt = (
        read_if_exists(ROOT / "CLAUDE.md") + "\n\n"
        "You are the librarian for a personal knowledge base called Second Brain. "
        "Answer using ONLY the wiki content provided below. Do not use general knowledge. "
        "If the wiki does not contain the answer, say so and suggest what kind of source to add. "
        "When sources disagree, present the disagreement explicitly. "
        "Style: short, simple, concise answers with no filler. Use numbered steps "
        "for how-to explanations, one action per step. Write like a real person "
        "talking, no corporate tone, no em dashes.\n\n"
        "==== WIKI CONTEXT ====\n\n" + context
    )

    # Earlier turns are plain text. The newest turn carries any attachments
    # as native image/PDF blocks so Claude can actually see them.
    api_messages = [{"role": m["role"], "content": m["content"]} for m in messages[:-1]]
    last_blocks = attachment_blocks(attachments)
    last_blocks.append({"type": "text", "text": question or "(see attached)"})
    api_messages.append({"role": "user", "content": last_blocks})

    saved_files = []
    if add_to_vault and attachments:
        target = suggested_vault if vault == "all" else vault
        for a in attachments:
            try:
                saved_files.append(str(save_attachment_to_vault(target, a).relative_to(ROOT)))
            except Exception as e:
                print("Could not save attachment: %s" % e)

    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    try:
        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=2000,
            system=system_prompt,
            messages=api_messages,
        )
    except anthropic.APIError as e:
        return jsonify({"error": "Anthropic API error: %s" % e}), 502

    answer = "".join(block.text for block in response.content if block.type == "text")

    # Quietly update the vault's living overview in the background so the
    # chat reply is never slowed down.
    threading.Thread(
        target=update_overview_from_chat,
        args=(suggested_vault, question, answer),
        daemon=True,
    ).start()

    return jsonify({"answer": answer, "suggested_vault": suggested_vault,
                    "saved_files": saved_files})


@app.route("/api/save", methods=["POST"])
def save():
    data = request.get_json(force=True)
    vault = data.get("vault", "business")
    question = data.get("question", "").strip()
    answer = data.get("answer", "").strip()
    if vault not in VAULTS:
        vault = "business"
    if not question or not answer:
        return jsonify({"error": "Nothing to save"}), 400

    # Filename: YYYY-MM-DD-{short-slug}.md from the first few question words.
    slug_words = re.findall(r"[a-z0-9]+", question.lower())[:5]
    slug = "-".join(slug_words) or "note"
    today = date.today().isoformat()
    folder = ROOT / vault / "chats"
    folder.mkdir(parents=True, exist_ok=True)

    path = folder / ("%s-%s.md" % (today, slug))
    counter = 2
    while path.exists():
        path = folder / ("%s-%s-%d.md" % (today, slug, counter))
        counter += 1

    note = (
        "---\n"
        "date: %s\n"
        "vault: %s\n"
        "---\n\n"
        "## Question\n\n%s\n\n"
        "## Answer\n\n%s\n" % (today, vault, question, answer)
    )
    path.write_text(note)
    return jsonify({"saved": str(path.relative_to(ROOT))})


if __name__ == "__main__":
    if not ANTHROPIC_API_KEY:
        raise SystemExit("ANTHROPIC_API_KEY is missing from .env")
    # 0.0.0.0 means other devices on your WiFi (like your phone) can reach it.
    app.run(host="0.0.0.0", port=5001, debug=False)
