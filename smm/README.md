# SINERGY SMM v1.1 Working Core

AI-first multi-tenant SMM Operating System.

## Modules
- apps/mobile: Expo React Native app for iOS/Android
- apps/web-admin: Next.js command center
- backend: FastAPI API
- workers: async publishing/analytics workers
- shared: shared domain contracts
- docs: architecture, security, store/release notes

## Core product loop
Brand Brain → AI Studio → Calendar → Publish → Omnichannel Inbox → Leads → Analytics → Autopilot.

Legacy SMM AI BOT is treated only as a feature reference. Old sessions, SQLite runtime DBs, certificates and secrets are intentionally excluded.

## v1.1 implemented
JWT auth, tenant workspaces, SQLAlchemy/PostgreSQL-ready domain, Alembic, Brand Brain, persistent content/calendar, Inbox schema, CRM attribution, analytics, Autopilot plan API, integration entry points, five-screen Expo mobile shell and updated Command Center.
