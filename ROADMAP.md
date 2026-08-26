# Roadmap

Ideas agreed on but intentionally saved for later.

## Move ingest to the cloud

Right now everything runs on the MacBook, so capture only works while it's on and awake. The strong version: run scripts/ingest.py on a cheap cloud server (Railway, like Rekko's n8n workflows) on a schedule, so Telegram links/photos/voice notes get processed 24/7 with the laptop closed. The Mac would then only run the chat app and pull the repo. Revisit after a few weeks of real usage. Saved 2026-08-24.

## Real RAG search

Replace keyword matching in app/server.py with embeddings when the vaults reach hundreds of files. Aiden wants to learn how to build this himself (planned as a learning project, ~mid-September 2026).

## Public template repo (when sharing with others)

This repo stays PRIVATE. It holds real personal data: 22 wiki notes, 22 video breakdowns, and profile files with school schedule, business plans, and content strategy. That data is also in git history, so making this repo public would expose it even if the files were deleted first.

When it is time to share, do NOT flip this repo public. Instead create a separate `second-brain-template` repo with fresh history containing only: code (scripts/, app/), prompts/, the CLAUDE.md rule files, empty vault folders with .gitkeep, .env.example, requirements.txt, README.md, SETUP-FOR-FRIENDS.md. No wiki content, no raw breakdowns, no overview.md profiles. Decided 2026-08-24.
