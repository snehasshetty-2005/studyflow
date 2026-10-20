"""Application configuration sourced from environment variables."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///student_tasks.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    _debug_mode = os.environ.get("FLASK_DEBUG", "0").lower() in {"1", "true", "yes"}
    SESSION_COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "0" if _debug_mode else "1").lower() in {"1", "true", "yes"}
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
    WTF_CSRF_TIME_LIMIT = 3600
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")

    @classmethod
    def validate(cls, app):
        if not app.config.get("SECRET_KEY"):
            if app.testing:
                app.config["SECRET_KEY"] = "test-only-secret-do-not-use-in-production"
            elif os.environ.get("FLASK_DEBUG", "0").lower() in {"1", "true", "yes"}:
                app.config["SECRET_KEY"] = "local-development-secret-change-me"
                app.logger.warning("Using a development-only secret key.")
            else:
                raise RuntimeError("SECRET_KEY is required. Set it in the environment before starting the app.")
