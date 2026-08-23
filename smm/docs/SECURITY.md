# Security baseline
- No social tokens in source control.
- OAuth tokens encrypted at rest and scoped per workspace.
- Rotation/revocation support.
- RBAC and immutable audit events for publish/delete/export actions.
- No legacy Telegram .session files, private certificates or SQLite runtime DBs are migrated.
- Store clients use short-lived API access tokens; privileged secrets stay server-side.
