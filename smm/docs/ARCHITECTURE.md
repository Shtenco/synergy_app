# Architecture

SINERGY SMM is multi-tenant by default.

Domain: User → Workspace → Brand → SocialAccount. Operational streams: Content/Campaign, Conversation/Inbox, Lead/CRM, Analytics. Brand Brain stores approved brand knowledge; Autopilot consumes only workspace-scoped data.

Official API adapters are preferred. Mass unsolicited automation and legacy user-session inviters are intentionally outside the store product.

Production target: PostgreSQL + Redis + FastAPI + worker pool + object storage + encrypted secrets vault + web/mobile clients.
