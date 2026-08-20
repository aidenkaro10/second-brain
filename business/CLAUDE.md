# Business Vault — Wiki Rules

This vault stores startup knowledge for Rekko: marketing, sales, ops, product, finance, and decisions.

## Organization

Organize by **function**:

```
wiki/
  index.md
  marketing.md
  sales.md
  ops.md
  product.md
  finance.md
  decisions-log.md
```

Split a function file into a folder (e.g. `marketing/`) when it grows too large for one file.

## File structure

Each function file keeps the knowledge for that area: tactics, playbooks, numbers, lessons learned. Use `[[wikilinks]]` between related notes and end every file with `## Sources` listing the raw filenames the content came from.

## Video breakdowns tagged #business

Raw files here are often TikTok/video breakdowns. Compile the LESSON, not the video: pull out the business or mindset takeaway (with verbatim quotes) and file it under the matching function file. Mindset and philosophy lessons go in `mindset.md`. The video's hook mechanics may also be cross-filed into the content vault's pattern files. Never stall waiting for input; pick the best-fitting file and note the choice.

## Decisions log

`decisions-log.md` records decisions as they happen. Each entry:

```
## YYYY-MM-DD — <decision>
- Reasoning: why we chose this
- Alternatives considered: what we didn't do
- Source: raw filename or "conversation"
```

Never rewrite past entries. If a decision is reversed, add a new entry that links back to the old one.
