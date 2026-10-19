# StudyFlow — Cloud Based Student Task Manager

StudyFlow is a responsive Flask application for students to organize assignments, study sessions, subjects, and due dates. It provides account registration and sign in, private task management, search and filters, and a dashboard whose counts come from the signed-in user's database records.

> **Project status:** Python 3.13.16 and the project dependencies are installed in `.venv`. The initial migration has been generated and applied to the ignored local SQLite database. The app startup smoke check passed, and pytest reports **12 passed**. Render + Supabase are the proposed demo setup; `render.yaml` is prepared, but no provider account, cloud resource, GitHub remote, or live deployment is configured.

## Contents

- [Features](#features)
- [How the application works](#how-the-application-works)
- [Project files](#project-files-and-what-each-file-does)
- [Technology](#technology)
- [Local setup](#local-setup)
- [Database and migrations](#database-and-migrations)
- [Environment variables](#environment-variables)
- [Tests](#tests)
- [Security and privacy](#security-and-privacy)
- [Deployment status and cost](#deployment-status-and-cost)
- [Limitations and next steps](#limitations-and-next-steps)
- [Documentation](#documentation)

## Features

- Register, sign in, sign out, and keep a private session.
- Create, read, edit, complete/reopen, and delete tasks.
- Give tasks a title, description, subject, due date, priority, and status.
- Search titles and descriptions; filter by status, priority, and subject; sort by due date, priority, or recent update.
- View total, pending, in-progress, completed, overdue, and completion-rate metrics calculated from the current user's task records.
- See a weekly completion visualization, upcoming due dates, and recently updated tasks.
- Use responsive desktop, tablet, and mobile layouts, keyboard focus styles, form labels, status text, and delete confirmation.
- Use SQLite for local development and tests, with a configurable SQLAlchemy database URL for a hosted relational database.

## How the application works

1. `run.py` creates the Flask app through `create_app()` in `app/__init__.py`.
2. The app loads settings from environment variables, configures SQLAlchemy, Flask-Migrate, Flask-Login, and CSRF protection, then registers the auth, main, and task route blueprints.
3. A registration request is validated on the server. The password is transformed with Werkzeug's password hashing helper; only the resulting hash is stored. Login checks the submitted password against that hash.
4. Flask-Login identifies the active user from the signed session cookie. Private routes require login.
5. Each task query includes both the requested task ID and `current_user.id`. A task that does not belong to the signed-in account returns 404, including for update, completion, and deletion routes.
6. Task changes use POST requests protected by Flask-WTF CSRF tokens. SQLAlchemy writes the change to the configured database.
7. The dashboard queries only the current user's tasks and calculates the cards, upcoming items, recent activity, and weekly counts from those records.
8. Jinja renders HTML templates. Static CSS and a small JavaScript file provide layout, responsive navigation, flash dismissal, and browser confirmation before deletion.

Overdue means a task is not completed and its due date is earlier than the server's local calendar date. A task without a due date is not overdue. Completion rate is completed tasks divided by total tasks; it is zero when there are no tasks. Timestamps are generated in UTC; SQLite may return naive datetime values, which the UI formats as dates without converting to a user-specific time zone. The date-based overdue rule currently uses the host's local date; configure production hosts to UTC or adapt the rule to an explicit user timezone before relying on it across regions.

## Project files and what each file does

| Path | Purpose and lifecycle |
| --- | --- |
| `run.py` | Manually created local development entry point; imports the app factory and runs Flask. |
| `wsgi.py` | Manually created WSGI entry point for a production server. |
| `render.yaml` | Render Blueprint for a Python 3.13.16 web service, generated secret, private database URL, migration command, and Gunicorn server. |
| `config.py` | Manually created configuration class; reads secret, database, and cookie settings from the environment and rejects a missing production secret. |
| `.env.example` | Manually created safe template for local environment values. Copy to `.env`; never put real secrets in the example. |
| `.python-version` | Manually created runtime version hint; selects the latest Python 3.13 patch release where supported. |
| `.gitignore` | Manually created ignore rules for virtualenvs, secrets, databases, caches, and build output. |
| `requirements.txt` | Manually created list of Python packages installed into the virtual environment by pip. |
| `.venv/` | Generated by `py -m venv .venv`; holds this project's Python interpreter and installed dependencies. It is ignored by Git and should be recreated on another machine. |
| `app/__init__.py` | App factory, creates Flask's runtime `instance/` directory, extension setup, blueprint registration, common template values, and generic error handlers. |
| `app/extensions.py` | Creates shared SQLAlchemy, migration, login, and CSRF extension objects; the factory initializes them. |
| `app/models.py` | User and task tables, password helpers, task enum constraints, relationships, completion timestamp, and login user loader. |
| `app/auth/__init__.py` | Defines the authentication URL blueprint. |
| `app/auth/routes.py` | Registration, login, logout, input validation, password verification, and safe redirect handling. |
| `app/main/__init__.py` | Defines the dashboard URL blueprint. |
| `app/main/routes.py` | Dashboard metrics, weekly data, upcoming deadlines, and recent task data. |
| `app/tasks/__init__.py` | Defines the task-management URL blueprint. |
| `app/tasks/routes.py` | Task list, search/filter/sort, validation, CRUD routes, and per-user ownership checks. |
| `app/templates/base.html` | Shared page shell, navigation, flash messages, stylesheet, and JavaScript references. |
| `app/templates/auth/login.html` | Sign-in form. |
| `app/templates/auth/register.html` | Account registration form. |
| `app/templates/main/dashboard.html` | Data-backed metrics, weekly progress, upcoming deadlines, and recent tasks. |
| `app/templates/tasks/list.html` | Search, filters, sort controls, task rows, empty state, and task actions. |
| `app/templates/tasks/form.html` | Shared create and edit task form. |
| `app/templates/tasks/detail.html` | Task details, edit, completion/reopen, and delete controls. |
| `app/templates/errors/403.html`, `404.html`, `500.html` | Safe user-facing error pages; no stack trace is displayed. |
| `app/static/css/style.css` | Design tokens, dashboard/auth/task layouts, responsive breakpoints, and focus/reduced-motion styles. |
| `app/static/js/main.js` | Confirmation prompts, dismissible flash messages, and mobile navigation toggle. |
| `tests/conftest.py` | Pytest app fixture, in-memory test database, and test helpers; database tables are created/dropped for tests. |
| `tests/test_auth.py` | Registration, duplicate email, password hash, login/logout, and validation checks. |
| `tests/test_tasks.py` | CRUD, validation, filtering/search, and cross-user isolation checks. |
| `tests/test_dashboard.py` | Dashboard metrics, empty-state safety, and CSRF checks. |
| `migrations/alembic.ini` | Generated by `flask db init`; Alembic migration configuration. |
| `migrations/env.py` | Generated by `flask db init`; loads Flask app/database metadata for migration commands. |
| `migrations/README` | Generated migration repository note. |
| `migrations/script.py.mako` | Generated Alembic template used when creating migration revision files. |
| `migrations/versions/cbdd23d24ef5_create_users_and_tasks.py` | Generated and reviewed initial schema migration for users and tasks, including `completed_at`. |
| `instance/` | Flask runtime instance directory; SQLite database files may be stored here. Keep its local data out of Git. |
| `docs/` | Manually maintained architecture, database, deployment, testing, and troubleshooting guides. |

Flask-Migrate commands generate the migration repository and revision scripts. Flask creates runtime/cache directories as needed. `pip install -r requirements.txt` creates package files inside the virtual environment; do not commit those generated files.

## Technology

- Python 3.11 or later supported Python 3.x
- Flask, Jinja, Flask-SQLAlchemy, SQLAlchemy, Flask-Migrate/Alembic
- Flask-Login, Werkzeug password hashing, Flask-WTF CSRF protection
- SQLite locally; a PostgreSQL-compatible SQLAlchemy URL can be provided for hosting
- pytest
- Plain CSS and small browser JavaScript; no frontend build system

## Local setup

### 1. Install Python

Install a currently supported Python 3 release from [python.org](https://www.python.org/downloads/) and enable the Windows Python launcher/PATH option during installation. Open a **new** terminal and check:

```powershell
py --version
```

On macOS/Linux, check `python3 --version`. This workspace session did not have either `python` or `py` available, so this prerequisite must be resolved before running the app.

### 2. Open the project and create a virtual environment

In PowerShell:

```powershell
cd "C:\Users\sneha\OneDrive\Desktop\cloud task manager"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt, or temporarily allow locally generated scripts in this PowerShell process with `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate. In Command Prompt:

```bat
cd /d "C:\Users\sneha\OneDrive\Desktop\cloud task manager"
py -m venv .venv
.venv\Scripts\activate.bat
```

On macOS/Linux:

```sh
cd "/path/to/cloud task manager"
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install packages and prepare local configuration

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

On Command Prompt use `copy .env.example .env`; on macOS/Linux use `cp .env.example .env`. Edit `.env` and replace `SECRET_KEY` with a private random value. Generate one locally (do not paste it into chat or commit it):

```powershell
py -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Create and upgrade the local database

Run these once from the activated environment to create the migration repository and first schema revision:

```powershell
python -m flask --app run.py db init
python -m flask --app run.py db migrate -m "Create user and task tables"
python -m flask --app run.py db upgrade
```

The migration commands generate the `migrations/` folder and a revision file, then apply that revision. For later model/schema changes, run `db migrate -m "describe change"`, review the generated revision, and run `db upgrade`. Details are in [Database and migrations](docs/DATABASE.md).

### 5. Start the server

```powershell
python run.py
```

Open <http://127.0.0.1:5000>. Stop the server with `Ctrl+C`; leave the virtual environment with `deactivate`.

## Database and migrations

The user table stores a display name, normalized unique email, password hash, and creation timestamp. The task table stores its owner, title, optional description/subject/due date, constrained priority/status, creation/update timestamps, and `completed_at` to record when completion happened. A foreign key with cascade delete and an index on `user_id` support ownership queries. See [docs/DATABASE.md](docs/DATABASE.md).

Local development uses SQLite. Production database choice is intentionally not hard-coded. Set `DATABASE_URL` in the host's private environment settings to a supported SQLAlchemy URL. Verify the database provider's current policies and connection requirements before choosing a production service.

## Environment variables

| Variable | Required | Meaning |
| --- | --- | --- |
| `SECRET_KEY` | Yes in production; recommended locally | Signs Flask sessions and CSRF tokens. Keep private and random. |
| `DATABASE_URL` | No locally; yes when selecting a hosted database | SQLAlchemy connection URL. Defaults to local SQLite at `sqlite:///student_tasks.db` (Flask-SQLAlchemy resolves relative SQLite paths under the instance folder). |
| `COOKIE_SECURE` | Set to `1` behind HTTPS in production | Adds the Secure attribute to session cookies. Keep `0` for local HTTP development. |
| `FLASK_APP` | Optional | Example file is `run.py`; CLI examples also pass `--app run.py`. |
| `FLASK_DEBUG` | Optional | Set to `1` only for local development. Never enable debug mode on a public production server. |

## Tests

Install dependencies, activate the environment, then run:

```powershell
python -m pytest
```

Tests use a separate in-memory SQLite database. They cover account flows and hashing, task CRUD and validation, filtering, user isolation, dashboard calculations, the zero-task case, and rejection of a state-changing request without a CSRF token. **Verified result in this workspace: 12 passed** with Python 3.13.16 and pytest 8.4.2 using `python -m pytest -q`.

## Security and privacy

- Passwords are hashed with Werkzeug; plain-text passwords are never stored.
- Private routes use Flask-Login, and task reads/writes/deletes check the owner in the database query.
- Flask-WTF CSRF protection is enabled globally. All state-changing HTML forms include CSRF tokens.
- SQLAlchemy ORM expressions parameterize values; Jinja autoescapes displayed user text.
- Server-side validation limits lengths and allowed priority/status values.
- Production must set a private `SECRET_KEY`, use HTTPS, set `COOKIE_SECURE=1`, and keep debug disabled.
- The app currently does not implement login rate limiting, email verification, password reset, or session revocation after password changes.
- A public demo should use fake student data only. Never commit `.env`, a database containing personal data, or production credentials.

## Deployment status and cost

**Suggested portfolio demo setup (not deployed): Render Free web service + Supabase Free PostgreSQL.** Current official pricing pages list both free plans at $0. Supabase Free currently includes 500 MB database, 50,000 monthly active users, 5 GB uncached and 5 GB cached egress, and at most two active projects; low-activity projects may pause after seven days. Render Free supports Python web services, sleeps after 15 minutes idle, takes about a minute to wake, has a shared 750 service-hour monthly allowance, and has ephemeral local disk. Render's setup guide says no payment is required; do not add a card if maintaining a strict ₹0 cap, because overage fees may apply once a payment method is added. Supabase's checked public docs don't clearly establish whether a card is required during Free signup, so verify the signup screen before creating a project. These tiers are suitable only for a hobby/portfolio demonstration with fake data, not a production service or real student records. Supabase Free has no downloadable database backups.

The suggested host supports Python 3.13 and the repo includes `.python-version`. Render's documented build command is `pip install -r requirements.txt`; this app's WSGI start command is `gunicorn --bind 0.0.0.0:$PORT wsgi:app`. Set `SECRET_KEY`, `DATABASE_URL`, `COOKIE_SECURE=1`, and `FLASK_DEBUG=0` in the host's private environment settings. Apply reviewed database migrations as part of the deployment build/release procedure. A public Git repository is needed for the simple dashboard-based Render flow.

No accounts, services, or deployment were created or checked. Before setup, review the official [Render free service limits](https://render.com/docs/free), [Render Flask deployment guide](https://render.com/docs/deploy-flask), [Render Python version guide](https://render.com/docs/python-version), [Supabase pricing](https://supabase.com/pricing), [Supabase project pausing policy](https://supabase.com/docs/guides/platform/free-project-pausing), and [Supabase Postgres connection guidance](https://supabase.com/docs/guides/database/connecting-to-postgres). Exact terms may change. Full steps are in [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

## Limitations and next steps

- Install Python and dependencies, then execute migrations, app startup, and tests.
- Review generated Alembic migration scripts before applying them.
- Perform browser/manual accessibility and responsive checks at 360px, 768px, and 1280px.
- Verify hosted provider plans and policies from official pages before selecting/deploying.
- Add pagination beyond the current 100-row list cap if datasets grow.
- Consider account recovery, rate limiting, and an explicit user timezone before production use.
- Capture real screenshots and add them after running the application; no screenshots or deployment URL are fabricated here.

## Resume and interview preparation

The following bullets describe the implementation in the repository. Keep the testing and deployment statements conditional until those steps have been run and verified:

- Built a Flask and SQLAlchemy student task manager with account authentication, password hashing, and per-user task ownership checks.
- Implemented task CRUD, search/filter/sort, status and priority tracking, and a dashboard calculated from the signed-in user's task records.
- Added pytest coverage for authentication, task workflows, CSRF, dashboard metrics, and cross-user access controls; 12 tests passed in this environment.

Interview talking points:

| Question | Answer based on this implementation |
| --- | --- |
| Why Flask? | The app is a small server-rendered project; Flask keeps routing, templates, and deployment straightforward without a frontend build system. |
| How does authentication work? | Flask-Login stores the authenticated user identifier in a signed session; login checks the submitted password against a Werkzeug hash. |
| Why hash passwords? | Hashing means the database does not contain the original password. Werkzeug's password checker verifies candidates without storing plaintext. |
| How is task ownership enforced? | The server adds the current user ID to each task lookup before returning or changing a task. A mismatched owner receives a 404. |
| How is the database structured? | A user has many tasks. Tasks have a foreign key, constrained priority/status values, and timestamps; local development uses SQLite. |
| How are secrets configured? | Environment variables are loaded locally from an ignored `.env`; production must provide a private `SECRET_KEY` and database URL through its secret settings. |
| What happens if the database is unavailable? | A request may fail and the user sees a generic 500 page. Detailed failure handling, health checks, retries, and operational alerts still need production hardening. |
| How does deployment work? | `wsgi.py` exports the Flask application and `gunicorn wsgi:app` is the planned Linux WSGI command. No provider has been selected or verified yet. |
| What tests protect the app? | Auth, password hashing, task CRUD/validation, filters, user isolation, dashboard counts, zero-task behavior, and CSRF are covered by authored pytest cases. The suite remains unrun. |
| What would you improve next? | Run the suite, perform browser/accessibility checks, add pagination and account recovery/rate limits, and choose a host only after verifying current costs and limits. |

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Database and migrations](docs/DATABASE.md)
- [Deployment checklist](docs/DEPLOYMENT.md)
- [Testing guide](docs/TESTING.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- The original detailed project specification is [specdrive.md](specdrive.md).
