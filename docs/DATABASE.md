# Database and migrations

## Tables

### `user`

`id` primary key, `name` (required, max 80), `email` (required, unique, indexed, normalized to lowercase at registration), `password_hash` (required), and UTC `created_at`.

### `task`

`id` primary key, indexed required `user_id` foreign key, required `title` (max 160), optional `description` (max 2,000), `subject` (max 80), nullable calendar `due_date`, `priority` constrained to Low/Medium/High, `status` constrained to Pending/In Progress/Completed, UTC `created_at`/`updated_at` timestamps, and nullable UTC `completed_at`. The dedicated completion timestamp lets the weekly chart count when a task was completed instead of guessing from its last edit. Reopening clears that value. Deleting a user cascades to their tasks.

## Local database

The default SQLAlchemy URL is `sqlite:///student_tasks.db`; Flask-SQLAlchemy resolves this relative path beneath Flask's `instance/` directory. The database file is local data and ignored by Git. Tests use a separate in-memory SQLite database and create/drop tables inside the fixture.

## Initialize and migrate

After installing dependencies and configuring `.env`, initialize the migration repository once and create/apply the initial revision:

```sh
python -m flask --app run.py db init
python -m flask --app run.py db migrate -m "Create user and task tables"
python -m flask --app run.py db upgrade
```

Review every generated revision under `migrations/versions/`. For future schema changes, edit `app/models.py`, generate a descriptive revision, inspect its operations, then apply it with `db upgrade`. Do not delete or rewrite migrations that have already been applied to a shared production database.

The initial migration was generated as `migrations/versions/cbdd23d24ef5_create_users_and_tasks.py` and applied to the ignored local SQLite database in this workspace. Future schema changes should follow the commands above.

## Production connection

Set `DATABASE_URL` in the hosting provider's secret/environment settings. Never place credentials in source control, a browser bundle, issue text, screenshots, or this documentation. Use TLS and a least-privilege database user where supported. Verify provider-specific connection pooling, SSL mode, backups, sleep/inactivity, and data retention before deploying.
