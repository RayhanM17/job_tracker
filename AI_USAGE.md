# AI Usage Documentation

## Tools Used
- Claude (Claude Code CLI) to scaffold the project, write the Flask app, and debug the local MySQL setup.

## Key Prompts
1. "Read the spec doc and build an app that meets all requirements; keep the code modular, with no repeated code, easy to set up and delete."
2. "Use Pico.css for the UI."

## What Worked Well
- Generating the schema, a config-driven generic CRUD blueprint, and the pure matching function.
- Diagnosing why MySQL would not restart: InnoDB silently ignores a data directory whose name starts with a dot (`.mysql-data`), so I renamed it to `mysql-data`.

## What I Modified
- *(Fill in your own changes here, e.g. field names, validation rules, styling tweaks.)*

## Lessons Learned
- Run the code: the first database script had a wrong "is initialized" check that only showed up when started.
- AI output needs testing against the real database, not only unit tests.
- *(Add your own reflections.)*
