from datetime import timedelta

from app.extensions import db
from app.models import Task, utcnow
from tests.conftest import register


def test_dashboard_metrics_are_user_specific(client, app, create_user):
    register(client)
    other = create_user("Other", "other@example.com")
    with app.app_context():
        # Find the signed-in test account from the session without relying on its numeric ID.
        from app.models import User
        user = db.session.scalar(db.select(User).where(User.email == "student@example.com"))
        db.session.add_all([
            Task(user_id=user.id, title="Pending one", status="Pending", due_date=utcnow().date() - timedelta(days=1)),
            Task(user_id=user.id, title="Completed one", status="Completed", due_date=utcnow().date() - timedelta(days=2)),
            Task(user_id=user.id, title="Working one", status="In Progress"),
            Task(user_id=other.id, title="Other user's task", status="Pending"),
        ])
        db.session.commit()
    response = client.get("/dashboard")
    assert b"Total tasks" in response.data
    assert b">3<" in response.data
    assert b"Other user&#39;s task" not in response.data
    assert b"Overdue" in response.data


def test_empty_dashboard_is_safe(client):
    register(client)
    response = client.get("/dashboard")
    assert b"0 percent of tasks completed" in response.data
    assert b"Create your first task" in response.data


def test_csrf_protects_state_changes(app):
    app.config["WTF_CSRF_ENABLED"] = True
    client = app.test_client()
    response = client.post("/register", data={
        "name": "No token", "email": "csrf@example.com",
        "password": "correct-horse-7", "confirm_password": "correct-horse-7",
    })
    assert response.status_code == 400
