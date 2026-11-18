# Job Application Tracker

Flask + MySQL app to track companies, jobs, applications and contacts, with a dashboard and a
skills-based **Job Match** page. UI uses [Pico.css](https://picocss.com) (loaded from a CDN, so you need internet in the browser).

**Video demo:** [Watch on Vimeo](https://vimeo.com/1248091616?share=copy&fl=sv&fe=ci)

MySQL runs **locally inside the conda env** with its data in `./mysql-data`, so nothing is installed system-wide.

## Prerequisites

- **conda** (Miniconda / Miniforge / Anaconda). MySQL itself is installed by conda, so `requirements.txt` alone is not enough.
- **Linux, macOS or WSL** (on Windows use WSL or Git Bash, since `scripts/db.sh` is a bash script).
- Internet access for the first `conda env create` and for Pico.css (CDN) in the browser.
- Free ports **3307** (MySQL) and **5000** (Flask).

## Don't have conda? Install it first (5 minutes)

Install **Miniforge** (free, small, no admin rights needed):

```bash
# Linux / WSL / macOS: download and run the installer
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh -b -p "$HOME/miniforge3"
"$HOME/miniforge3/bin/conda" init "$(basename "$SHELL")"
# then CLOSE and REOPEN the terminal, and check:  conda --version
```

- **Windows:** install [WSL](https://learn.microsoft.com/windows/wsl/install) (`wsl --install` in PowerShell), open the Ubuntu terminal, and run the commands above.
- Or use the graphical installer: <https://conda-forge.org/download/>.

After that, continue with **Setup** below.

## Setup (once)

```bash
cd job_tracker
conda env create -f environment.yml      # or, if the env "job-app" already exists:
                                         # conda install -n job-app -c conda-forge mysql=9.7 mysql-server=9.7 flask mysql-connector-python pytest
conda activate job-app
scripts/db.sh reset                      # starts MySQL (port 3307), creates the schema from schema.sql
scripts/db.sh seed                       # optional: loads sample data
```

## Run

```bash
conda activate job-app
scripts/db.sh start                      # no-op if already running
python app.py                            # open http://127.0.0.1:5000
```

## Try it out

1. **Dashboard** (`/`): counts, applications by status, average salary, recent applications.
2. **Companies / Jobs / Applications / Contacts**: use *Add*, *View*, *Edit*, *Delete* (delete asks for confirmation). Try submitting an empty title or `2026-13-45` as a date to see validation. Deleting a company also removes its jobs, applications and contacts (FK cascade).
3. **Job Match** (`/job-match`): enter `Python, SQL, Flask`. Jobs are ranked by % of required skills you have, with missing skills listed. Skills are case-insensitive. Jobs' skills are entered comma-separated and stored as a JSON array.
4. Applications' *interview data* is a JSON object, e.g. `{"round": 1, "interviewer": "Sam"}`.

## Troubleshooting

| Problem | Fix |
|---|---|
| `MySQL failed to start; see mysql-data.log` | Read `mysql-data.log`. Usually the port is taken: `DB_PORT=3310 scripts/db.sh reset`, then run the app with the same `DB_PORT=3310`. |
| `Address already in use` on port 5000 | Stop the other process using it, or run `flask --app app run --port 5001`. |
| `mysqld: command not found` | Run `conda activate job-app` first. |
| Page has no styling | The browser needs internet for the Pico.css CDN. |
| Want to use your own MySQL | Set `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` and run `schema.sql` (and optionally `seed.sql`) against it. |

## Shut down

```bash
# 1. Stop the Flask app: press Ctrl+C in the terminal where `python app.py` is running
# 2. Stop the local MySQL server (data in ./mysql-data is kept):
scripts/db.sh stop
scripts/db.sh status                     # confirm it is stopped
conda deactivate                         # optional: leave the conda env
```

Next time, just follow **Run** again. Your data is still there.

## Tests

```bash
pytest -q         # matching + validation unit tests (no database needed)
```

## Project layout

| File | Purpose |
|---|---|
| `app.py` | Flask app, dashboard and job-match routes |
| `crud.py` | One generic list/add/edit/delete/detail blueprint used by all 4 tables |
| `resources.py` | Declarative table/field definitions driving the CRUD pages and forms |
| `validation.py` | Form input → clean values + errors |
| `matching.py` | Pure skill-matching functions |
| `database.py`, `config.py` | MySQL helpers and connection settings (env vars `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`) |
| `schema.sql`, `seed.sql` | Schema (4 tables, FKs, JSON columns) and sample data |
| `templates/`, `static/style.css` | Shared templates (`list`, `form`, `detail`) plus dashboard/job match |
| `scripts/db.sh` | Local MySQL control |
| `AI_USAGE.md` | GenAI documentation |

Note: instead of four near-identical `companies.html`, `jobs.html`... templates, one generic `list.html`/`form.html` serves every table.

## Database commands

`scripts/db.sh start | stop | status | reset | seed | destroy`
(`reset` drops and recreates all tables; `destroy` stops MySQL and deletes `mysql-data/`.)

To use your own MySQL instead, set the `DB_*` env vars and run `schema.sql` against it.

## Remove everything

```bash
scripts/db.sh destroy
conda deactivate && conda env remove -n job-app
```
Then delete the project folder.
