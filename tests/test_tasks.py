from tests.conftest import login, register
from app.extensions import db
from app.models import Task


def test_create_edit_complete_reopen_and_delete(client):
    register(client)
    response = client.post("/tasks/new", data={
        "title": "Read chapter", "description": "Take notes", "subject": "Biology",
        "priority": "High", "status": "Pending", "due_date": "2030-05-20",
    })
    assert response.status_code == 302
    with client.application.app_context():
        task = db.session.scalar(db.select(Task))
        task_id = task.id
    assert client.post(f"/tasks/{task_id}/edit", data={
        "title": "Read chapter 2", "description": "", "subject": "Biology",
        "priority": "Medium", "status": "In Progress", "due_date": "",
    }).status_code == 302
    with client.application.app_context():
        task = db.session.get(Task, task_id)
        assert task.title == "Read chapter 2"
        assert task.status == "In Progress"
    client.post(f"/tasks/{task_id}/toggle")
    with client.application.app_context():
        task = db.session.get(Task, task_id)
        assert task.status == "Completed"
        assert task.completed_at is not None
    client.post(f"/tasks/{task_id}/toggle")
    with client.application.app_context():
        task = db.session.get(Task, task_id)
        assert task.status == "Pending"
        assert task.completed_at is None
    client.post(f"/tasks/{task_id}/delete")
    with client.application.app_context():
        assert db.session.get(Task, task_id) is None


def test_task_validation_rejects_bad_enum(client):
    register(client)
    response = client.post("/tasks/new", data={"title": "Study", "priority": "Urgent", "status": "Pending"})
    assert b"Choose a valid priority" in response.data
    response = client.post("/tasks/new", data={"title": "Study", "priority": "Low", "status": "Blocked"})
    assert b"Choose a valid status" in response.data


def test_search_filters_and_sort(client):
    register(client)
    client.post("/tasks/new", data={"title": "Algebra worksheet", "subject": "Math", "priority": "High", "status": "Pending"})
    client.post("/tasks/new", data={"title": "Cell notes", "subject": "Biology", "priority": "Low", "status": "In Progress"})
    response = client.get("/tasks/?q=Algebra&status=Pending&priority=High&sort=priority")
    assert b"Algebra worksheet" in response.data
    assert b"Cell notes" not in response.data
    response = client.get("/tasks/?q=no-such-task")
    assert b"No matching tasks" in response.data


def test_user_cannot_read_edit_complete_or_delete_another_users_task(client, app, create_user):
    owner = create_user("Owner", "owner@example.com")
    stranger = create_user("Stranger", "stranger@example.com")
    with app.app_context():
        task = Task(user_id=owner.id, title="Private assignment")
        db.session.add(task)
        db.session.commit()
        task_id = task.id
    login(client, "stranger@example.com")
    assert client.get(f"/tasks/{task_id}").status_code == 404
    assert client.get(f"/tasks/{task_id}/edit").status_code == 404
    assert client.post(f"/tasks/{task_id}/edit", data={"title": "Stolen"}).status_code == 404
    assert client.post(f"/tasks/{task_id}/toggle").status_code == 404
    assert client.post(f"/tasks/{task_id}/delete").status_code == 404
    with app.app_context():
        assert db.session.get(Task, task_id).title == "Private assignment"
