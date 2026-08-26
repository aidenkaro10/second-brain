# AI Video Editing Pipeline

## Core lesson

Automate video editing end to end with Claude Code plus three tools: WhisperX (transcription/captions), Hyperframes (motion graphics rendering), and FFmpeg (audio/export). Drop in raw footage and Claude runs a transcript-based rough cut, generates on-beat motion graphics, burns in captions, mixes background audio, and exports — no manual cutting in Premiere. Getting a clean result needs a second, targeted refinement pass (natural-language notes on individual graphic segments) instead of one big prompt.

> "This video that you're watching right now was edited by Claude entirely from end to end."

> "I built the most cracked, dialed-in Claude video editing system on all of YouTube."

> "All I have to do is drop in raw footage and Claude does the rest."

> "Just follow along with this tutorial and by the end, you will have Claude editing your videos while you sleep."

> "This step really makes the whole difference between AI slop versus like an actually good edited video."

> "Instead of rendering the entire video all over again... all it needs to render is just that first part because that's the only part we're making changes to."

> "To edit a video like this normally, for me it takes probably like four or five hours... I think it's a huge, huge time save."

## Framework: The 7-step pipeline

1. **Intake (07:31)** — record raw footage, copy the file path into Claude to start the project workspace.
2. **Rough cut (07:31–10:20)** — WhisperX transcribes with word-level timestamps; Claude removes dead space, silences, filler words, and bad takes, and polishes the audio.
3. **Graphics, first pass (10:20–11:42)** — Hyperframes generates on-beat motion graphics, full-screen takeovers, or split-screen layouts based on the content.
4. **Graphics, second pass / refinement (11:42–15:43)** — review the draft and give targeted natural-language notes per graphic segment (adjust position, change colors to brand hex codes, insert PNG logos/mascots, tweak layout). Only the modified section re-renders, not the whole video.
5. **Captions (15:43–17:37)** — on-beat burn-in captions for short-form video, preset styling (Coolvetica font, black background text box, animated word pop-ins synced to WhisperX timestamps).
6. **Background music (17:37–18:50)** — provide a music file path, set its decibel level relative to the voice track (e.g. -23 dB) so it stays subtle.
7. **Export (18:50–19:23)** — export the finished MP4 to the outputs/downloads directory, keep project files intact for future edits.

Simplified version of the same pipeline (from the shorter Instagram breakdown): intake → rough cut → graphics → captions → music → export, with the option to export straight to `final.mp4` or hand the rough cut off to Premiere for manual polish instead of finishing entirely inside the pipeline.

> "Just follow along with this tutorial and by the end, you will have Claude editing your videos while you sleep."

## Format variants

- **Short – Explainer:** motion graphics on the top half, speaker face on the bottom half, captions in the middle.
- **Short – TikTok/Raw:** text hook overlay at the top, tight rough cut, burned-in captions.
- **Long-form YouTube:** full-frame video, motion graphic overlays, dynamic visual takeovers, background music, optional captions.

## Numbers and proof

- Raw 4:10 clip trimmed down to 47 seconds in the rough cut.
- Rough cut render time: ~10–15 minutes.
- Graphics first-pass render time: 22 minutes.
- Graphics second-pass (targeted re-render): ~3–3.5 minutes per pass.
- Audio mix settled at -23 dB for background music, after testing -18 dB.
- Total editing time in Claude: ~2 hours, vs. an estimated 4–5 hours manual (or days for a beginner editor).
- System took 2 full weeks of continuous development to build.
- 100% of the video edited by Claude, zero human edits (per the Instagram version).
- 94% of motion graphics auto-built on beat (per the Instagram version).

## How to apply

- Set up a local project folder with Claude Code, Hyperframes, WhisperX, and FFmpeg installed.
- Work in order — lock in the transcript-based rough cut before touching graphics or background audio.
- Refine visuals with targeted prompts per segment instead of re-prompting the whole video; it only re-renders what changed, saving a lot of time.
- If full automation isn't wanted yet, export the automated rough cut into Premiere for manual polish instead of finishing the whole pipeline inside Claude.

## Related

- [[formats]] — the short-form and long-form structures this pipeline is built to produce.
- [[platform-tactics]] — burned-in caption styling ties to short-form retention tactics.

## Sources

- 2026-08-25-jason-cooperson.md
- 2026-08-25-jason-cooperson-2.md
