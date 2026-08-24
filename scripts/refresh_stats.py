#!/usr/bin/env python3
"""
Refresh the numbers on my own videos.

Your videos keep getting likes after you post them, so the number captured
the day you saved a video goes stale. This script re-checks every video
listed in content/wiki/my-videos.md and writes:

  content/video-stats.json      every check, kept over time (growth history)
  content/wiki/my-video-stats.md  a readable table, best performing first

Run it:  /usr/local/bin/python3 scripts/refresh_stats.py
Or let cron run it weekly (see README).
"""

import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import ingest  # reuse its yt-dlp options (Instagram login, etc.)

# Videos stop moving after about two weeks, so only re-check recent ones.
# Older videos keep whatever numbers they last had (their final numbers).
FRESH_DAYS = 14

LOG_FILE = ROOT / "content" / "wiki" / "my-videos.md"
HISTORY_FILE = ROOT / "content" / "video-stats.json"
TABLE_FILE = ROOT / "content" / "wiki" / "my-video-stats.md"


def videos_from_log():
    """Pull every video's link, title, and post date out of my-videos.md."""
    if not LOG_FILE.exists():
        return []
    text = LOG_FILE.read_text()
    videos = []
    # Entries look like:  ## 2026-08-23 — "the hook" (Instagram, 0:21)
    for block in re.split(r"\n## ", text)[1:]:
        head = block.splitlines()[0]
        m = re.match(r"(\d{4}-\d{2}-\d{2})\s*[—-]\s*(.+)", head)
        if not m:
            continue
        # The log writes "- **Link:** https://..." so skip the bold marks.
        link = re.search(r"Link:\**\s*(https?://\S+)", block)
        if not link:
            continue
        series = re.search(r"Series/day:\**\s*([^\n]+)", block)
        videos.append({
            "posted": m.group(1),
            "title": m.group(2).strip(),
            "url": link.group(1),
            # Keep the series label short, e.g. "Day 0/30".
            "series": series.group(1).strip().split(",")[0] if series else "",
        })
    return videos


def fetch_stats(url):
    """Current numbers for one video. Missing values stay None."""
    ingest._meta_cache.pop(url, None)   # always ask fresh
    meta = ingest.video_meta(url)
    return {k: meta.get(k) for k in
            ("view_count", "like_count", "comment_count", "repost_count")}


def load_history():
    if HISTORY_FILE.exists():
        return json.loads(HISTORY_FILE.read_text())
    return {}


def fmt(n):
    """1234 -> 1,234 ; None -> '-' (platform didn't give us the number)."""
    return "-" if n is None else format(n, ",")


def write_table(history):
    """A readable table, most likes first, so patterns are obvious."""
    rows = []
    for url, entry in history.items():
        checks = entry.get("checks", [])
        if not checks:
            continue
        latest = checks[-1]
        # A video older than FRESH_DAYS is done moving; its numbers are final.
        settled = False
        try:
            from datetime import datetime as _dt
            settled = (_dt.strptime(entry.get("posted", ""), "%Y-%m-%d").date()
                       < date.today() - timedelta(days=FRESH_DAYS))
        except Exception:
            pass
        rows.append({
            "settled": settled,
            "posted": entry.get("posted", ""),
            "title": entry.get("title", url),
            "series": entry.get("series", ""),
            "url": url,
            "checked": latest["date"],
            **{k: latest.get(k) for k in
               ("view_count", "like_count", "comment_count", "repost_count")},
        })
    # Best performing first. Likes is the number every platform gives us.
    rows.sort(key=lambda r: (r.get("like_count") or -1), reverse=True)

    lines = [
        "# My Video Stats",
        "",
        "Numbers on my own posts, best first. Refreshed by "
        "`scripts/refresh_stats.py`, do not edit by hand.",
        "",
        "Instagram does not report views or shares, so those show `-` on IG posts. "
        "TikTok reports all four.",
        "",
        "| Posted | Video | Series | Views | Likes | Comments | Shares | Checked |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        title = r["title"].replace("|", "/")
        if len(title) > 60:
            title = title[:57] + "..."
        lines.append("| %s | [%s](%s) | %s | %s | %s | %s | %s | %s |" % (
            r["posted"], title, r["url"], r["series"] or "-",
            fmt(r.get("view_count")), fmt(r.get("like_count")),
            fmt(r.get("comment_count")), fmt(r.get("repost_count")),
            r["checked"] + (" (final)" if r.get("settled") else "")))

    # Growth since the first check, so it's clear what is still climbing.
    lines += ["", "## Growth since first check", ""]
    for url, entry in history.items():
        checks = entry.get("checks", [])
        if len(checks) < 2:
            continue
        first, last = checks[0], checks[-1]
        gains = []
        for key, label in (("view_count", "views"), ("like_count", "likes"),
                           ("comment_count", "comments"), ("repost_count", "shares")):
            if first.get(key) is not None and last.get(key) is not None:
                delta = last[key] - first[key]
                if delta:
                    gains.append("+%s %s" % (format(delta, ","), label))
        if gains:
            lines.append("- **%s**: %s (since %s)" %
                         (entry.get("title", url), ", ".join(gains), first["date"]))
    if len(lines) and lines[-1] == "":
        lines.append("- Nothing to compare yet, this was the first check.")

    TABLE_FILE.write_text("\n".join(lines) + "\n")


def main():
    videos = videos_from_log()
    if not videos:
        print("No videos found in %s. Send some with #mine first." % LOG_FILE.name)
        return

    history = load_history()
    today = date.today().isoformat()

    cutoff = date.today() - timedelta(days=FRESH_DAYS)
    skipped = 0

    for v in videos:
        url = v["url"]
        entry = history.setdefault(url, {"checks": []})
        entry.update({"posted": v["posted"], "title": v["title"], "series": v["series"]})

        # Skip old videos, but always check a video at least once so it
        # has numbers even if it was added to the log late.
        if entry["checks"]:
            try:
                posted = datetime.strptime(v["posted"], "%Y-%m-%d").date()
            except ValueError:
                posted = None
            if posted and posted < cutoff:
                skipped += 1
                continue

        try:
            stats = fetch_stats(url)
        except Exception as e:
            print("Could not check %s: %s" % (url, str(e)[:100]))
            continue
        # One check per day per video, so re-running does not pile up rows.
        entry["checks"] = [c for c in entry["checks"] if c["date"] != today]
        entry["checks"].append({"date": today, **stats})
        print("%s | likes %s | comments %s | views %s" % (
            v["title"][:40], fmt(stats.get("like_count")),
            fmt(stats.get("comment_count")), fmt(stats.get("view_count"))))

    if skipped:
        print("\nSkipped %d video(s) older than %d days (numbers already settled)."
              % (skipped, FRESH_DAYS))

    HISTORY_FILE.write_text(json.dumps(history, indent=2))
    write_table(history)
    print("Wrote %s" % TABLE_FILE.relative_to(ROOT))


if __name__ == "__main__":
    main()
