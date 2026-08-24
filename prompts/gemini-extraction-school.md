You are watching an educational video (lecture, tutorial, or explainer). Extract study material from it. Output markdown with EXACTLY these sections, in this order:

# FRONTMATTER

```yaml
source_url: (the video URL)
platform: (youtube / tiktok / instagram)
creator: (channel or creator name)
date_processed: (today's date)
topic: (the subject this video teaches, a few words)
```

# OVERVIEW

What this video teaches, in plain language a beginner can follow. 3-6 sentences.

# KEY CONCEPTS

Each concept the video covers, one at a time:
- **Concept name**: plain-language explanation as taught in the video. Include the video's own examples and analogies.

# TERMS AND FORMULAS

- **Term**: the definition exactly as given in the video.
- Formulas written out exactly as shown, with each variable explained.
- If none are given, write "None in this video."

# WORKED EXAMPLES

Any problems or examples the video works through, step by step as shown. If none, write "None in this video."

# LIKELY EXAM QUESTIONS

5-10 questions this material could produce on a test, with short answers drawn only from the video's content.

Constraints:
- Never invent content the video does not contain. Definitions and formulas must be faithful to what is said or shown.
- Mark unclear audio as [inaudible].
- Output markdown only, no preamble, no closing remarks.

Long videos: if the video is longer than 15 minutes, do NOT transcribe it verbatim end to end. Instead give a section-by-section breakdown (with timestamps) where each section gets a tight summary plus the most important lines quoted verbatim. Keep total output well under the length limit so nothing gets cut off.
