You are analyzing a short-form video. Produce a markdown document with EXACTLY these five sections, in this order.

# FRONTMATTER

A fenced yaml block with these keys:
- source_url: the video URL (provided below)
- platform: youtube, tiktok, or instagram
- creator: the creator's handle or channel name, if identifiable
- date_processed: today's date, YYYY-MM-DD

# HOOK

The first 3 seconds, verbatim:
- Spoken words: exactly what is said, word for word.
- On-screen text: exactly what text appears on screen.

# SCENE-BY-SCENE

A timestamped breakdown of the whole video. For each scene or cut:
- Timestamp range (e.g. 0:00-0:03)
- What is shown (visuals, camera angle, b-roll)
- Cuts and transitions
- Text overlays, verbatim
- Pacing notes (fast cuts, holds, zooms)

# FULL TRANSCRIPT

The complete spoken audio, verbatim.

# WHY IT WORKS

Your analysis of the hook mechanism and retention devices. 5 bullets maximum.

## Constraints

- The transcript must be VERBATIM. Do not summarize, clean up, or paraphrase anything in the FULL TRANSCRIPT section.
- Mark unclear audio as [inaudible].
- Output markdown only. No preamble, no commentary before or after the document.

Long videos: if the video is longer than 15 minutes, do NOT transcribe it verbatim end to end. Instead give a section-by-section breakdown (with timestamps) where each section gets a tight summary plus the most important lines quoted verbatim. Keep total output well under the length limit so nothing gets cut off.
