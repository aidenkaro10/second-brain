# Content Vault — Wiki Rules

This vault stores social media knowledge: hooks, formats, CTAs, platform tactics, and breakdowns of viral videos.

## Organization

Organize by **pattern type, not by creator**. Wiki files live in `wiki/` and group patterns:

- `hooks/` — one file per hook type: `curiosity-gap.md`, `contrarian.md`, `pov.md`, `negativity.md`, `question.md`, and new types as they show up in sources.
- `formats.md` — video formats (talking head, screen recording, skit, listicle, etc). Split into a `formats/` folder if it grows large.
- `ctas.md` — call-to-action patterns.
- `platform-tactics.md` — platform-specific tactics (TikTok, Instagram, YouTube). Split per platform if it grows large.
- `index.md` — every wiki file with a one-line description.

## Pattern file structure

Each pattern file must keep:

1. **Verbatim examples** from sources. Quote the exact hook line or script text, never a paraphrase.
2. A short **"why it works"** breakdown for each example or for the pattern overall.
3. **Performance numbers** (views, likes, retention) whenever the source includes them.
4. `[[wikilinks]]` to related patterns.
5. `## Sources` at the bottom listing the raw filenames the content came from.

When a new breakdown arrives in `raw/`, file each of its findings under the matching pattern. One video usually feeds several pattern files.

## Advice videos (#advice)

Some raw files are ADVICE about making content, not viral examples. You can tell by their sections (CORE LESSON, FRAMEWORKS AND STEPS) instead of HOOK / SCENE-BY-SCENE. Compile these into `strategy/` with one file per topic (e.g. `strategy/hooks-advice.md`, `strategy/posting-cadence.md`, `strategy/algorithm.md`). Keep the frameworks complete, quotes verbatim, and numbers when given. Never mix advice into the pattern files, patterns hold examples, strategy holds instructions. Link them where related (a hooks advice file links to the hook pattern files it talks about).
