# Troubleshooting

## `python` or `py` is not recognized

If Python is missing on another machine, install Python 3 from python.org, enable the Python launcher/PATH option, close and reopen the terminal, and check `py --version` (Windows) or `python3 --version` (macOS/Linux). In this workspace, Python 3.13.16 is installed under the current user's Programs folder and the app dependencies are in `.venv`.

## Flask cannot find the app

Run commands from the project root with the virtual environment active. Use `python -m flask --app run.py ...` so Flask imports the correct module.

## `SECRET_KEY is required`

Copy `.env.example` to `.env` and set a private random `SECRET_KEY`. Do not commit `.env`. The development-only fallback is available only when `FLASK_DEBUG=1`; production startup intentionally fails without a secret.

## Database tables are missing

Run the `db init` command once if no `migrations/` directory exists, then `db migrate` and `db upgrade`. For a later model change, generate and review a new migration, then upgrade.

## PowerShell will not activate the virtual environment

Use Command Prompt activation (`.venv\Scripts\activate.bat`) or follow Microsoft guidance for a suitable PowerShell execution policy. Avoid changing machine-wide policy just for this project.

## Port 5000 is already in use

Stop the process using the port or run Flask on another local port with `flask --app run.py run --port 5001`.

## A static style/script change is not visible

Hard-refresh the browser after confirming the edited file is under `app/static/`. Clear caches only if needed.

## Production database connection fails

Check host-provided `DATABASE_URL`, SSL/TLS options, network allowlists, connection limits, and whether the database is paused. Never print the full URL into logs because it may contain a password.
