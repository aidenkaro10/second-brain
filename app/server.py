#!/usr/bin/env python3
"""
Second Brain chat app.

A small Flask server with one page. You pick a vault, ask a question,
and the server sends your question plus the relevant wiki files to Claude.
Answers can be saved as markdown notes in the vault's chats/ folder.

Run it:  python3 app/server.py   then open http://localhost:5001
"""

import os
import re
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
# so we never blow past the model's input limit.
MAX_CONTEXT_CHARS = 100_000

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
    files = [p for p in wiki.rglob("*.md") if p.name != "index.md"]
    scored = [(score_file(p, query_words), p) for p in files]
    scored = [(s, p) for s, p in scored if s > 0]
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
    parts.append("### %s/CLAUDE.md\n\n%s" % (vault, read_if_exists(base / "CLAUDE.md")))
    parts.append("### %s/wiki/index.md\n\n%s" % (vault, read_if_exists(base / "wiki" / "index.md")))

    total_score = 0
    for score, path in matched_wiki_files(vault, query)[:8]:
        total_score += score
        rel = path.relative_to(ROOT)
        parts.append("### %s\n\n%s" % (rel, read_if_exists(path)))

    return "\n\n---\n\n".join(parts), total_score


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

    context = context[:MAX_CONTEXT_CHARS]

    system_prompt = (
        "You are the librarian for a personal knowledge base called Second Brain. "
        "Answer using ONLY the wiki content provided below. Do not use general knowledge. "
        "If the wiki does not contain the answer, say so and suggest what kind of source to add. "
        "When sources disagree, present the disagreement explicitly.\n\n"
        "==== WIKI CONTEXT ====\n\n" + context
    )

    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    try:
        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": m["role"], "content": m["content"]} for m in messages],
        )
    except anthropic.APIError as e:
        return jsonify({"error": "Anthropic API error: %s" % e}), 502

    answer = "".join(block.text for block in response.content if block.type == "text")
    return jsonify({"answer": answer, "suggested_vault": suggested_vault})


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
    app.run(host="127.0.0.1", port=5001, debug=False)
