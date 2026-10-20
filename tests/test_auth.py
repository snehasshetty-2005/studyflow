from app.extensions import db
from app.models import User
from tests.conftest import login, register


def test_registration_hashes_password_and_logs_in(client, app):
    response = register(client)
    assert response.status_code == 200
    assert b"Your account is ready" in response.data
    with app.app_context():
        user = db.session.scalar(db.select(User).where(User.email == "student@example.com"))
        assert user is not None
        assert user.password_hash != "correct-horse-7"
        assert user.check_password("correct-horse-7")


def test_duplicate_email_is_rejected(client):
    register(client)
    client.post("/logout")
    response = client.post("/register", data={
        "name": "Another Student", "email": "STUDENT@example.com",
        "password": "correct-horse-7", "confirm_password": "correct-horse-7",
    })
    assert b"already exists" in response.data


def test_login_and_logout(client):
    register(client)
    client.post("/logout", follow_redirects=True)
    assert client.get("/dashboard").status_code == 302
    assert login(client).status_code == 200
    client.post("/logout", follow_redirects=True)
    assert client.get("/dashboard").status_code == 302


def test_incorrect_login_is_generic(client):
    register(client)
    client.post("/logout")
    response = client.post("/login", data={"email": "student@example.com", "password": "wrong"})
    assert b"Email or password is incorrect" in response.data


def test_login_is_rate_limited(app):
    app.config["RATELIMIT_ENABLED"] = True
    client = app.test_client()
    responses = [client.post("/login", data={"email": "student@example.com", "password": "wrong"}) for _ in range(6)]
    assert all(response.status_code == 200 for response in responses[:5])
    assert responses[5].status_code == 429
    assert b"Too many login attempts" in responses[5].data


def test_registration_validates_required_fields(client):
    response = client.post("/register", data={"name": "", "email": "not-an-email", "password": "x", "confirm_password": "y"})
    assert b"Enter a name" in response.data
    assert b"Enter a valid email" in response.data
    assert response.status_code == 200
