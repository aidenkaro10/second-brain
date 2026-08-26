# FRONTMATTER

```yaml
source_url: https://youtu.be/XeTAlZiIWHE
platform: youtube
creator: jason-cooperson
date_processed: 2026-08-25
topic: Claude AI Video Editing System
```

# CORE LESSON

Automate video editing end-to-end by building a structured, step-by-step pipeline using Claude Code, Hyperframes, WhisperX, and FFmpeg. Instead of manually editing in software like Premiere, creators can input raw footage and let AI execute transcript-based rough cuts, generate on-beat motion graphics, burn in captions, mix audio, and export. High-quality output requires an iterative second pass with targeted natural language prompts to refine individual graphics rather than relying on a single prompt.

# FRAMEWORKS AND STEPS

### The 7-Step Claude Video Editing Pipeline

1. **Intake (07:31)**
   - Record raw video footage.
   - Copy the file path of the raw clip into Claude to initialize the project workspace.

2. **Rough Cut (07:31 - 10:20)**
   - Use **WhisperX** to transcribe raw footage with word-level timestamps.
   - Claude analyzes the transcript to remove dead space, silences, filler words, and bad takes while polishing audio.

3. **Graphics - First Pass (10:20 - 11:42)**
   - Use the **Hyperframes** rendering engine to generate on-beat motion graphics, full-screen takeovers, or split-screen layouts based on video content.

4. **Second Pass / Refinement (11:42 - 15:43)**
   - Review the first draft and issue targeted natural language prompts per graphic segment (e.g., adjust position, change colors to brand hex codes, insert PNG logos/mascots, tweak layouts).
   - The system re-renders only modified sections rather than the full video to save time.

5. **Captions (15:43 - 17:37)**
   - Apply on-beat burn-in captions for short-form formats.
   - Use preset styling (e.g., Coolvetica font, black background text box, animated word pop-ins aligned to WhisperX timestamps).

6. **Background Music (17:37 - 18:50)**
   - Provide a file path for background music.
   - Specify decibel levels relative to the voice track (e.g., -23 dB) so music remains subtle.

7. **Export (18:50 - 19:23)**
   - Export the completed MP4 video directly to the outputs/downloads directory while keeping project files intact for future edits.

---

### Format Variants

- **Short - Explainer:** Motion graphics on top half, speaker face on bottom half, captions in middle.
- **Short - TikTok / Raw:** Text hook overlay at top, tight rough cut, on-screen burned-in captions.
- **Long-Form - YouTube:** Full-frame video with motion graphics overlays, dynamic visual takeovers, background music, optional captions.

# KEY QUOTES

- "This video that you're watching right now was edited by Claude entirely from end to end." (00:01)
- "I built the most cracked, dialed-in Claude video editing system on all of YouTube." (00:06)
- "All I have to do is drop in raw footage and Claude does the rest." (00:11)
- "This step really makes the whole difference between AI slop versus like an actually good edited video." (04:04)
- "Instead of rendering the entire video all over again... all it needs to render is just that first part because that's the only part we're making changes to." (12:51)
- "To edit a video like this normally, for me it takes probably like four or five hours... I think it's a huge, huge time save." (14:52)

# NUMBERS AND PROOF

- **Footage Trimming:** Raw 4-minute 10-second clip cut down to 47 seconds in the rough cut stage.
- **Rough Cut Render Time:** ~10 to 15 minutes.
- **Graphics First Pass Render Time:** 22 minutes.
- **Graphics Second Pass Partial Render Time:** ~3 to 3.5 minutes per targeted modification pass.
- **Audio Mixing Level:** Settled at -23 dB for background music after testing -18 dB.
- **Total Editing Time in Claude:** ~2 hours (versus an estimated 4–5 hours for manual editing, or days for beginner editors).
- **System Development Time:** 2 full weeks of continuous development.

# HOW TO APPLY

- Set up a local project folder configured with Claude Code, Hyperframes, WhisperX, and FFmpeg dependencies.
- Process video edits sequentially—lock in the transcript-based rough cut before generating graphics or mixing background audio.
- Refine visuals iteratively by prompting Claude to edit individual frame segments rather than re-rendering full video sequences.