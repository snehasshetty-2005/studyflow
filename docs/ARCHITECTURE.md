# Architecture

## Request flow

```text
Browser
  ├── Jinja pages / static CSS and JavaScript
  └── HTTP requests with Flask session cookie + CSRF token
          ↓
Flask app factory (app/__init__.py)
  ├── auth blueprint: registration, login, logout
  ├── main blueprint: dashboard metrics
  └── tasks blueprint: CRUD, search, filtering, sorting
          ↓
Flask-Login + Flask-WTF + SQLAlchemy ORM
          ↓
SQLite locally / configured SQLAlchemy database URL when hosted
```

`run.py` is for local use. A production WSGI server imports `app` from `wsgi.py`. The factory pattern keeps setup testable and permits pytest to pass a separate test configuration.

## Why these pieces

- Flask and Jinja keep the server-rendered application small and approachable for a Python learner.
- SQLAlchemy expresses ownership and filters in ORM queries and supports SQLite locally plus PostgreSQL drivers.
- Flask-Login manages user sessions; Werkzeug stores password hashes.
- Flask-WTF applies CSRF checks to unsafe methods.
- Flask-Migrate provides Alembic revisions for schema evolution.
- CSS and a small JavaScript file avoid adding a frontend framework or build pipeline.

## Trust boundaries

The browser is untrusted. The server validates fields and allowed enum values. Every task endpoint filters on both `Task.id` and the current user's ID before returning or mutating a record. User-provided strings are rendered through Jinja's escaping. Session and CSRF signing depend on `SECRET_KEY`.

## Time assumptions

Created, updated, and completion timestamps are created in UTC. The current implementation calculates overdue against the server's local calendar date because no per-user timezone setting exists. Hosts should use UTC until timezone-aware user preferences are implemented. Dates such as due dates are calendar dates and are not timestamps. Weekly completions are grouped by the date portion of `completed_at`.
