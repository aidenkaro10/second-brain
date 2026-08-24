# Roadmap

Ideas agreed on but intentionally saved for later.

## Move ingest to the cloud

Right now everything runs on the MacBook, so capture only works while it's on and awake. The strong version: run scripts/ingest.py on a cheap cloud server (Railway, like Rekko's n8n workflows) on a schedule, so Telegram links/photos/voice notes get processed 24/7 with the laptop closed. The Mac would then only run the chat app and pull the repo. Revisit after a few weeks of real usage. Saved 2026-08-24.

## Real RAG search

Replace keyword matching in app/server.py with embeddings when the vaults reach hundreds of files. Aiden wants to learn how to build this himself (planned as a learning project, ~mid-September 2026).
