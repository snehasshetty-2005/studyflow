import pytest

from app import create_app
from app.extensions import db
from app.models import User


class TestConfig:
    TESTING = True
    SECRET_KEY = "pytest-only-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False


@pytest.fixture
def app():
    application = create_app(TestConfig)
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def register(client, name="Test Student", email="student@example.com", password="correct-horse-7"):
    return client.post("/register", data={
        "name": name, "email": email, "password": password,
        "confirm_password": password,
    }, follow_redirects=True)


def login(client, email="student@example.com", password="correct-horse-7"):
    return client.post("/login", data={"email": email, "password": password}, follow_redirects=True)


@pytest.fixture
def create_user(app):
    def _create(name, email, password="correct-horse-7"):
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    return _create
