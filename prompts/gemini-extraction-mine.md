You are analyzing a video that the creator MADE AND POSTED THEMSELVES. This goes into their personal archive of their own work, so they can see what they did, spot their patterns, and improve. Be exhaustive and be honest. Output markdown with EXACTLY these sections, in this order:

# FRONTMATTER

```yaml
source_url: (the video URL)
platform: (youtube / tiktok / instagram)
creator: (the account name)
date_posted: (the real upload date, given to you below)
length: (total runtime, mm:ss)
series: (if the video is part of a numbered series, e.g. "Day 3/30"; otherwise "one-off")
topic: (a few words on what it is about)
```

# HOOK

The first 3 seconds, exactly:
- **Spoken:** verbatim words
- **On-screen text:** every word visible, in the order it appears
- **Visual:** what is on screen (shot type, location, what the viewer sees first)

# FULL TRANSCRIPT

Every word spoken, verbatim, start to finish. Do not summarize, do not clean up. Keep filler words ("um", "like", "you know") exactly as said, because the creator wants to hear their real speech patterns. Mark unclear audio as [inaudible].

# SHOT BY SHOT

Every shot or cut, with timestamps. For each one:
- **Visual:** shot type (wide/medium/close-up/selfie), location, framing, camera movement (static, walking, pan, handheld)
- **On-screen text:** any text or captions in that shot, verbatim
- **Graphics:** logos, images, screenshots, diagrams, memes, or b-roll that appear
- **Audio:** music, sound effects, or silence, if noticeable

# EDITING AND PRODUCTION

- **Cut rate:** roughly how many cuts, and the average shot length
- **Caption style:** font look, placement, animation (word-by-word, karaoke highlight, static block), auto-captions or custom
- **Text overlays:** persistent overlays (like a day counter) vs. moment-specific text
- **Graphics style:** how images/logos enter and leave, size, placement
- **Transitions:** hard cuts, whip pans, match cuts, zooms, jump cuts
- **Audio:** background music (genre/energy), sound effects, voiceover vs. in-camera audio, audio quality issues
- **Look:** lighting, color, resolution issues, vertical framing, anything visually rough

# DELIVERY

How the creator performs on camera: speech pace, energy level, eye contact, confidence, filler-word habits, whether the tone matches the content. Be specific and honest, this is a mirror.

# TECHNIQUES USED

Name every technique plainly, so it can be matched against known patterns:
- Hook type (question / contrarian / curiosity gap / POV / negativity / motivational / other)
- Format (talking head, listicle, tutorial, challenge log, b-roll voiceover, skit, other)
- Retention devices (day counter, open loop, pattern interrupts, text pacing, speed prompts)
- CTA type and exact wording, or "no CTA"

# STRUCTURE

The beats of the video with timestamps: hook, setup, body sections, payoff, CTA. Name what each beat is doing.

# HONEST CRITIQUE

5-8 bullets. Direct and specific, no encouragement filler. Cover:
- Does the hook earn the next 3 seconds? Name what would make it stronger.
- Does the middle hold, or is there a dead stretch? Give the timestamp.
- Is there a real payoff, or just stated intent?
- Does the CTA fit the video?
- Anything technically weak: audio, lighting, caption timing, pacing.
- The single highest-leverage fix for the next video.

Constraints:
- Never invent anything the video does not contain. Quotes must be verbatim.
- The critique must be genuinely useful, not flattering. If something is weak, say exactly why and what to do instead.
- Output markdown only, no preamble, no closing remarks.

Long videos: if the video is longer than 15 minutes, keep every section above, but replace the word-for-word transcript with a timestamped section-by-section breakdown that quotes the most important lines verbatim.
