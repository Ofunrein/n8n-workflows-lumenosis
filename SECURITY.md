# Workflow credentials

Workflow templates and the two Vercel catalogs must not contain live webhook URLs.
The scheduled Discord template reads `DISCORD_WEBHOOK_URL` from the n8n instance
environment. Configure that value outside this repository before activating the
imported workflow. If the instance blocks environment access, configure a Discord
credential in n8n instead. Never save the credential into an exported template.

Before committing exported workflows, run:

```sh
python3 scripts/test-discord-webhooks.py
python3 scripts/check-discord-webhooks.py
```

The guard checks tracked JSON files, including generated catalogs, and reports
filenames without printing credential values. It checks Discord webhook patterns;
it is not a general-purpose secret scanner.

Removing a credential from the current files does not invalidate it or remove it
from Git history. A Discord administrator must revoke or replace any exposed
webhook through Discord. Do not test an exposed URL by sending a request to it.
