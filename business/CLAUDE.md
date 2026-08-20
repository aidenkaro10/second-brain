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

## Decisions log

`decisions-log.md` records decisions as they happen. Each entry:

```
## YYYY-MM-DD — <decision>
- Reasoning: why we chose this
- Alternatives considered: what we didn't do
- Source: raw filename or "conversation"
```

Never rewrite past entries. If a decision is reversed, add a new entry that links back to the old one.
