# Testing

## Run the suite

```sh
python -m pip install -r requirements.txt
python -m pytest
```

Pytest loads `tests/conftest.py`, creates the Flask app with a dedicated in-memory SQLite database, creates schema before a test, then drops it afterward. Tests do not connect to a hosted database.

## Coverage intent

- `test_auth.py`: valid registration, unique normalized email, password hashing, correct/incorrect login, logout, and field validation.
- `test_tasks.py`: create/edit/delete, complete/reopen, enum validation, search/filter, and user A/B access isolation for detail/edit/toggle/delete.
- `test_dashboard.py`: database-derived counts, other-user exclusion, safe zero-task completion rate, and CSRF rejection without a token.

## Result in this workspace

Verified on Python 3.13.16 and pytest 8.4.2: **12 passed** (`.venv\Scripts\python.exe -m pytest -q`). The initial run found four failures; the authentication tests were corrected to sign out between attempts, an empty completion timestamp case was fixed, and enum validation messages were added to the form. The suite then passed. Manual browser checks at 360px, 768px, and 1280px remain outstanding.
