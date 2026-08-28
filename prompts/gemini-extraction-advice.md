You are watching a video that gives ADVICE about making social media content (growth tactics, hooks, algorithms, posting strategy). Extract the advice. Output markdown with EXACTLY these sections, in this order:

# FRONTMATTER

```yaml
source_url: (the video URL)
platform: (youtube / tiktok / instagram)
creator: (channel or creator name)
date_processed: (today's date)
topic: (what the advice is about, a few words, e.g. "hooks", "posting cadence", "algorithm")
```

# CORE LESSON

The main advice of the video in 2-4 sentences, plain language.

# FULL TRANSCRIPT

Every word spoken in the video, verbatim, start to finish. Do not summarize, do not paraphrase, do not clean it up. Keep filler words exactly as said. Mark unclear audio as [inaudible]. If nobody speaks, write "No speech."

# FRAMEWORKS AND STEPS

Every framework, checklist, step-by-step process, or rule the video teaches. Numbered or bulleted, complete, in the video's own structure. If none, write "None in this video."

# KEY QUOTES

The most quotable lines, verbatim, in quotation marks. Only lines actually spoken or shown on screen.

# NUMBERS AND PROOF

Every metric, view count, percentage, timeframe, or example result the video cites as evidence. If none, write "None in this video."

# HOW TO APPLY

3 bullets max: how a short-form creator should act on this advice. Base it only on what the video argues.

Constraints:
- Never invent claims the video does not make. Quotes must be verbatim.
- Mark unclear audio as [inaudible].
- Output markdown only, no preamble, no closing remarks.

Long videos: always transcribe every word, no matter the length. For videos longer than 20 minutes, split the transcript into timestamped chunks (## 0:00-5:00, ## 5:00-10:00, and so on) so it stays organised, but never drop or summarise speech. Keep the other analysis sections brief on long videos so the transcript is what gets the room.
