# AI Usage Documentation

## Tools Used
- Claude (Claude Code CLI) to scaffold the project, write the Flask app, and debug the local MySQL setup.

## Key Prompts
1. "Read the spec doc and build an app that meets all requirements; keep the code modular, with no repeated code, easy to set up and delete."
2. "Use Pico.css for the UI."
3. "Will the professor be able to run the app?" (with the instructor note: they will clone the repo and run it, so the README needs clear setup instructions).
4. "Add steps for someone without conda."
5. "Update the AI usage too with our convos and changes so far, then push to GitHub."

## Fresh-Clone Verification (conversation summary)
I asked whether the instructor could run the app after cloning. Claude cloned the repo to a clean directory and ran the README steps: schema creation, seeding, the app serving `/` and `/job-match` (HTTP 200) and all 7 tests passing. That test found real issues:
- MySQL failed to start when the clone lived in a long directory path, because the Unix socket path limit is about 107 characters.
- The README did not state that conda is required, that Windows needs WSL/Git Bash, which ports are used, or how to troubleshoot.

## Changes Made From That Review
- `scripts/db.sh`: the MySQL socket now lives at `/tmp/job-tracker-mysql-<port>.sock`, so it works from any clone location. Re-tested from a very long path and it started, created the schema and seeded.
- `README.md`: added Prerequisites, a "Don't have conda?" install section (Miniforge, WSL for Windows) and a Troubleshooting table (port conflicts, `mysqld` not found, no styling, using your own MySQL).
- `AI_USAGE.md`: this section.

## What Worked Well
- Generating the schema, a config-driven generic CRUD blueprint, and the pure matching function.
- Diagnosing why MySQL would not restart: InnoDB silently ignores a data directory whose name starts with a dot (`.mysql-data`), so I renamed it to `mysql-data`.

## What I Modified
- *(Fill in your own changes here, e.g. field names, validation rules, styling tweaks.)*

## Lessons Learned
- Run the code: the first database script had a wrong "is initialized" check that only showed up when started.
- AI output needs testing against the real database, not only unit tests.
- *(Add your own reflections.)*
